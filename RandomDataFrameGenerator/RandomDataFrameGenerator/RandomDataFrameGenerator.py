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


def _is_func_list(obj):
    return isinstance(obj, list) and \
           all([isinstance(x, type(random_word)) or isinstance(x, type(numpy.random.poisson)) for x in obj])


def _is_func_dict(obj):
    return isinstance(obj, dict) and \
           _is_str_list(list(obj.keys())) and \
           all([isinstance(x, type(random_word)) or isinstance(x, type(numpy.random.poisson)) for x in list(obj.values())])


def random_data_frame(n_rows=None,
                      columns_spec=None,
                      form="wide",
                      generators=None,
                      min_number_of_values=None, max_number_of_values=None,
                      row_names=False):
    # Process number of rows
    mn_rows = n_rows
    if isinstance(mn_rows, type(None)):
        mn_rows = int(numpy.random.poisson(lam=20, size=1))
        mn_rows = 1 if mn_rows == 0 else mn_rows
    elif not isinstance(mn_rows, int) and mn_rows > 0:
        raise ValueError("The first argument 'n_rows' is expected to be a positive integer or None.")
        return None

    # Process number of columns
    mn_cols = None
    column_names = None
    if isinstance(columns_spec, type(None)):
        mn_cols = int(numpy.random.poisson(lam=7, size=1)[0])
        mn_cols = 1 if mn_cols == 0 else mn_cols
    elif _is_str_list(columns_spec):
        column_names = columns_spec
        mn_cols = len(column_names)
    elif isinstance(columns_spec, int) and columns_spec > 0:
        mn_cols = columns_spec
    else:
        TypeError("""The second, columns specification argument is expected to be a positive integer,
        a list of strings, or None.""")
        return None

    # Column names generator
    if isinstance(column_names, type(None)):
        column_names = random_word(size=mn_cols, kind='Common')

    # Generators
    aDefaultGenerators = {}
    for cn in column_names:
        my_rand = random.random()
        if my_rand < 0.3:
            aDefaultGenerators[cn] = random_word
        elif my_rand < 0.5:
            aDefaultGenerators[cn] = random_string
        elif my_rand < 0.8:
            aDefaultGenerators[cn] = numpy.random.normal
        else:
            aDefaultGenerators[cn] = numpy.random.poisson

    if isinstance(generators, type(None)):

        aGenerators = aDefaultGenerators

    elif _is_func_list(generators):

        aGenerators = generators
        while len(aGenerators) < mn_cols:
            aGenerators = aGenerators + aGenerators
        aGenerators = dict(zip(column_names, aGenerators[0:mn_cols]))

    elif _is_func_dict(generators):

        common_keys = set(aDefaultGenerators) & set(generators)
        aGenerators = aDefaultGenerators | {x: generators[x] for x in common_keys}

    else:
        raise TypeError("Unknown type of generators specification.")
        return None

    # Generate data frame
    dfRand = pandas.DataFrame.from_dict({k: f(size=mn_rows) for (k, f) in aGenerators.items()})

    return dfRand
