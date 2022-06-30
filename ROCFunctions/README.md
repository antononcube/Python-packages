# ROCFunctions basic usage

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
import pandas
from ROCFunctions import *
print(roc_functions("properties"))
```

    ['FunctionInterpretations', 'FunctionNames', 'Functions', 'Methods', 'Properties']



```python
print(roc_functions("FunctionInterpretations"))
```

    {'TPR': 'true positive rate', 'TNR': 'true negative rate', 'SPC': 'specificity', 'PPV': 'positive predictive value', 'NPV': 'negative predictive value', 'FPR': 'false positive rate', 'FDR': 'false discovery rate', 'FNR': 'false negative rate', 'ACC': 'accuracy', 'AUROC': 'area under the ROC curve', 'FOR': 'false omission rate', 'F1': 'F1 score', 'MCC': 'Matthews correlation coefficient', 'Recall': 'same as TPR', 'Precision': 'same as PPV', 'Accuracy': 'same as ACC', 'Sensitivity': 'same as TPR'}



```python
print(roc_functions("FPR"))
```

    <function FPR at 0x7f7612f48050>


### Single ROC record

**Definition:** A
ROC record (ROC-dictionary, or ROC-hash, or ROC-hash-map) is an associative object that has the keys:
"FalseNegative", "FalsePositive", "TrueNegative", "TruePositive".Here is an example:


```python
{"FalseNegative": 50, "FalsePositive": 51, "TrueNegative": 60, "TruePositive": 39}
```




    {'FalseNegative': 50,
     'FalsePositive': 51,
     'TrueNegative': 60,
     'TruePositive': 39}



Here we generate a random "dataset" with columns "Actual" and "Predicted" that have the values
"true" and "false"and show the summary:


```python
from RandomDataGenerators import *

dfRandomLabels = random_data_frame(200, ["Actual", "Predicted"],
                                   generators={"Actual": ["true", "false"],
                                               "Predicted": ["true", "false"]})
dfRandomLabels.shape
```




    (200, 2)



Here is a sample of the dataset:



```python
print(dfRandomLabels[:4])
```

      Actual Predicted
    0  false     false
    1  false     false
    2  false     false
    3   true     false


Here we make the corresponding ROC dictionary:


```python
to_roc_dict('true', 'false',
            list(dfRandomLabels.Actual.values),
            list(dfRandomLabels.Predicted.values))
```




    {'TruePositive': 52,
     'FalsePositive': 48,
     'TrueNegative': 50,
     'FalseNegative': 50}



### Multiple ROC records

Here we make random dataset with entries that associated with a certain threshold parameter with three unique values:


```python
dfRandomLabels2 = random_data_frame(200, ["Threshold", "Actual", "Predicted"],
                                    generators={"Threshold": [0.2, 0.4, 0.6],
                                                "Actual": ["true", "false"],
                                                "Predicted": ["true", "false"]})
```

**Remark:** Threshold parameters are typically used while tuning Machine Learning (ML) classifiers. Here we find and print the ROC records(dictionaries) for each unique threshold value:



```python
thresholds = list(dfRandomLabels2.Threshold.drop_duplicates())

rocGroups = {}
for x in thresholds:
    dfLocal = dfRandomLabels2[dfRandomLabels2["Threshold"] == x]
    rocGroups[x] = to_roc_dict('true', 'false',
                        list(dfLocal.Actual.values),
                        list(dfLocal.Predicted.values))

rocGroups
```




    {0.4: {'TruePositive': 13,
      'FalsePositive': 23,
      'TrueNegative': 24,
      'FalseNegative': 12},
     0.2: {'TruePositive': 18,
      'FalsePositive': 11,
      'TrueNegative': 19,
      'FalseNegative': 18},
     0.6: {'TruePositive': 23,
      'FalsePositive': 9,
      'TrueNegative': 16,
      'FalseNegative': 14}}



### Application of ROC functions

Here we define a list of ROC functions:


```python
funcs = ["PPV", "NPV", "TPR", "ACC", "SPC", "MCC"]
```

Here we apply each ROC function to each of the ROC records obtained above:


```python
import pandas
rocRes = { k : {f: roc_functions(f)(v) for f in funcs} for (k, v) in rocGroups.items()}

print(pandas.DataFrame(rocRes))
```

              0.4       0.2       0.6
    PPV  0.361111  0.620690  0.718750
    NPV  0.666667  0.513514  0.533333
    TPR  0.520000  0.500000  0.621622
    ACC  0.513889  0.560606  0.629032
    SPC  0.510638  0.633333  0.640000
    MCC  0.030640  0.134535  0.261666



-------

## References

### Articles

[Wk1] Wikipedia entry,
["Receiver operating characteristic"](https://en.wikipedia.org/wiki/Receiver_operating_characteristic).

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
