# OutlierIdentifiers

## In brief

This a Python package for 1D outlier identifier functions. 
If follows closely the Wolfram Language (WL) paclet [AAp1], the R package [AAp2], and the Raku package [AAp3].

Here is a Jupyter notebook with usage examples: ["OutlierIdentifiers-guide.ipynb"](https://github.com/antononcube/Python-packages/blob/main/OutlierIdentifiers/docs/OutlierIdentifiers-guide.ipynb);
[(Markdown version)](https://github.com/antononcube/Python-packages/blob/main/OutlierIdentifiers/docs/OutlierIdentifiers-guide.md).

------

## Installation 

From PyPI.org:

```shell
python3 -m pip install OutlierIdentifiers
```

From GitHub:

```shell
python3 -m pip install git+https://github.com/antononcube/Python-packages.git#egg=OutlierIdentifiers\&subdirectory=OutlierIdentifiers
```

------

## Usage examples

Load packages:


```python
import numpy as np
import plotly.graph_objects as go

from OutlierIdentifiers import *
```

Generate a vector with random numbers:


```python
np.random.seed(14)
vec = np.random.normal(loc=10, scale=20, size=30)
print(vec)
```

    [ 41.02678223  11.58372049  13.47953057   8.55326868 -30.086588
      12.89355626 -20.02337245  14.22218902  -1.16410111  31.6905813
       6.27421752  10.2932275  -11.51138939  22.84504148   6.39326577
      22.40600507  26.21948669  25.55871733   5.25020644 -27.83824691
     -13.44243588  26.72413943  30.18546801  35.86198722  -0.98662331
      -9.6342573   28.29345516  27.46140757  10.44222283   9.91712833]


Plot the vector:


```python
# Create a scatter plot with markers
fig = go.Figure(data=go.Scatter(y=vec, mode='markers'))

# Add labels and title
fig.update_layout(title='Vector of Numbers', xaxis_title='Index', yaxis_title='Value', template = "plotly_dark")

# Display the plot
fig.show()

```



Find outlier positions:


```python
outlier_identifier(vec, identifier=hampel_identifier_parameters)
```




    array([ True, False, False, False,  True, False,  True, False, False,
            True, False, False,  True, False, False, False, False, False,
           False,  True,  True, False, False,  True, False,  True, False,
           False, False, False])



Find outlier values:


```python
outlier_identifier(vec, identifier=hampel_identifier_parameters, value = True)
```




    array([ 41.02678223, -30.086588  , -20.02337245,  31.6905813 ,
           -11.51138939, -27.83824691, -13.44243588,  35.86198722,
            -9.6342573 ])



Find *top* outlier positions and values:


```python
outlier_identifier(vec, identifier = lambda v: top_outliers(hampel_identifier_parameters(v)))
```




    array([ True, False, False, False, False, False, False, False, False,
            True, False, False, False, False, False, False, False, False,
           False, False, False, False, False,  True, False, False, False,
           False, False, False])




```python
outlier_identifier(vec, identifier = lambda v: top_outliers(hampel_identifier_parameters(v)), value=True)
```




    array([41.02678223, 31.6905813 , 35.86198722])



Find *bottom* outlier positions and values (using quartiles-based identifier):


```python
outlier_identifier(vec, identifier = lambda v: bottom_outliers(quartile_identifier_parameters(v)))
```




    array([False, False, False, False,  True, False,  True, False, False,
           False, False, False, False, False, False, False, False, False,
           False,  True, False, False, False, False, False, False, False,
           False, False, False])




```python
outlier_identifier(vec, identifier = lambda v: bottom_outliers(quartile_identifier_parameters(v)), value=True)
```




    array([-30.086588  , -20.02337245, -27.83824691])


Here is another way to get the outlier values:


```python
vec[pred]
```



    array([-30.086588  , -20.02337245, -27.83824691])



The available outlier parameters functions are:

- `hampel_identifier_parameters`
- `splus_quartile_identifier_parameters`
- `quartile_identifier_parameters`


```python
[ f(vec) for f in (hampel_identifier_parameters, splus_quartile_identifier_parameters, quartile_identifier_parameters)]
```




    [(-8.796653643076334, 30.822596969354976),
     (-37.649981209714, 64.27685968784428),
     (-14.46873856125025, 36.49468188752889)]



------

## References 

[AA1] Anton Antonov,
["Outlier detection in a list of numbers"](https://mathematicaforprediction.wordpress.com/2013/10/16/outlier-detection-in-a-list-of-numbers/),
(2013),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

[AAp1] Anton Antonov,
[OutlierIdentifiers WL paclet](https://resources.wolframcloud.com/PacletRepository/resources/AntonAntonov/OutlierIdentifiers/),
(2023),
[Wolfram Language Paclet Repository](https://resources.wolframcloud.com/PacletRepository/).

[AAp2] Anton Antonov,
[OutlierIdentifiers R package](https://github.com/antononcube/R-packages/tree/master/OutlierIdentifiers),
(2019),
[R-packages at GitHub/antononcube](https://github.com/antononcube/R-packages).

[AAp3] Anton Antonov,
[OutlierIdentifiers Raku package](https://github.com/antononcube/Raku-Statistics-OutlierIdentifiers),
(2022),
[GitHub/antononcube](https://github.com/antononcube/).
