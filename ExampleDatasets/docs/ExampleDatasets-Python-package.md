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

Here we summarize the dataset obtained above:

```python
tbl.describe()
```

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

Here we get a dataset through 
[`pandas`](https://pandas.pydata.org)
by using an URL and display the head of the obtained dataset:

```python
import pandas
url = 'https://raw.githubusercontent.com/antononcube/Raku-Data-Reshapers/main/resources/dfTitanic.csv'
tbl2 = pandas.read_csv(url)
tbl2.head()
```


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

```python
import time
startTime = time.time()
data = example_dataset(itemSpec = 'titanic', packageSpec = 'COUNT', keep = True)
endTime = time.time()
print("Geting the data second time took " + str( endTime - startTime ) + " seconds")
```

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
