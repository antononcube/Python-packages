# DataTypeSystem

This Python package provides a type system for different data structures that are 
coercible to full arrays. It is Python translation of the code of the Raku package
["Data::TypeSystem"](https://raku.land/zef:antononcube/Data::TypeSystem), [AAp1].

------

## Installation

### Install from GitHub

```shell
pip install -e git+https://github.com/antononcube/Python-packages.git#egg=DataTypeSystem-antononcube\&subdirectory=DataTypeSystem
```

### From PyPi

```shell
pip install DataTypeSystem
```

------

## Usage examples

The type system conventions follow those of Mathematica's 
[`Dataset`](https://reference.wolfram.com/language/ref/Dataset.html) 
-- see the presentation 
["Dataset improvements"](https://www.wolfram.com/broadcast/video.php?c=488&p=4&disp=list&v=3264).

Here we get the Titanic dataset, change the "passengerAge" column values to be numeric, 
and show dataset's dimensions:


```python
import pandas

dfTitanic = pandas.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv')
dfTitanic = dfTitanic[["sex", "age", "pclass", "survived"]]
dfTitanic = dfTitanic.rename(columns ={"pclass": "class"})
dfTitanic.shape
```




    (891, 4)



Here is a sample of dataset's records:


```python
from DataTypeSystem import *

dfTitanic.sample(3)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sex</th>
      <th>age</th>
      <th>class</th>
      <th>survived</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>555</th>
      <td>male</td>
      <td>62.0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>278</th>
      <td>male</td>
      <td>7.0</td>
      <td>3</td>
      <td>0</td>
    </tr>
    <tr>
      <th>266</th>
      <td>male</td>
      <td>16.0</td>
      <td>3</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



Here is the type of a single record:


```python
deduce_type(dfTitanic.iloc[12].to_dict())
```




    Struct([age, class, sex, survived], [float, int, str, int])



Here is the type of single record's values:


```python
deduce_type(dfTitanic.iloc[12].to_dict().values())
```




    Tuple([Atom(<class 'str'>), Atom(<class 'float'>), Atom(<class 'int'>), Atom(<class 'int'>)])



Here is the type of the whole dataset:


```python
deduce_type(dfTitanic.to_dict())
```




    Assoc(Atom(<class 'str'>), Assoc(Atom(<class 'int'>), Atom(<class 'str'>), 891), 4)



Here is the type of "values only" records:


```python
valArr = dfTitanic.transpose().to_dict().values()
deduce_type(valArr)
```




    Vector(Struct([age, class, sex, survived], [float, int, str, int]), 891)



-------

## References

[AAp1] Anton Antonov,
[Data::TypeSystem Raku package](https://github.com/antononcube/Raku-Data-TypeSystem),
(2023),
[GitHub/antononcube](https://github.com/antononcube/).
