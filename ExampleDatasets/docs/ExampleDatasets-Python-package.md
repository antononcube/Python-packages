Raku package for (obtaining) example datasets.

Currently, this repository contains only [datasets
metadata](./resources/dfRdatasets.csv). The datasets are downloaded from
the repository
[Rdatasets](https://github.com/vincentarelbundock/Rdatasets/), \[VAB1\].

This package follows the design of the [Raku](https://raku.org) package
with the same name; see \[AAr1\].

------------------------------------------------------------------------

## Usage examples

### Setup

Here we load the Raku modules
[`Data::Generators`](https://modules.raku.org/dist/Data::Generators:cpan:ANTONOV),
[`Data::Summarizers`](https://github.com/antononcube/Raku-Data-Summarizers),
and this module,
[`Data::ExampleDatasets`](https://github.com/antononcube/Raku-Data-ExampleDatasets):

    from ExampleDatasets import *
    import pandas

### Get a dataset by using an identifier

Here we get a dataset by using an identifier and display part of the
obtained dataset:

    tbl = example_dataset(itemSpec = 'Baumann')
    tbl.head

    ## <bound method NDFrame.head of     Unnamed: 0  group  pretest.1  ...  post.test.1  post.test.2  post.test.3
    ## 0            1  Basal          4  ...            5            4           41
    ## 1            2  Basal          6  ...            9            5           41
    ## 2            3  Basal          9  ...            5            3           43
    ## 3            4  Basal         12  ...            8            5           46
    ## 4            5  Basal         16  ...           10            9           46
    ## ..         ...    ...        ...  ...          ...          ...          ...
    ## 61          62  Strat         11  ...           11            7           48
    ## 62          63  Strat         14  ...           15            7           49
    ## 63          64  Strat          8  ...            9            5           33
    ## 64          65  Strat          5  ...            6            8           45
    ## 65          66  Strat          8  ...            4            6           42
    ## 
    ## [66 rows x 7 columns]>

Here we summarize the dataset obtained above:

    tbl.describe()

    ##        Unnamed: 0  pretest.1  pretest.2  post.test.1  post.test.2  post.test.3
    ## count   66.000000  66.000000  66.000000    66.000000    66.000000    66.000000
    ## mean    33.500000   9.787879   5.106061     8.075758     6.712121    44.015152
    ## std     19.196354   3.020520   2.212752     3.393707     2.635644     6.643661
    ## min      1.000000   4.000000   1.000000     1.000000     0.000000    30.000000
    ## 25%     17.250000   8.000000   3.250000     5.000000     5.000000    40.000000
    ## 50%     33.500000   9.000000   5.000000     8.000000     6.000000    45.000000
    ## 75%     49.750000  12.000000   6.000000    11.000000     8.000000    49.000000
    ## max     66.000000  16.000000  13.000000    15.000000    13.000000    57.000000

**Remark**: The values for the arguments `itemSpec` and `packageSpec`
correspond to the values of the columns “Item” and “Package”,
respectively, in the [metadata
dataset](https://vincentarelbundock.github.io/Rdatasets/articles/data.html)
from the GitHub repository “Rdatasets”,
\[[VAB1](https://github.com/vincentarelbundock/Rdatasets/)\]. See the
datasets metadata sub-section below.

### Get a dataset by using an URL

Here we can find URLs of datasets that have titles adhering to a regex:

    dfMeta = load_datasets_metadata()
    print(dfMeta[dfMeta.Title.str.contains('^tita')][["Package", "Item", "CSV"]].to_string())

    ##     Package        Item                                                                      CSV
    ## 288   COUNT     titanic     https://vincentarelbundock.github.io/Rdatasets/csv/COUNT/titanic.csv
    ## 289   COUNT  titanicgrp  https://vincentarelbundock.github.io/Rdatasets/csv/COUNT/titanicgrp.csv

Here we get a dataset through [`pandas`](https://pandas.pydata.org) by
using an URL and display the head of the obtained dataset:

    import pandas
    url = 'https://raw.githubusercontent.com/antononcube/Raku-Data-Reshapers/main/resources/dfTitanic.csv'
    tbl2 = pandas.read_csv(url)
    tbl2.head()

    ##    id passengerClass  passengerAge passengerSex passengerSurvival
    ## 0   1            1st            30       female          survived
    ## 1   2            1st             0         male          survived
    ## 2   3            1st             0       female              died
    ## 3   4            1st            30         male              died
    ## 4   5            1st            20       female              died

### Datasets metadata

Here we: 1. Get the dataset of the datasets metadata 2. Filter it to
have only datasets with 13 rows 3. Keep only the columns “Item”,
“Title”, “Rows”, and “Cols” 4. Display it

    tblMeta = load_datasets_metadata()
    tblMeta = tblMeta[["Item", "Title", "Rows", "Cols"]]
    tblMeta = tblMeta[tblMeta["Rows"] == 13]
    tblMeta

    ##             Item                                              Title  Rows  Cols
    ## 805   Snow.pumps  John Snow's Map and Data on the 1854 London Ch...    13     4
    ## 820          BCG                                   BCG Vaccine Data    13     7
    ## 935       cement                    Heat Evolved by Setting Cements    13     5
    ## 1354    kootenay  Waterflow Measurements of Kootenay River in Li...    13     2
    ## 1644  Newhouse77  Medical-Care Expenditure: A Cross-National Sur...    13     5
    ## 1735      Saxony                                 Families in Saxony    13     2

### Keeping downloaded data

By default the data is obtained over the web from
[Rdatasets](https://github.com/vincentarelbundock/Rdatasets/), but
`example_dataset` has an option to keep the data “locally.” (The data is
saved in `XDG_DATA_HOME`, see [SS1](https://pypi.org/project/xdg/).)

This can be demonstrated with the following timings of a dataset with
~1300 rows:

    import time
    startTime = time.time()
    data = example_dataset(itemSpec = 'titanic', packageSpec = 'COUNT', keep = True)
    endTime = time.time()
    print("Geting the data first time took " + str( endTime - startTime ) + " seconds")

    ## Geting the data first time took 0.013968706130981445 seconds

    import time
    startTime = time.time()
    data = example_dataset(itemSpec = 'titanic', packageSpec = 'COUNT', keep = True)
    endTime = time.time()
    print("Geting the data second time took " + str( endTime - startTime ) + " seconds")

    ## Geting the data second time took 0.013860702514648438 seconds

------------------------------------------------------------------------

## References

### Functions, packages, repositories

\[AAf1\] Anton Antonov,
[`ExampleDataset`](https://resources.wolframcloud.com/FunctionRepository/resources/ExampleDataset),
(2020), [Wolfram Function
Repository](https://resources.wolframcloud.com/FunctionRepository).

\[AAr1\] Anton Antonov,
[`Data::ExampleDatasets Raku package`](https://github.com/antononcube/Raku-Data-ExampleDatasets),
(2021), [GitHub/antononcube](https://github.com/antononcube).

\[VAB1\] Vincent Arel-Bundock,
[Rdatasets](https://github.com/vincentarelbundock/Rdatasets/), (2020),
[GitHub/vincentarelbundock](https://github.com/vincentarelbundock).

\[SS1\] Scott Stevenson, [xdg Python
package](https://pypi.org/project/xdg/), (2016-2021),
[PyPI.org](https://pypi.org/project/xdg/).

### Interactive interfaces

\[AAi1\] Anton Antonov, [Example datasets recommender
interface](https://antononcube.shinyapps.io/ExampleDatasetsRecommenderInterface/),
(2021), [Shinyapps.io](https://antononcube.shinyapps.io/).
