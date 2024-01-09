# Crossense

Crossense is a collection of utilities designed to facilitate working with scikit-learn models, including training, Inferencing and benchmarking.

## Features
(to be written)

## Installation

You can install Crossense using pip:

```bash
pip install crossense
```

## Usage
``` python
from crossense.ensemble import CrossBaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedKFold

ds = load_iris()
clf = CrossBaggingClassifier(LogisticRegression(), cv=StratifiedKFold(5))
clf.fit(ds.data, ds.target)
```
For more detailed usage and examples, please refer to the [documentation](https://zeeonome.github.io/crossense).

## Contributing
If you'd like to contribute to Crossense, please follow the contribution guidelines (comming soon).

## License
This project is licensed under the MIT License - see the LICENSE file for details.
