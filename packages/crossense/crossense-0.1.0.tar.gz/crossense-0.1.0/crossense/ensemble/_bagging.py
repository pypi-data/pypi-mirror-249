from __future__ import annotations
import itertools
from abc import abstractmethod, ABCMeta
from functools import partial
from numbers import Integral
from typing import Union, Iterable, Optional

import numpy as np
from joblib import Parallel, delayed
from sklearn.base import (
    _fit_context,
    is_classifier,
    ClassifierMixin,
    RegressorMixin,
)
from sklearn.ensemble import BaseEnsemble

from sklearn.ensemble._base import _partition_estimators
from sklearn.model_selection import BaseCrossValidator
from sklearn.model_selection._split import check_cv, _BaseKFold
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.utils import indices_to_mask
from sklearn.utils._available_if import available_if
from sklearn.utils._param_validation import (
    HasMethods,
)
from sklearn.utils._tags import _safe_tags
from sklearn.utils.multiclass import check_classification_targets
from sklearn.utils.validation import (
    _check_sample_weight,
    has_fit_parameter,
    column_or_1d,
    check_is_fitted,
)


def _parallel_build_estimators(
    n_estimators,
    ensemble,
    indices,
    X,
    y,
    sample_weight,
    total_n_estimators,
    verbose,
    check_input,
):
    """Private function used to build a batch of estimators within a job."""
    # Retrieve settings
    n_samples, n_features = X.shape
    support_sample_weight = has_fit_parameter(ensemble.estimator_, "sample_weight")
    has_check_input = has_fit_parameter(ensemble.estimator_, "check_input")

    if not support_sample_weight and sample_weight is not None:
        raise ValueError("The base estimator doesn't support sample weight")

    # Build estimators
    estimators = []

    for i in range(n_estimators):
        if verbose > 1:
            print(
                "Building estimator %d of %d for this parallel run (total %d)..."
                % (i + 1, n_estimators, total_n_estimators)
            )

        estimator = ensemble._make_estimator(append=False)

        if has_check_input:
            estimator_fit = partial(estimator.fit, check_input=check_input)
        else:
            estimator_fit = estimator.fit

        # corresponding fold sample indices
        current_indices = indices[i]

        # Draw samples, using sample weights, and then fit
        if support_sample_weight:
            if sample_weight is None:
                curr_sample_weight = np.ones((n_samples,))
            else:
                curr_sample_weight = sample_weight.copy()

            not_indices_mask = ~indices_to_mask(current_indices, n_samples)
            curr_sample_weight[not_indices_mask] = 0

            estimator_fit(X, y, sample_weight=curr_sample_weight)
        else:
            estimator_fit(X[current_indices], y[current_indices])

        estimators.append(estimator)

    return (estimators,)


def _parallel_predict_proba(estimators, X, n_classes):
    """Private function used to compute (proba-)predictions within a job."""
    n_samples = X.shape[0]
    proba = []

    for estimator in estimators:
        if hasattr(estimator, "predict_proba"):
            proba_estimator = estimator.predict_proba(X)

            if n_classes == len(estimator.classes_):
                proba.append(proba_estimator)

            else:
                proba.append(proba_estimator[:, range(len(estimator.classes_))])

        else:
            # Resort to voting
            predictions = estimator.predict(X)
            p_ = np.zeros((n_samples, n_classes))
            for i in range(n_samples):
                p_[i, predictions[i]] += 1
            proba.append(p_)

    return proba


def _parallel_predict_log_proba(estimators, X, n_classes):
    """Private function used to compute log probabilities within a job."""
    n_samples = X.shape[0]
    log_proba = np.empty((n_samples, n_classes))
    log_proba.fill(-np.inf)
    all_classes = np.arange(n_classes, dtype=int)

    for estimator in estimators:
        log_proba_estimator = estimator.predict_log_proba(X)

        if n_classes == len(estimator.classes_):
            log_proba = np.logaddexp(log_proba, log_proba_estimator)

        else:
            log_proba[:, estimator.classes_] = np.logaddexp(
                log_proba[:, estimator.classes_],
                log_proba_estimator[:, range(len(estimator.classes_))],
            )

            missing = np.setdiff1d(all_classes, estimator.classes_)
            log_proba[:, missing] = np.logaddexp(log_proba[:, missing], -np.inf)

    return log_proba


def _parallel_decision_function(estimators, X):
    """Private function used to compute decisions within a job."""
    return sum(estimator.decision_function(X) for estimator in estimators)


def _parallel_predict_regression(estimators, X):
    """Private function used to compute predictions within a job."""
    return [estimator.predict(X) for estimator in estimators]


def _estimator_has(attr):
    """Check if we can delegate a method to the underlying estimator.

    First, we check the first fitted estimator if available, otherwise we
    check the estimator attribute.
    """

    def check(self):
        if hasattr(self, "estimators_"):
            return hasattr(self.estimators_[0], attr)
        elif self.estimator is not None:
            return hasattr(self.estimator, attr)
        else:  # TODO(1.4): Remove when the base_estimator deprecation cycle ends
            return hasattr(self.base_estimator, attr)

    return check


class BaseCrossBagging(BaseEnsemble, metaclass=ABCMeta):
    """Base class for cross-fold Bagging meta-estimator.

    Warning: This class should not be used directly. Use derived classes
    instead.
    """

    _parameter_constraints: dict = {
        "estimator": [HasMethods(["fit", "predict"]), None],
        "n_jobs": [None, Integral],
        "random_state": ["random_state"],
        "verbose": ["verbose"],
    }

    @abstractmethod
    def __init__(
        self,
        estimator=None,
        cv=5,
        *,
        n_jobs=None,
        verbose=0,
    ):
        self.cv: _BaseKFold = check_cv(cv, classifier=is_classifier(estimator))
        super().__init__(
            estimator=estimator,
            n_estimators=self.cv.n_splits,
        )
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.estimators_ = []
        self.estimators_samples_ = []

    @_fit_context(
        # BaseBagging.estimator is not validated yet
        prefer_skip_nested_validation=False
    )
    def fit(self, X, y, sample_weight=None):
        """Build a Bagging ensemble of estimators from the training set (X, y).

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only if
            they are supported by the base estimator.

        y : array-like of shape (n_samples,)
            The target values (class labels in classification, real numbers in
            regression).

        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted.
            Note that this is supported only if the base estimator supports
            sample weighting.
        """
        # Convert data (X is required to be 2d and indexable)
        X, y = self._validate_data(
            X,
            y,
            accept_sparse=["csr", "csc"],
            dtype=None,
            force_all_finite=False,
            multi_output=True,
        )
        return self._fit(X, y, sample_weight=sample_weight)

    # noinspection PyMethodMayBeStatic
    def _parallel_args(self):
        return {}

    def _fit(
        self,
        X,
        y,
        max_depth=None,
        sample_weight=None,
        check_input=True,
    ):
        """Build a Bagging ensemble of estimators from the training
           set (X, y).

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only if
            they are supported by the base estimator.

        y : array-like of shape (n_samples,)
            The target values (class labels in classification, real numbers in
            regression).

        max_depth : int, default=None
            Override value used when constructing base estimator. Only
            supported if the base estimator has a max_depth parameter.

        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted.
            Note that this is supported only if the base estimator supports
            sample weighting.

        check_input : bool, default=True
            Override value used when fitting base estimator. Only supported
            if the base estimator has a check_input parameter for fit function.
        """
        self._generate_fold_indices(X, y, None)
        if sample_weight is not None:
            sample_weight = _check_sample_weight(sample_weight, X, dtype=None)

        # Remap output
        n_samples = X.shape[0]
        self._n_samples = n_samples
        y = self._validate_y(y)

        # Check parameters
        self._validate_estimator()

        if max_depth is not None:
            self.estimator_.max_depth = max_depth

        # Parallel loop
        n_jobs, n_estimators, starts = _partition_estimators(
            self.n_estimators, self.n_jobs
        )
        total_n_estimators = sum(n_estimators)

        all_results = Parallel(
            n_jobs=n_jobs, verbose=self.verbose, **self._parallel_args()
        )(
            delayed(_parallel_build_estimators)(
                n_estimators[i],
                self,
                self.estimators_samples_[starts[i] : starts[i + 1]],
                X,
                y,
                sample_weight,
                total_n_estimators,
                verbose=self.verbose,
                check_input=check_input,
            )
            for i in range(n_jobs)
        )

        # Reduce
        self.estimators_ = list(
            itertools.chain.from_iterable(t[0] for t in all_results)
        )
        return self

    # noinspection PyMethodMayBeStatic
    def _validate_y(self, y):
        if len(y.shape) == 1 or y.shape[1] == 1:
            return column_or_1d(y, warn=True)
        return y

    def _generate_fold_indices(self, X, y, groups):
        check_is_fitted(self)
        for fold in self.cv.split(X, y, groups):
            self.estimators_samples_.append(fold[0])

    def set_params(self, **params):
        cv = params.pop("cv", None)
        if cv:
            self.cv = check_cv(cv, classifier=is_classifier(self.estimator))
        return super().set_params(**params)


class CrossBaggingClassifier(ClassifierMixin, BaseCrossBagging):
    """A cross-validation Bagging classifier.

    A Bagging classifier is an ensemble meta-estimator that fits base
    classifiers each on a fold of cross-validation generator

    Attributes
    ----------
    estimator_ : estimator
        The base estimator from which the ensemble is grown.

    n_features_in_ : int
        Number of features seen during :term:`fit`.

    feature_names_in_ : ndarray of shape (`n_features_in_`,)
        Names of features seen during :term:`fit`. Defined only when `X`
        has feature names that are all strings.

    estimators_ : list of estimators
        The collection of fitted base estimators.

    estimators_samples_ : list of arrays
        The subset of drawn samples (i.e., the in-bag samples) for each base
        estimator. Each subset is defined by an array of the indices selected.

    classes_ : ndarray of shape (n_classes,)
        The classes labels.

    n_classes_ : int or list
        The number of classes.

    Examples
    --------
    >>> from sklearn.svm import SVC
    >>> from crossense.ensemble import CrossBaggingClassifier
    >>> from sklearn.datasets import make_classification
    >>> X, y = make_classification(n_samples=100, n_features=4,
    ...                            n_informative=2, n_redundant=0,
    ...                            random_state=0, shuffle=False)
    >>> clf = CrossBaggingClassifier(estimator=SVC(), cv=5).fit(X, y)
    >>> clf.predict([[0, 0, 0, 0]])
    array([1])
    """

    def __init__(
        self,
        estimator: object = None,
        cv: Union[int, BaseCrossValidator, Iterable] = 5,
        *,
        n_jobs: Optional[int] = None,
        verbose=0,
    ):
        """
        Parameters
        ----------
        estimator:
            The base estimator to fit on random subsets of the dataset.
            If None, then the base estimator is a
            :class:`~sklearn.tree.DecisionTreeClassifier`.

        cv:
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are:

            - `None`, to use the default 5-fold cross validation,
            - int, to specify the number of folds in a `(Stratified)KFold`,
            - :term:`CV splitter`,
            - An iterable that generates (train, test) splits as arrays of indices.

            For `int`/`None` inputs, if the estimator is a classifier and `y` is
            either binary or multiclass, :class:`StratifiedKFold` is used. In all
            other cases, :class:`KFold` is used. These splitters are instantiated
            with `shuffle=False` so the splits will be the same across calls.

            Refer :ref:`User Guide <cross_validation>` for the various
            cross-validation strategies that can be used here.

        n_jobs:
            The number of jobs to run in parallel for both :meth:`fit` and
            :meth:`predict`. ``None`` means 1 unless in a
            :obj:`joblib.parallel_backend` context. ``-1`` means using all
            processors. See :term:`Glossary <n_jobs>` for more details.

        verbose:
            Controls the verbosity when fitting and predicting.
        """
        super().__init__(
            estimator=estimator,
            cv=cv,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    def _validate_estimator(self, default=None):
        """Check the estimator and set the estimator_ attribute."""
        super()._validate_estimator(default=DecisionTreeClassifier())

    def _validate_y(self, y):
        y = column_or_1d(y, warn=True)
        check_classification_targets(y)
        self.classes_, y = np.unique(y, return_inverse=True)
        self.n_classes_ = len(self.classes_)

        return y

    def predict_all_proba(self, X):
        """Predict class probabilities of all models for X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only if
            they are supported by the base estimator.

        Returns
        -------
        p : ndarray of shape (n_estimators, n_samples, n_classes)
            The class probabilities of the input samples. The order of the
            classes corresponds to that in the attribute :term:`classes_`.
        """
        check_is_fitted(self)
        # Check data
        X = self._validate_data(
            X,
            accept_sparse=["csr", "csc"],
            dtype=None,
            force_all_finite=False,
            reset=False,
        )

        # Parallel loop
        n_jobs, _, starts = _partition_estimators(self.n_estimators, self.n_jobs)

        all_proba = Parallel(
            n_jobs=n_jobs, verbose=self.verbose, **self._parallel_args()
        )(
            delayed(_parallel_predict_proba)(
                self.estimators_[starts[i] : starts[i + 1]],
                X,
                self.n_classes_,
            )
            for i in range(n_jobs)
        )
        all_proba = list(itertools.chain.from_iterable(all_proba))
        return np.concatenate([x[np.newaxis, :, :] for x in all_proba], axis=0)

    def predict(self, X):
        """Predict class for X.

        The predicted class of an input sample is computed as the class with
        the highest mean predicted probability. If base estimators do not
        implement a ``predict_proba`` method, then it resorts to voting.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only if
            they are supported by the base estimator.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            The predicted classes.
        """
        predicted_probabilitiy = self.predict_proba(X)
        return self.classes_.take((np.argmax(predicted_probabilitiy, axis=1)), axis=0)

    def predict_proba(self, X):
        """Predict class probabilities for X.

        The predicted class probabilities of an input sample is computed as
        the mean predicted class probabilities of the base estimators in the
        ensemble. If base estimators do not implement a ``predict_proba``
        method, then it resorts to voting and the predicted class probabilities
        of an input sample represents the proportion of estimators predicting
        each class.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only if
            they are supported by the base estimator.

        Returns
        -------
        p : ndarray of shape (n_samples, n_classes)
            The class probabilities of the input samples. The order of the
            classes corresponds to that in the attribute :term:`classes_`.
        """
        all_proba = self.predict_all_proba(X)
        # Reduce
        proba = all_proba.mean(axis=0)

        return proba

    def predict_log_proba(self, X):
        """Predict class log-probabilities for X.

        The predicted class log-probabilities of an input sample is computed as
        the log of the mean predicted class probabilities of the base
        estimators in the ensemble.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only if
            they are supported by the base estimator.

        Returns
        -------
        p : ndarray of shape (n_samples, n_classes)
            The class log-probabilities of the input samples. The order of the
            classes corresponds to that in the attribute :term:`classes_`.
        """
        check_is_fitted(self)
        if hasattr(self.estimator_, "predict_log_proba"):
            # Check data
            X = self._validate_data(
                X,
                accept_sparse=["csr", "csc"],
                dtype=None,
                force_all_finite=False,
                reset=False,
            )

            # Parallel loop
            n_jobs, _, starts = _partition_estimators(self.n_estimators, self.n_jobs)

            all_log_proba = Parallel(n_jobs=n_jobs, verbose=self.verbose)(
                delayed(_parallel_predict_log_proba)(
                    self.estimators_[starts[i] : starts[i + 1]],
                    X,
                    self.n_classes_,
                )
                for i in range(n_jobs)
            )

            # Reduce
            log_proba = all_log_proba[0]

            for j in range(1, len(all_log_proba)):
                log_proba = np.logaddexp(log_proba, all_log_proba[j])

            log_proba -= np.log(self.n_estimators)

        else:
            log_proba = np.log(self.predict_proba(X))

        return log_proba

    @available_if(_estimator_has("decision_function"))
    def decision_function(self, X):
        """Average of the decision functions of the base classifiers.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only if
            they are supported by the base estimator.

        Returns
        -------
        score : ndarray of shape (n_samples, k)
            The decision function of the input samples. The columns correspond
            to the classes in sorted order, as they appear in the attribute
            ``classes_``. Regression and binary classification are special
            cases with ``k == 1``, otherwise ``k==n_classes``.
        """
        # noinspection DuplicatedCode
        check_is_fitted(self)

        # Check data
        X = self._validate_data(
            X,
            accept_sparse=["csr", "csc"],
            dtype=None,
            force_all_finite=False,
            reset=False,
        )

        # Parallel loop
        n_jobs, _, starts = _partition_estimators(self.n_estimators, self.n_jobs)

        all_decisions = Parallel(n_jobs=n_jobs, verbose=self.verbose)(
            delayed(_parallel_decision_function)(
                self.estimators_[starts[i] : starts[i + 1]],
                X,
            )
            for i in range(n_jobs)
        )

        # Reduce
        decisions = sum(all_decisions) / self.n_estimators

        return decisions

    def _more_tags(self):
        if self.estimator is None:
            estimator = DecisionTreeClassifier()
        else:
            estimator = self.estimator

        return {"allow_nan": _safe_tags(estimator, "allow_nan")}


class CrossBaggingRegressor(RegressorMixin, BaseCrossBagging):
    """A cross-validation Bagging regressor.

    A Bagging regressor is an ensemble meta-estimator that fits base
    regressors each on a fold of cross-validation generator

    Attributes
    ----------
    estimator_ : estimator
        The base estimator from which the ensemble is grown.

    n_features_in_ : int
        Number of features seen during :term:`fit`.

    feature_names_in_ : ndarray of shape (`n_features_in_`,)
        Names of features seen during :term:`fit`. Defined only when `X`
        has feature names that are all strings.

    estimators_ : list of estimators
        The collection of fitted sub-estimators.

    estimators_samples_ : list of arrays
        The subset of drawn samples (i.e., the in-bag samples) for each base
        estimator. Each subset is defined by an array of the indices selected.

    Examples
    --------
    >>> from sklearn.svm import SVR
    >>> from crossense.ensemble import CrossBaggingRegressor
    >>> from sklearn.datasets import make_regression
    >>> X, y = make_regression(n_samples=100, n_features=4,
    ...                        n_informative=2, n_targets=1,
    ...                        random_state=0, shuffle=False)
    >>> regr = CrossBaggingRegressor(estimator=SVR(), cv=5).fit(X, y)
    >>> regr.predict([[0, 0, 0, 0]])
    array([-2.8720...])
    """

    def __init__(
        self,
        estimator: object = None,
        cv: Union[int, BaseCrossValidator, Iterable] = 5,
        *,
        n_jobs: Optional[int] = None,
        verbose=0,
    ):
        """
        Parameters
        ----------
        estimator:
            The base estimator to fit on random subsets of the dataset.
            If None, then the base estimator is a
            :class:`~sklearn.tree.DecisionTreeClassifier`.

        cv:
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are:

            - `None`, to use the default 5-fold cross validation,
            - int, to specify the number of folds in a `(Stratified)KFold`,
            - :term:`CV splitter`,
            - An iterable that generates (train, test) splits as arrays of indices.

            For `int`/`None` inputs, if the estimator is a classifier and `y` is
            either binary or multiclass, :class:`StratifiedKFold` is used. In all
            other cases, :class:`KFold` is used. These splitters are instantiated
            with `shuffle=False` so the splits will be the same across calls.

            Refer :ref:`User Guide <cross_validation>` for the various
            cross-validation strategies that can be used here.

        n_jobs:
            The number of jobs to run in parallel for both :meth:`fit` and
            :meth:`predict`. ``None`` means 1 unless in a
            :obj:`joblib.parallel_backend` context. ``-1`` means using all
            processors. See :term:`Glossary <n_jobs>` for more details.

        verbose:
            Controls the verbosity when fitting and predicting.
        """
        super().__init__(
            estimator=estimator,
            cv=cv,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    def predict_all(self, X):
        """Predict regression target of all models for X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only if
            they are supported by the base estimator.

        Returns
        -------
        p : ndarray of shape (n_estimators, n_samples, )
            The predicted values.
        """
        # noinspection DuplicatedCode
        check_is_fitted(self)
        # Check data
        X = self._validate_data(
            X,
            accept_sparse=["csr", "csc"],
            dtype=None,
            force_all_finite=False,
            reset=False,
        )

        # Parallel loop
        n_jobs, _, starts = _partition_estimators(self.n_estimators, self.n_jobs)

        all_y_hat = Parallel(n_jobs=n_jobs, verbose=self.verbose)(
            delayed(_parallel_predict_regression)(
                self.estimators_[starts[i] : starts[i + 1]],
                X,
            )
            for i in range(n_jobs)
        )
        all_y_hat = list(itertools.chain.from_iterable(all_y_hat))
        return np.concatenate([x[np.newaxis, :] for x in all_y_hat], axis=0)

    def predict(self, X):
        """Predict regression target for X.

        The predicted regression target of an input sample is computed as the
        mean predicted regression targets of the estimators in the ensemble.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only if
            they are supported by the base estimator.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            The predicted values.
        """
        all_y_hat = self.predict_all(X)
        # Reduce
        y_hat = sum(all_y_hat) / self.n_estimators

        return y_hat

    # noinspection PyMethodOverriding
    def _validate_estimator(self):
        """Check the estimator and set the estimator_ attribute."""
        super()._validate_estimator(default=DecisionTreeRegressor())

    def _more_tags(self):
        if self.estimator is None:
            estimator = DecisionTreeRegressor()
        else:
            estimator = self.estimator
        return {"allow_nan": _safe_tags(estimator, "allow_nan")}
