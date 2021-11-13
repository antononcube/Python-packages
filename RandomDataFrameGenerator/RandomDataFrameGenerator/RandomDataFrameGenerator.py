import random
import pandas
import numpy
from .RandomFunctions import random_string
from .RandomFunctions import random_pet_name
from .RandomFunctions import random_word


def _is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def _is_str_keys_dict(obj):
    return isinstance(obj, dict) and all([isinstance(k, str) for (k, v) in obj.items()])


def random_data_frame(n_rows=None,
                      columns_spec=None,
                      form="wide",
                      generators=None,
                      min_number_of_values=None, max_number_of_values=None,
                      row_names=False):
    # Process number of rows
    mn_rows = n_rows
    if isinstance(mn_rows, type(None)):
        mn_rows = numpy.random.poisson(lam=20, size=1)
    elif not isinstance(mn_rows, int) and mn_rows > 0:
        raise ValueError("The first argument 'n_rows' is expected to be a positive integer or None.")
        return None

    # Process number of columns
    mn_col = None
    column_names = None
    if isinstance(columns_spec, type(None)):
        mn_col = numpy.random.poisson(lam=7, size=1)
    elif _is_str_list(columns_spec):
        column_names = columns_spec
        mn_col = len(column_names)
    elif isinstance(columns_spec, int) and columns_spec > 0:
        mn_col = columns_spec
    else:
        TypeError("""The second, columns specification argument is expected to be a positive integer,
        a list of strings, or None.""")
        return None

    # Column names generator
    if isinstance(column_names, type(None)):
        column_names = random_word(size=mn_col, kind='Common')

    # Generate random values
    aDFColumns = {}
    for cn in column_names:
        my_rand = random.random()
        if my_rand < 0.3:
            aDFColumns[cn] = random_word
        elif my_rand < 0.5:
            aDFColumns[cn] = random_string
        elif my_rand < 0.8:
            aDFColumns[cn] = numpy.random.normal
        else:
            aDFColumns[cn] = numpy.random.poisson

    # Generate data frame
    dfRand = pandas.DataFrame.from_dict({k: f(size=mn_rows) for (k, f) in aDFColumns.items()})

    return dfRand

