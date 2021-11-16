# Random Sparse Matrix Generator in Python

## In brief

This Python package implements the function `random_sparse_matrix` that generates random sparse matrices.

------

## Installation 

To install from GitHub use the shell command:

```shell
python -m pip install git+https://github.com/antononcube/Python-packages.git#egg=RandomSparseMatrix\&subdirectory=RandomSparseMatrix
```

------

## Examples

Here is random data frame with 14 rows:

```python
from RandomSparseMatrix.RandomFunctions import random_sparse_matrix
rmat=random_sparse_matrix(5, 5, max_number_of_values=10)
rmat.print_matrix(n_digits=20)

# ===========================================================================================
#           |            backseat             bedevil         carnivorous            upturned
# -------------------------------------------------------------------------------------------
# deepening |                   .                   .                   .   11.83055318326952
#     auric |                   .   7.563280169058409                   .  10.837344529418854
#     Cox-1 |                   .                   .   8.064729659976713  10.239783727049803
#    barony |   8.920426910396417                   .                   .                   .
# ===========================================================================================
```

------

## References

[AAp1] Anton Antonov,
[Random Tabular Dataset Mathematica Package](https://github.com/antononcube/MathematicaForPrediction/blob/master/Misc/RandomTabularDataset.m),
(2020),
[MathematicaForPrediction at GitHub/antononcube](https://github.com/antononcube/MathematicaForPrediction).

[AAp2] Anton Antonov,
[RandomTabularDataset Mathematica unit tests](https://github.com/antononcube/MathematicaForPrediction/blob/master/UnitTests/RandomTabularDataset-Unit-Tests.wlt),
(2020),
[MathematicaForPrediction at GitHub/antononcube](https://github.com/antononcube/MathematicaForPrediction).

[AAp3] Anton Antonov,
[RandomDataFrameGenerator R package](https://github.com/antononcube/R-packages/tree/master/RandomDataFrameGenerator),
(2020),
[R-packages at GitHub/antononcube](https://github.com/antononcube/R-packages/).

[AAp4] Anton Antonov,
[Data::Generators Raku module](https://modules.raku.org/dist/Data::Generator),
(2021),
[Raku Modules](https://modules.raku.org).