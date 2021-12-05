# Random Sparse Matrix Generator in Python

## In brief

This Python package implements the function `random_sparse_matrix` that generates random sparse matrices.

------

## Installation 

To install from GitHub use the shell command:

```shell
python -m pip install git+https://github.com/antononcube/Python-packages.git#egg=RandomSparseMatrix\&subdirectory=RandomSparseMatrix
```

To install from PyPI:

```shell
python -m pip install RandomSparseMatrix
```

------

## Examples

Here is random sparse matrix 
([`SSparseMatrix` object](https://pypi.org/project/SSparseMatrix)) 
with 6 rows and 4 columns:

```python
import random
from RandomSparseMatrix import *

random.seed(87)
rmat = random_sparse_matrix(6, 4,
                            column_names_generator=random_pet_name,
                            row_names_generator=random_word,
                            min_number_of_values=6,
                            max_number_of_values=None)
rmat.print_matrix(n_digits=20)

# ============================================================================================
#            |                Cleo             Diamond                 Max               Tessa
# --------------------------------------------------------------------------------------------
#  cuticular |                   .                   .                   .  12.886794438387263
#    elysian |                   .                   .                   .  13.891135469455826
# spot-check |                   .  11.465064963144142                   .                   .
#   cetacean |                   .   9.626463367706222                   .                   .
#       idem |   5.474873249244756                   .                   .                   .
#        lot |                   .                   .  10.818678723268317                   .
# ============================================================================================
```

------

## References

[AAp1] Anton Antonov,
[SSparseMatrix Python package](https://pypi.org/project/SSparseMatrix),
(2021),
[PyPI](https://pypi.org).

[AAp2] Anton Antonov,
[RandomDataGenerators Python package](https://pypi.org/project/RandomDataGenerators),
(2021),
[PyPI](https://pypi.org).

[AAp3] Anton Antonov,
[SparseMatrixRecommender Python package](https://pypi.org/project/SparseMatrixRecommender),
(2021),
[PyPI](https://pypi.org).

