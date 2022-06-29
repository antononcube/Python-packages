# ROCFunctions

This repository has the code of a Python package for
[Receiver Operating Characteristic (ROC)](https://en.wikipedia.org/wiki/Receiver_operating_characteristic)
functions.

The ROC framework is used for analysis and tuning of binary classifiers, [Wk1].
(The classifiers are assumed to classify into a positive/true label or a negative/false label. )

For computational introduction to ROC utilization (in Mathematica) see the article
["Basic example of using ROC with Linear regression"](https://mathematicaforprediction.wordpress.com/2016/10/12/basic-example-of-using-roc-with-linear-regression/)
,
[AA1].

The examples below use the package
["RandomDataGenerators"](https://pypi.org/project/RandomDataGenerators/),
[AA2].

-------

## Installation

From PyPI.org:

```shell
python3 -m pip install ROCFunctions
```

------

## Usage examples

### Properties

Here are some retrieval functions:

```python
import ROCFunctions

print(roc_functions("properties"))
```

```python
print(roc_functions("FunctionInterpretations"))
```

```python
print(roc_functions("FPR"))
```

### Single ROC record

**Definition:** A ROC record (ROC-dictionary, or ROC-hash, or ROC-hash-map) is an associative object that has the keys:
"FalseNegative", "FalsePositive", "TrueNegative", "TruePositive". Here is an example:

```python
{"FalseNegative": 50, "FalsePositive": 51, "TrueNegative": 60, "TruePositive": 39}
```

Here we generate a random "dataset" with columns "Actual" and "Predicted" that have the values "true" and "false"
and show the summary:

```python
import RandomDataGenerators

dfRandomLabels = random_data_frame(200, ["Actual", "Predicted"],
                                   generators={"Actual": ["true", "false"],
                                               "Predicted": ["true", "false"]})
```

Here is a sample of the dataset:

```python
print(dfRandomLabels[:4])
```

-------

## References

### Articles

[Wk1] Wikipedia
entry, ["Receiver operating characteristic"](https://en.wikipedia.org/wiki/Receiver_operating_characteristic).

[AA1] Anton Antonov,
["Basic example of using ROC with Linear regression"](https://mathematicaforprediction.wordpress.com/2016/10/12/basic-example-of-using-roc-with-linear-regression/)
,
(2016),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

[AA2] Anton Antonov,
["Introduction to data wrangling with Raku"](https://rakuforprediction.wordpress.com/2021/12/31/introduction-to-data-wrangling-with-raku/)
,
(2021),
[RakuForPrediction at WordPress](https://rakuforprediction.wordpress.com).

### Packages

[AAp1] Anton Antonov,
[ROCFunctions Mathematica package](https://github.com/antononcube/MathematicaForPrediction/blob/master/ROCFunctions.m),
(2016-2022),
[MathematicaForPrediction at GitHub/antononcube](https://github.com/antononcube/MathematicaForPrediction/).

[AAp2] Anton Antonov,
[ROCFunctions R package](https://github.com/antononcube/R-packages/tree/master/ROCFunctions),
(2021),
[R-packages at GitHub/antononcube](https://github.com/antononcube/R-packages).

[AAp3] Anton Antonov,
[ML::ROCFunctions Raku package](https://github.com/antononcube/Raku-ML-ROCFunctions),
(2022),
[GitHub/antononcube](https://github.com/antononcube).