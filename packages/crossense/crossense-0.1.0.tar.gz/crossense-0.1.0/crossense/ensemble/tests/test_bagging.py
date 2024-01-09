"""
Testing for the bagging ensemble module (crossense.ensemble.bagging).
"""

from itertools import cycle

import joblib
import numpy as np
import pytest
from sklearn.base import BaseEstimator
from sklearn.datasets import load_diabetes, load_iris, make_hastie_10_2
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
)

from crossense.ensemble import (
    CrossBaggingClassifier,
    CrossBaggingRegressor,
)
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.model_selection import GridSearchCV, ParameterGrid, train_test_split, KFold
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.random_projection import SparseRandomProjection
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.utils import check_random_state
from sklearn.utils._testing import assert_array_almost_equal, assert_array_equal

rng = check_random_state(0)

# also load the iris dataset
# and randomly permute it
iris = load_iris()
perm = rng.permutation(iris.target.size)
iris.data = iris.data[perm]
iris.target = iris.target[perm]

# also load the diabetes dataset
# and randomly permute it
diabetes = load_diabetes()
perm = rng.permutation(diabetes.target.size)
diabetes.data = diabetes.data[perm]
diabetes.target = diabetes.target[perm]


def test_classification():
    # Check classification for various parameter settings.
    rng = check_random_state(0)
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, random_state=rng
    )
    grid = ParameterGrid(
        {
            "cv": [2, 5],
        }
    )
    estimators = [
        None,
        DummyClassifier(),
        Perceptron(max_iter=20),
        DecisionTreeClassifier(max_depth=2),
        KNeighborsClassifier(),
        SVC(),
    ]
    # Try different parameter settings with different base classifiers without
    # doing the full cartesian product to keep the test durations low.
    for params, estimator in zip(grid, cycle(estimators)):
        CrossBaggingClassifier(
            estimator=estimator,
            **params,
        ).fit(
            X_train, y_train
        ).predict(X_test)


def test_regression():
    # Check regression for various parameter settings.
    rng = check_random_state(0)
    X_train, X_test, y_train, y_test = train_test_split(
        diabetes.data[:50], diabetes.target[:50], random_state=rng
    )
    grid = ParameterGrid(
        {
            "cv": [5, 10],
        }
    )

    for estimator in [
        None,
        DummyRegressor(),
        DecisionTreeRegressor(),
        KNeighborsRegressor(),
        SVR(),
    ]:
        for params in grid:
            CrossBaggingRegressor(estimator=estimator, **params).fit(
                X_train, y_train
            ).predict(X_test)


class DummySizeEstimator(BaseEstimator):
    def fit(self, X, y):
        self.training_size_ = X.shape[0]
        self.training_hash_ = joblib.hash(X)

    def predict(self, X):
        return np.ones(X.shape[0])


def test_probability():
    # Predict probabilities.
    rng = check_random_state(0)
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, random_state=rng
    )

    with np.errstate(divide="ignore", invalid="ignore"):
        # Normal case
        ensemble = CrossBaggingClassifier(estimator=DecisionTreeClassifier()).fit(
            X_train, y_train
        )

        assert_array_almost_equal(
            np.sum(ensemble.predict_proba(X_test), axis=1), np.ones(len(X_test))
        )

        assert_array_almost_equal(
            ensemble.predict_proba(X_test), np.exp(ensemble.predict_log_proba(X_test))
        )

        # Degenerate case, where some classes are missing
        ensemble = CrossBaggingClassifier(estimator=LogisticRegression()).fit(
            X_train, y_train
        )

        assert_array_almost_equal(
            np.sum(ensemble.predict_proba(X_test), axis=1), np.ones(len(X_test))
        )

        assert_array_almost_equal(
            ensemble.predict_proba(X_test), np.exp(ensemble.predict_log_proba(X_test))
        )


def test_error():
    # Test support of decision_function
    X, y = iris.data, iris.target
    base = DecisionTreeClassifier()
    assert not hasattr(CrossBaggingClassifier(base).fit(X, y), "decision_function")


def test_parallel_classification():
    # Check parallel classification.
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, random_state=0
    )
    cv = KFold(n_splits=5)
    ensemble = CrossBaggingClassifier(
        DecisionTreeClassifier(random_state=0), cv=cv, n_jobs=3
    ).fit(X_train, y_train)

    # predict_proba
    y1 = ensemble.predict_proba(X_test)
    ensemble.set_params(n_jobs=1)
    y2 = ensemble.predict_proba(X_test)
    assert_array_almost_equal(y1, y2)

    ensemble = CrossBaggingClassifier(
        DecisionTreeClassifier(random_state=0), cv=cv, n_jobs=1
    ).fit(X_train, y_train)

    y3 = ensemble.predict_proba(X_test)
    assert_array_almost_equal(y1, y3)

    # decision_function
    ensemble = CrossBaggingClassifier(
        SVC(decision_function_shape="ovr", random_state=0), cv=cv, n_jobs=3
    ).fit(X_train, y_train)

    decisions1 = ensemble.decision_function(X_test)
    ensemble.set_params(n_jobs=1)
    decisions2 = ensemble.decision_function(X_test)
    assert_array_almost_equal(decisions1, decisions2)

    ensemble = CrossBaggingClassifier(
        SVC(decision_function_shape="ovr", random_state=0), n_jobs=1
    ).fit(X_train, y_train)

    decisions3 = ensemble.decision_function(X_test)
    assert_array_almost_equal(decisions1, decisions3)


def test_parallel_regression():
    # Check parallel regression.
    rng = check_random_state(0)
    cv = KFold(10)
    X_train, X_test, y_train, y_test = train_test_split(
        diabetes.data, diabetes.target, random_state=rng
    )

    ensemble = CrossBaggingRegressor(
        DecisionTreeRegressor(random_state=0), cv=cv, n_jobs=3
    ).fit(X_train, y_train)

    ensemble.set_params(n_jobs=1)
    y1 = ensemble.predict(X_test)
    ensemble.set_params(n_jobs=2)
    y2 = ensemble.predict(X_test)
    assert_array_almost_equal(y1, y2)

    ensemble = CrossBaggingRegressor(
        DecisionTreeRegressor(random_state=0), cv=cv, n_jobs=1
    ).fit(X_train, y_train)

    y3 = ensemble.predict(X_test)
    assert_array_almost_equal(y1, y3)


def test_gridsearch():
    # Check that bagging ensembles can be grid-searched.
    # Transform iris into a binary classification task
    X, y = iris.data, iris.target
    y[y == 2] = 1

    # Grid search with scoring based on decision_function
    parameters = {"cv": (2, 3, 4, 5)}

    GridSearchCV(CrossBaggingClassifier(SVC()), parameters, scoring="roc_auc").fit(X, y)


def test_estimator():
    # Check estimator and its default values.
    rng = check_random_state(0)

    # Classification
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, random_state=rng
    )

    ensemble = CrossBaggingClassifier(None, n_jobs=3).fit(X_train, y_train)

    assert isinstance(ensemble.estimator_, DecisionTreeClassifier)

    ensemble = CrossBaggingClassifier(DecisionTreeClassifier(), n_jobs=3).fit(
        X_train, y_train
    )

    assert isinstance(ensemble.estimator_, DecisionTreeClassifier)

    ensemble = CrossBaggingClassifier(Perceptron(), n_jobs=3).fit(X_train, y_train)

    assert isinstance(ensemble.estimator_, Perceptron)

    # Regression
    X_train, X_test, y_train, y_test = train_test_split(
        diabetes.data, diabetes.target, random_state=rng
    )

    ensemble = CrossBaggingRegressor(None, n_jobs=3).fit(X_train, y_train)

    assert isinstance(ensemble.estimator_, DecisionTreeRegressor)

    ensemble = CrossBaggingRegressor(DecisionTreeRegressor(), n_jobs=3).fit(
        X_train, y_train
    )

    assert isinstance(ensemble.estimator_, DecisionTreeRegressor)

    ensemble = CrossBaggingRegressor(SVR(), n_jobs=3).fit(X_train, y_train)
    assert isinstance(ensemble.estimator_, SVR)


def test_bagging_with_pipeline():
    estimator = CrossBaggingClassifier(
        make_pipeline(SelectKBest(k=1), DecisionTreeClassifier(random_state=0))
    )
    estimator.fit(iris.data, iris.target)
    assert isinstance(estimator[0].steps[-1][1].random_state, int)


class DummyZeroEstimator(BaseEstimator):
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        return self

    def predict(self, X):
        return self.classes_[np.zeros(X.shape[0], dtype=int)]


def test_bagging_sample_weight_unsupported_but_passed():
    estimator = CrossBaggingClassifier(DummyZeroEstimator())
    rng = check_random_state(0)

    estimator.fit(iris.data, iris.target).predict(iris.data)
    with pytest.raises(ValueError):
        estimator.fit(
            iris.data,
            iris.target,
            sample_weight=rng.randint(10, size=(iris.data.shape[0])),
        )


def test_estimators_samples():
    # Check that format of estimators_samples_ is correct and that results
    # generated at fit time can be identically reproduced at a later time
    # using data saved in object attributes.
    X, y = make_hastie_10_2(n_samples=200, random_state=1)
    bagging = CrossBaggingClassifier(
        LogisticRegression(),
    )
    bagging.fit(X, y)

    # Get relevant attributes
    estimators_samples = bagging.estimators_samples_
    estimators = bagging.estimators_

    # Test for correct formatting
    assert len(estimators_samples) == len(estimators)
    assert len(estimators_samples[0]) == len(X) // 5 * 4
    assert estimators_samples[0].dtype.kind == "i"

    # Re-fit single estimator to test for consistent sampling
    estimator_index = 0
    estimator_samples = estimators_samples[estimator_index]
    estimator = estimators[estimator_index]

    X_train = X[estimator_samples]
    y_train = y[estimator_samples]

    orig_coefs = estimator.coef_
    estimator.fit(X_train, y_train)
    new_coefs = estimator.coef_

    assert_array_almost_equal(orig_coefs, new_coefs)


def test_estimators_samples_deterministic():
    # This test is a regression test to check that with a random step
    # (e.g. SparseRandomProjection) and a given random state, the results
    # generated at fit time can be identically reproduced at a later time using
    # data saved in object attributes. Check issue #9524 for full discussion.

    iris = load_iris()
    X, y = iris.data, iris.target

    base_pipeline = make_pipeline(
        SparseRandomProjection(n_components=2, random_state=0),
        LogisticRegression(random_state=0),
    )
    cv = KFold(5)
    clf = CrossBaggingClassifier(estimator=base_pipeline, cv=cv)
    clf.fit(X, y)
    pipeline_estimator_coef = clf.estimators_[0].steps[-1][1].coef_.copy()

    estimator = clf.estimators_[0]
    estimator_sample = clf.estimators_samples_[0]

    X_train = X[estimator_sample]
    y_train = y[estimator_sample]

    estimator.fit(X_train, y_train)
    assert_array_equal(estimator.steps[-1][1].coef_, pipeline_estimator_coef)


def replace(X):
    X = X.astype("float", copy=True)
    X[~np.isfinite(X)] = 0
    return X


def test_bagging_regressor_with_missing_inputs():
    # Check that BaggingRegressor can accept X with missing/infinite data
    X = np.array(
        [
            [1, 3, 5],
            [2, None, 6],
            [2, np.nan, 6],
            [2, np.inf, 6],
            [2, -np.inf, 6],
        ]
    )
    y_values = [
        np.array([2, 3, 3, 3, 3]),
        np.array(
            [
                [2, 1, 9],
                [3, 6, 8],
                [3, 6, 8],
                [3, 6, 8],
                [3, 6, 8],
            ]
        ),
    ]
    for y in y_values:
        regressor = DecisionTreeRegressor()
        pipeline = make_pipeline(FunctionTransformer(replace), regressor)
        pipeline.fit(X, y).predict(X)
        bagging_regressor = CrossBaggingRegressor(pipeline)
        y_hat = bagging_regressor.fit(X, y).predict(X)
        assert y.shape == y_hat.shape

        # Verify that exceptions can be raised by wrapper regressor
        regressor = DecisionTreeRegressor()
        pipeline = make_pipeline(regressor)
        with pytest.raises(ValueError):
            pipeline.fit(X, y)
        bagging_regressor = CrossBaggingRegressor(pipeline)
        with pytest.raises(ValueError):
            bagging_regressor.fit(X, y)


def test_bagging_get_estimators_indices():
    # Check that Bagging estimator can generate sample indices properly
    # Non-regression test for:
    # https://github.com/scikit-learn/scikit-learn/issues/16436

    rng = np.random.RandomState(0)
    X = rng.randn(13, 4)
    y = np.arange(13)

    class MyEstimator(DecisionTreeRegressor):
        """An estimator which stores y indices information at fit."""

        def fit(self, X, y):
            self._sample_indices = y

    clf = CrossBaggingRegressor(estimator=MyEstimator())
    clf.fit(X, y)

    assert_array_equal(clf.estimators_[0]._sample_indices, clf.estimators_samples_[0])


@pytest.mark.parametrize(
    "bagging, expected_allow_nan",
    [
        (CrossBaggingClassifier(HistGradientBoostingClassifier(max_iter=1)), True),
        (CrossBaggingRegressor(HistGradientBoostingRegressor(max_iter=1)), True),
        (CrossBaggingClassifier(LogisticRegression()), False),
        (CrossBaggingRegressor(SVR()), False),
    ],
)
def test_bagging_allow_nan_tag(bagging, expected_allow_nan):
    """Check that bagging inherits allow_nan tag."""
    assert bagging._get_tags()["allow_nan"] == expected_allow_nan
