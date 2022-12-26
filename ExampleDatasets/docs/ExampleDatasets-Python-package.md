# Example Datasets Python package

Python package for (obtaining) example datasets.

Currently, this repository contains only [datasets metadata](https://github.com/antononcube/Python-packages/raw/main/ExampleDatasets/ExampleDatasets/resources/dfRdatasets.csv.gz).
The datasets are downloaded from the repository 
[Rdatasets](https://github.com/vincentarelbundock/Rdatasets/),
[VAB1].

This package follows the design of the [Raku](https://raku.org) package with the same name; see [AAr1].

------

## Usage examples

### Setup

Here we load the Python packages `time`, `pandas`, and this package:


```python
from ExampleDatasets import *
import pandas
```

### Get a dataset by using an identifier

Here we get a dataset by using an identifier and display part of the obtained dataset:


```python
tbl = example_dataset(itemSpec = 'Baumann')
tbl.head
```




    <bound method NDFrame.head of     Unnamed: 0  group  pretest.1  pretest.2  post.test.1  post.test.2  \
    0            1  Basal          4          3            5            4   
    1            2  Basal          6          5            9            5   
    2            3  Basal          9          4            5            3   
    3            4  Basal         12          6            8            5   
    4            5  Basal         16          5           10            9   
    ..         ...    ...        ...        ...          ...          ...   
    61          62  Strat         11          4           11            7   
    62          63  Strat         14          4           15            7   
    63          64  Strat          8          2            9            5   
    64          65  Strat          5          3            6            8   
    65          66  Strat          8          3            4            6   
    
        post.test.3  
    0            41  
    1            41  
    2            43  
    3            46  
    4            46  
    ..          ...  
    61           48  
    62           49  
    63           33  
    64           45  
    65           42  
    
    [66 rows x 7 columns]>



Here we summarize the dataset obtained above:


```python
tbl.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>pretest.1</th>
      <th>pretest.2</th>
      <th>post.test.1</th>
      <th>post.test.2</th>
      <th>post.test.3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>66.000000</td>
      <td>66.000000</td>
      <td>66.000000</td>
      <td>66.000000</td>
      <td>66.000000</td>
      <td>66.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>33.500000</td>
      <td>9.787879</td>
      <td>5.106061</td>
      <td>8.075758</td>
      <td>6.712121</td>
      <td>44.015152</td>
    </tr>
    <tr>
      <th>std</th>
      <td>19.196354</td>
      <td>3.020520</td>
      <td>2.212752</td>
      <td>3.393707</td>
      <td>2.635644</td>
      <td>6.643661</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>4.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>30.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>17.250000</td>
      <td>8.000000</td>
      <td>3.250000</td>
      <td>5.000000</td>
      <td>5.000000</td>
      <td>40.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>33.500000</td>
      <td>9.000000</td>
      <td>5.000000</td>
      <td>8.000000</td>
      <td>6.000000</td>
      <td>45.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>49.750000</td>
      <td>12.000000</td>
      <td>6.000000</td>
      <td>11.000000</td>
      <td>8.000000</td>
      <td>49.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>66.000000</td>
      <td>16.000000</td>
      <td>13.000000</td>
      <td>15.000000</td>
      <td>13.000000</td>
      <td>57.000000</td>
    </tr>
  </tbody>
</table>
</div>



**Remark**: The values for the arguments `itemSpec` and `packageSpec` correspond to the values
of the columns "Item" and "Package", respectively, in the 
[metadata dataset](https://vincentarelbundock.github.io/Rdatasets/articles/data.html)
from the GitHub repository "Rdatasets", 
[[VAB1](https://github.com/vincentarelbundock/Rdatasets/)].
See the datasets metadata sub-section below.

### Get a dataset by using an URL

Here we can find URLs of datasets that have titles adhering to a regex:


```python
dfMeta = load_datasets_metadata()
print(dfMeta[dfMeta.Title.str.contains('^tita')][["Package", "Item", "CSV"]].to_string())
```

        Package        Item                                                                      CSV
    288   COUNT     titanic     https://vincentarelbundock.github.io/Rdatasets/csv/COUNT/titanic.csv
    289   COUNT  titanicgrp  https://vincentarelbundock.github.io/Rdatasets/csv/COUNT/titanicgrp.csv


Here we get a dataset through 
[`pandas`](https://pandas.pydata.org)
by using an URL and display the head of the obtained dataset:


```python
import pandas
url = 'https://raw.githubusercontent.com/antononcube/Raku-Data-Reshapers/main/resources/dfTitanic.csv'
tbl2 = pandas.read_csv(url)
tbl2.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>passengerClass</th>
      <th>passengerAge</th>
      <th>passengerSex</th>
      <th>passengerSurvival</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1st</td>
      <td>30</td>
      <td>female</td>
      <td>survived</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1st</td>
      <td>0</td>
      <td>male</td>
      <td>survived</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1st</td>
      <td>0</td>
      <td>female</td>
      <td>died</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1st</td>
      <td>30</td>
      <td>male</td>
      <td>died</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>1st</td>
      <td>20</td>
      <td>female</td>
      <td>died</td>
    </tr>
  </tbody>
</table>
</div>



### Datasets metadata

Here we:
1. Get the dataset of the datasets metadata
2. Filter it to have only datasets with 13 rows
3. Keep only the columns "Item", "Title", "Rows", and "Cols"
4. Display it 


```python
tblMeta = load_datasets_metadata()
tblMeta = tblMeta[["Item", "Title", "Rows", "Cols"]]
tblMeta = tblMeta[tblMeta["Rows"] == 13]
tblMeta
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item</th>
      <th>Title</th>
      <th>Rows</th>
      <th>Cols</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>805</th>
      <td>Snow.pumps</td>
      <td>John Snow's Map and Data on the 1854 London Ch...</td>
      <td>13</td>
      <td>4</td>
    </tr>
    <tr>
      <th>820</th>
      <td>BCG</td>
      <td>BCG Vaccine Data</td>
      <td>13</td>
      <td>7</td>
    </tr>
    <tr>
      <th>935</th>
      <td>cement</td>
      <td>Heat Evolved by Setting Cements</td>
      <td>13</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1354</th>
      <td>kootenay</td>
      <td>Waterflow Measurements of Kootenay River in Li...</td>
      <td>13</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1644</th>
      <td>Newhouse77</td>
      <td>Medical-Care Expenditure: A Cross-National Sur...</td>
      <td>13</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1735</th>
      <td>Saxony</td>
      <td>Families in Saxony</td>
      <td>13</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



### Keeping downloaded data

By default the data is obtained over the web from
[Rdatasets](https://github.com/vincentarelbundock/Rdatasets/),
but `example_dataset` has an option to keep the data "locally."
(The data is saved in `XDG_DATA_HOME`, see 
[SS1](https://pypi.org/project/xdg/).)

This can be demonstrated with the following timings of a dataset with ~1300 rows:


```python
import time
startTime = time.time()
data = example_dataset(itemSpec = 'titanic', packageSpec = 'COUNT', keep = True)
endTime = time.time()
print("Getting the data first time took " + str( endTime - startTime ) + " seconds")
```

    Getting the data first time took 0.003923892974853516 seconds



```python
import time
startTime = time.time()
data = example_dataset(itemSpec = 'titanic', packageSpec = 'COUNT', keep = True)
endTime = time.time()
print("Geting the data second time took " + str( endTime - startTime ) + " seconds")
```

    Geting the data second time took 0.003058910369873047 seconds


------

## References

### Functions, packages, repositories

[AAf1] Anton Antonov,
[`ExampleDataset`](https://resources.wolframcloud.com/FunctionRepository/resources/ExampleDataset),
(2020),
[Wolfram Function Repository](https://resources.wolframcloud.com/FunctionRepository).

[AAr1] Anton Antonov,
[`Data::ExampleDatasets Raku package`](https://github.com/antononcube/Raku-Data-ExampleDatasets),
(2021),
[GitHub/antononcube](https://github.com/antononcube).

[VAB1] Vincent Arel-Bundock,
[Rdatasets](https://github.com/vincentarelbundock/Rdatasets/),
(2020),
[GitHub/vincentarelbundock](https://github.com/vincentarelbundock).

[SS1] Scott Stevenson,
[xdg Python package](https://pypi.org/project/xdg/),
(2016-2021),
[PyPI.org](https://pypi.org/project/xdg/).

### Interactive interfaces

[AAi1] Anton Antonov,
[Example datasets recommender interface](https://antononcube.shinyapps.io/ExampleDatasetsRecommenderInterface/),
(2021),
[Shinyapps.io](https://antononcube.shinyapps.io/).
