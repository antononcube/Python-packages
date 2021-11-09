# SSparseMatrix

## In brief

This package attempts to cover as many as possible of the functionalities for 
sparse matrix objects that are provided by R’s Matrix library. 

- [X] Sub-matrix extraction by row and column names
   - [X] Single element access
   - [X] Slices (with integers)
   - [X] Subsets of row names and column names
- [X] Row and column names propagation for dot products
   - [X] Lists
   - [X] Dense vectors (`numpy.array`)
   - [X] `scipy` sparse matrices
   - [X] `SSparseMatrix` objects
- [X] Row and column sums 
- [X] Transposing
- [X] Pretty printing
- [ ] Row and column binding of `SSparseMatrix` objects
  - [ ] Row binding
  - [ ] Column binding
- [ ] "Export" functions
  - [ ] Triplets
  - [ ] Row-dictionaries
  - [ ] Column-dictionaries

This package more or less follows the design of the
Mathematica package
[SSparseMatrix.m](https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m).

-------

## Installation

### Install from GitHub

```shell
pip install -e git+https://github.com/antononcube/Python-packages.git#egg=SSparseMatrix-antononcube\&subdirectory=SSparseMatrix
```

### From local directory

```shell
pip install ./SSparseMatrix
```

-------

## Usage examples

The usage examples below can be run through the file ["examples.py"](./examples.py).

### Creation

Setup:

```python
from SSparseMatrix.src.SSparseMatrix import *
```

Create a sparse matrix with named rows and columns (a SSparseMatrix object):

```python
mat = [[1, 0, 4, 16], [4, 0, 0, 10], [0, 9, 5, 5], [0, 0, 1, 0], [0, 0, 0, 5]]
smat = SSparseMatrix(mat)
smat.set_row_names(["A", "B", "C", "D", "E"])
smat.set_column_names(["a", "b", "c", "d"])
```

Print the created sparse matrix:

```python
smat.print_matrix()
# ===========
#   | a b c d
# -----------
# A | 1 0 0 3
# B | 4 0 0 5
# C | 0 3 0 5
# D | 0 0 1 0
# E | 0 0 0 5
# ===========
```

### Multiplication

Multiply with the transpose and print:

```python
smat2 = smat.copy().dot(smat.copy().transpose())
smat2.print_matrix()
# ==================
#   |  A  B  C  D  E
# ------------------
# A | 10 19 15  0 15
# B | 19 41 25  0 25
# C | 15 25 34  0 25
# D |  0  0  0  1  0
# E | 15 25 25  0 25
# ==================
```

Multiply with a list-vector:

```python
smat3 = smat.copy().dot([1, 2, 1, 0])
smat3.print_matrix()
# =====
#   | 0
# -----
# A | 1
# B | 4
# C | 6
# D | 1
# E | 0
# =====
```

**Remark:** The type of the `.dot` argument can be:
- `SSparseMatrix`
- `list`
- `numpy.array`
- `scipy.sparse.csr_matrix`

### Slices

Get single element:

```python
print(smat["A", "d"])
print(smat[0, 3])
# 3
# 3
```

Get subset of rows:
```python
smat[["A", "D", "B"],:].print_matrix()
# ===========
#   | a b c d
# -----------
# A | 1 0 0 3
# D | 0 0 1 0
# B | 4 0 0 5
# ===========
```
Get subset of columns:
```python
smat[:, ['a', 'c']].print_matrix()
# =======
#   | a c
# -------
# A | 1 0
# B | 4 0
# C | 0 0
# D | 0 1
# E | 0 0
# =======
```

**Remark:** The current implementation of `scipy` (1.7.1) does not allow retrieval
of sub-matrices with by specifying *both* row and column subsets. 

**Remark:** "Standard" slices with integers also work. 

### Sums

Row sums:

```python
print(smat.row_sums())
print(smat.row_sums_dict())
# [4, 9, 8, 1, 5]
# {'A': 4, 'B': 9, 'C': 8, 'D': 1, 'E': 5}
```

Column sums:

```python
print(smat.column_sums())
print(smat.column_sums_dict())
# [5, 3, 1, 18]
# {'a': 5, 'b': 3, 'c': 1, 'd': 18}
```

-------

## Larger data

*TBD...*

-------

## Unit tests

The [unit tests](./tests) have more usage detailed examples. 

To run all tests in the directors [./tests](./tests) use the shell command:

*TBD...*

-------

## References

### Articles

[AA1] Anton Antonov,
["RSparseMatrix for sparse matrices with named rows and columns"](https://mathematicaforprediction.wordpress.com/2015/10/08/rsparsematrix-for-sparse-matrices-with-named-rows-and-columns/),
(2015),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

### Packages

[AAp1] Anton Antonov,
[SSparseMatrix.m](https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m),
(2018),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).
