# Sparse matrices with named rows and columns

![PyPI](https://img.shields.io/pypi/v/SSparseMatrix?label=pypi%20SSparseMatrix)
![PyPI - Downloads](https://img.shields.io/pypi/dm/SSparseMatrix)

PePy:   
[![Downloads](https://static.pepy.tech/badge/SSparseMatrix)](https://pepy.tech/project/SSparseMatrix)
[![Downloads](https://static.pepy.tech/badge/SSparseMatrix/month)](https://pepy.tech/project/SSparseMatrix)
[![Downloads](https://static.pepy.tech/badge/SSparseMatrix/week)](https://pepy.tech/project/SSparseMatrix)


## Introduction

This Python package provides the class `SSparseMatrix` the objects of which are sparse matrices with named rows and columns.

We can say the package attempts to cover as many as possible of the functionalities for 
sparse matrix objects that are provided by R’s library [Matrix](http://matrix.r-forge.r-project.org). ([R](https://en.wikipedia.org/wiki/R_(programming_language)) is a implementation of [S](https://en.wikipedia.org/wiki/S_(programming_language)). 
S introduced named data structures for statistical computations, [RB1], hence the name `SSparseMatrix`.)

The package builds on top of the [`scipy` sparse matrices](https://scipy.github.io/devdocs/reference/sparse.html). 
(The added functionalities though are general -- other sparse matrix implementations could be used.)

Here is a list of functionalities provided for `SSparseMatrix`:

- Sub-matrix extraction by row and column names:
   - Single element access
   - Subsets of row names and column names
- Slices (with integers)
- Row and column names propagation for dot products with:
   - Lists
   - Dense vectors (`numpy.array`)
   - `scipy` sparse matrices
   - `SSparseMatrix` objects
- Row and column sums 
   - Vector form
   - Dictionary form
- Transposing
- Representation:
  - Tabular, matrix form ("pretty printing")
  - String and `repr` forms
- Row and column binding of `SSparseMatrix` objects
- "Export" functions
  - Triplets
  - Row-dictionaries
  - Column-dictionaries
  - Wolfram Language full form representation

The full list of features and development status can be found in the 
[org-mode](https://orgmode.org)
file
[SSparseMatrix-work-plan.org](https://github.com/antononcube/Python-packages/blob/main/org/SSparseMatrix-work-plan.org).

This package more or less follows the design of the
Mathematica package
[SSparseMatrix.m](https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m), [AAp1], and the corresponding paclet [AAp3].

The usage examples below can be also run through the file ["examples.py"](./examples.py).

**Remark:** The functionalities provided by package, "SSparseMatrix", are fundamental for the packages
["SparseMatrixRecommender"](https://pypi.org/project/SparseMatrixRecommender/), [AAp4], and
["LatentSemanticAnalyzer"](https://pypi.org/project/LatentSemanticAnalyzer/), [AAp5].

### Usage in other packages

The class `SSparseMatrix` is foundational in the packages
[SparseMatrixRecommender](https://github.com/antononcube/Python-packages/tree/main/SparseMatrixRecommender)
and
[LatentSemanticAnalyzer](https://github.com/antononcube/Python-packages/tree/main/LatentSemanticAnalyzer).
(The implementation of those packages was one of the primary motivations to develop `SSparseMatrix`.)

The package
[RandomSparseMatrix](https://github.com/antononcube/Python-packages/tree/main/RandomSparseMatrix)
can be used to generate random sparse matrices (`SSparseMatrix` objects.)

------

## Installation

### Install from GitHub

```shell
pip install -e git+https://github.com/antononcube/Python-packages.git#egg=SSparseMatrix-antononcube\&subdirectory=SSparseMatrix
```

### From PyPi

```shell
pip install SSparseMatrix
```


------

## Setup

Import the package:


```python
from SSparseMatrix import *
```

The import command above is equivalent to the import commands:

```python
from SSparseMatrix.SSparseMatrix import SSparseMatrix
from SSparseMatrix.SSparseMatrix import make_s_sparse_matrix
from SSparseMatrix.SSparseMatrix import is_s_sparse_matrix
from SSparseMatrix.SSparseMatrix import column_bind
```

-----

## Creation

Create a sparse matrix with named rows and columns (a `SSparseMatrix` object):


```python
mat = [[1, 0, 0, 3], [4, 0, 0, 5], [0, 3, 0, 5], [0, 0, 1, 0], [0, 0, 0, 5]]
smat = SSparseMatrix(mat)
smat.set_row_names(["A", "B", "C", "D", "E"])
smat.set_column_names(["a", "b", "c", "d"])
```




    <5x4 SSparseMatrix (sparse matrix with named rows and columns) of type '<class 'numpy.int64'>'
    	with 8 stored elements in Compressed Sparse Row format, and fill-in 0.4>



Print the created sparse matrix:


```python
smat.print_matrix()
```

    ===================================
      |       a       b       c       d
    -----------------------------------
    A |       1       .       .       3
    B |       4       .       .       5
    C |       .       3       .       5
    D |       .       .       1       .
    E |       .       .       .       5
    ===================================


Another way to create using the function `make_s_sparse_matrix`:


```python
ssmat=make_s_sparse_matrix(mat)
ssmat
```




    <5x4 SSparseMatrix (sparse matrix with named rows and columns) of type '<class 'numpy.int64'>'
    	with 8 stored elements in Compressed Sparse Row format, and fill-in 0.4>



------

## Structure

The `SSparseMatrix` objects have a simple structure. Here are the attributes:
- `_sparseMatrix`
- `_rowNames`
- `_colNames`
- `_dimNames`

Here are the methods to "query" `SSparseMatrix` objects:
- `sparse_matrix()`
- `row_names()` and `row_names_dict()`
- `column_names()` and `column_names_dict()`
- `shape()`
- `dimension_names()`

`SSparseMatrix` over-writes the methods of `scipy.sparse.csr_matrix` that might require the handling of row names and column names.

Most of the rest of the `scipy.sparse.csr_matrix`
[methods](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html)
are delegated to the `_sparseMatrix` attribute.

For example, for a given `SSparseMatrix` object `smat` the dense version of `smat`'s sparse matrix attribute
can be obtained by accessing that attribute first and then using the method `todense`:


```python
print(smat.sparse_matrix().todense())
```

    [[1 0 0 3]
     [4 0 0 5]
     [0 3 0 5]
     [0 0 1 0]
     [0 0 0 5]]


Alternatively, we can use the "delegated" form and directly invoke `todense` on `smat`:


```python
print(smat.todense())
```

    [[1 0 0 3]
     [4 0 0 5]
     [0 3 0 5]
     [0 0 1 0]
     [0 0 0 5]]


Here is another example showing a direct application of the element-wise operation `sin` through
the `scipy.sparse.csr_matrix` method `sin`:


```python
smat.sin().print_matrix(n_digits=20)
```

    ===================================================================================
      |                   a                   b                   c                   d
    -----------------------------------------------------------------------------------
    A |  0.8414709848078965                   .                   .  0.1411200080598672
    B | -0.7568024953079282                   .                   . -0.9589242746631385
    C |                   .  0.1411200080598672                   . -0.9589242746631385
    D |                   .                   .  0.8414709848078965                   .
    E |                   .                   .                   . -0.9589242746631385
    ===================================================================================


------
## Representation

Here the function `print` uses the string representation of `SSparseMatrix` object:


```python
print(smat)
```

      ('A', 'a')	1
      ('A', 'd')	3
      ('B', 'a')	4
      ('B', 'd')	5
      ('C', 'b')	3
      ('C', 'd')	5
      ('D', 'c')	1
      ('E', 'd')	5


Here we print the representation obtained with [`repr`](https://docs.python.org/3.4/library/functions.html?highlight=repr#repr):


```python
print(repr(smat))
```

    <5x4 SSparseMatrix (sparse matrix with named rows and columns) of type '<class 'numpy.int64'>'
    	with 8 stored elements in Compressed Sparse Row format, and fill-in 0.4>


Here is the matrix form ("pretty printing" ):


```python
smat.print_matrix()
```

    ===================================
      |       a       b       c       d
    -----------------------------------
    A |       1       .       .       3
    B |       4       .       .       5
    C |       .       3       .       5
    D |       .       .       1       .
    E |       .       .       .       5
    ===================================


The method `triplets` can be used to obtain a list of `(row, column, value)` triplets:


```python
smat.triplets()
```




    [('A', 'a', 1),
     ('A', 'd', 3),
     ('B', 'a', 4),
     ('B', 'd', 5),
     ('C', 'b', 3),
     ('C', 'd', 5),
     ('D', 'c', 1),
     ('E', 'd', 5)]



The method `row_dictionaries` gives a dictionary with keys that are row-names and values that are column-name-to-matrix-value dictionaries:


```python
smat.row_dictionaries()
```




    {'A': {'a': 1, 'd': 3},
     'B': {'a': 4, 'd': 5},
     'C': {'b': 3, 'd': 5},
     'D': {'c': 1},
     'E': {'d': 5}}



Similarly, the method `column_dictionaries` gives a dictionary with keys that are column-names and values that are row-name-to-matrix-value dictionaries:


```python
smat.column_dictionaries()
```




    {'a': {'A': 1, 'B': 4},
     'b': {'C': 3},
     'c': {'D': 1},
     'd': {'A': 3, 'B': 5, 'C': 5, 'E': 5}}



------

## Multiplication

Multiply with the transpose and print:


```python
ssmat2 = ssmat.dot(smat.transpose())
ssmat2.print_matrix()
```

    ===========================================
      |       A       B       C       D       E
    -------------------------------------------
    0 |      10      19      15       .      15
    1 |      19      41      25       .      25
    2 |      15      25      34       .      25
    3 |       .       .       .       1       .
    4 |      15      25      25       .      25
    ===========================================


Multiply with a list-vector:


```python
smat3 = smat.dot([1, 2, 1, 0])
smat3.print_matrix()
```

    ===========
      |       0
    -----------
    A |       1
    B |       4
    C |       6
    D |       1
    E |       .
    ===========


**Remark:** The type of the `.dot` argument can be:
- `SSparseMatrix`
- `list`
- `numpy.array`
- `scipy.sparse.csr_matrix`

------

## Slices

Single element access:


```python
print(smat["A", "d"])
print(smat[0, 3])
```

    3
    3


Get sub-matrix of rows using row names:


```python
smat[["A", "D", "B"], :].print_matrix()
```

    ===================================
      |       a       b       c       d
    -----------------------------------
    A |       1       .       .       3
    D |       .       .       1       .
    B |       4       .       .       5
    ===================================


Get sub-matrix using row indices:


```python
smat[[0, 3, 1], :].print_matrix()
```

    ===================================
      |       a       b       c       d
    -----------------------------------
    A |       1       .       .       3
    D |       .       .       1       .
    B |       4       .       .       5
    ===================================


Get sub-matrix with columns names:


```python
smat[:, ['a', 'c']].print_matrix()
```

    ===================
      |       a       c
    -------------------
    A |       1       .
    B |       4       .
    C |       .       .
    D |       .       1
    E |       .       .
    ===================


Get sub-matrix with columns indices:


```python
smat[:, [0, 2]].print_matrix()
```

    ===================
      |       a       c
    -------------------
    A |       1       .
    B |       4       .
    C |       .       .
    D |       .       1
    E |       .       .
    ===================


**Remark:** The current implementation of `scipy` (1.7.1) does not allow retrieval
of sub-matrices by specifying *both* row and column ranges or slices. 

**Remark:** "Standard" slices with integers also work. 

-------

## Row and column sums

Row sums and dictionary of row sums:


```python
print(smat.row_sums())
print(smat.row_sums_dict())
```

    [4, 9, 8, 1, 5]
    {'A': 4, 'B': 9, 'C': 8, 'D': 1, 'E': 5}


Column sums and dictionary of column sums:


```python
print(smat.column_sums())
print(smat.column_sums_dict())
```

    [5, 3, 1, 18]
    {'a': 5, 'b': 3, 'c': 1, 'd': 18}


------

## Column and row binding

### Column binding

Here we create another `SSparseMatrix` object:


```python
mat2=smat.sparse_matrix().transpose()
smat2 = SSparseMatrix(mat2, row_names=list("ABCD"), column_names="c")
smat2.print_matrix()
```

    ===========================================
      |      c0      c1      c2      c3      c4
    -------------------------------------------
    A |       1       4       .       .       .
    B |       .       .       3       .       .
    C |       .       .       .       1       .
    D |       3       5       5       .       5
    ===========================================


Here we column-bind two SSparseMatrix objects:


```python
smat[list("ABCD"), :].column_bind(smat2).print_matrix()
```

    ===========================================================================
      |       a       b       c       d      c0      c1      c2      c3      c4
    ---------------------------------------------------------------------------
    A |       1       .       .       3       1       4       .       .       .
    B |       4       .       .       5       .       .       3       .       .
    C |       .       3       .       5       .       .       .       1       .
    D |       .       .       1       .       3       5       5       .       5
    ===========================================================================


**Remark:** If during column-binding some column names are duplicated then to the column names of both matrices are
added suffixes that designate to which matrix each column belongs to.

### Row binding

Here we rename the column names of `smat` to be the same as `smat2`:


```python
smat3 = smat.copy()
smat3.set_column_names(smat2.column_names()[0:4])
smat3 = smat3.impose_column_names(smat2.column_names())
smat3.print_matrix()
```

    ===========================================
      |      c0      c1      c2      c3      c4
    -------------------------------------------
    A |       1       .       .       3       .
    B |       4       .       .       5       .
    C |       .       3       .       5       .
    D |       .       .       1       .       .
    E |       .       .       .       5       .
    ===========================================


Here we row-bind `smat2` and `smat3`:


```python
smat2.row_bind(smat3).print_matrix()

```

    =============================================
        |      c0      c1      c2      c3      c4
    ---------------------------------------------
    A.1 |       1       4       .       .       .
    B.1 |       .       .       3       .       .
    C.1 |       .       .       .       1       .
    D.1 |       3       5       5       .       5
    A.2 |       1       .       .       3       .
    B.2 |       4       .       .       5       .
    C.2 |       .       3       .       5       .
    D.2 |       .       .       1       .       .
    E.2 |       .       .       .       5       .
    =============================================


**Remark:** If during row-binding some row names are duplicated then to the row names of both matrices are added
suffixes that designate to which matrix each row belongs to.

------

## In place computations

- The methods for setting row- and column-names are "in place" methods -- no new `SSparseMatrix` objects a created.

- The dot product, arithmetic, and transposing methods have an optional argument whether to do computations in place or not.
    - The optional argument is `copy`, which corresponds to argument with the same name and function in `scipy.sparse`.
    - By default, the computations are *not* in place: new objects are created.
    - I.e. `copy=True` default.

- The class `SSparseMatrix` has the method `copy()` that produces deep copies when invoked.

-------

## Unit tests

The unit tests (so far) are broken into functionalities; see the folder
[./tests](https://github.com/antononcube/Python-packages/tree/main/SSparseMatrix/tests).
Similar unit tests are given in [AAp2].

-------

## References

### Articles

[AA1] Anton Antonov,
["RSparseMatrix for sparse matrices with named rows and columns"](https://mathematicaforprediction.wordpress.com/2015/10/08/rsparsematrix-for-sparse-matrices-with-named-rows-and-columns/),
(2015),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

[RB1] Richard Becker, 
[“A Brief History of S”](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.131.1428&rep=rep1&type=pdf),
(2004).

### Packages

[AAp1] Anton Antonov,
[SSparseMatrix.m](https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m),
(2018),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp2] Anton Antonov,
[SSparseMatrix Mathematica unit tests](https://github.com/antononcube/MathematicaForPrediction/blob/master/UnitTests/SSparseMatrix-tests.wlt),
(2018),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp3] Anton Antonov,
[SSparseMatrix WL paclet](https://resources.wolframcloud.com/PacletRepository/resources/AntonAntonov/SSparseMatrix/),
(2023),
[Wolfram Language Paclet Repository](https://resources.wolframcloud.com/PacletRepository/).

[AAp4] Anton Antonov,
[SparseMatrixRecommender Python package](https://pypi.org/project/SparseMatrixRecommender/),
(2021),
[PyPI.org/antononcube](https://pypi.org/user/antononcube/).

[AAp4] Anton Antonov,
[LatentSemanticAnalyzer Python package](https://pypi.org/project/LatentSemanticAnalyzer/),
(2021),
[PyPI.org/antononcube](https://pypi.org/user/antononcube/).

