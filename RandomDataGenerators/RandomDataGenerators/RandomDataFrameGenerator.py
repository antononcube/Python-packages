import random
import pandas
import numpy
import itertools
import warnings
from .RandomFunctions import random_string
from .RandomFunctions import random_word


def _is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def _is_str_keys_dict(obj):
    return isinstance(obj, dict) and all([isinstance(k, str) for (k, v) in obj.items()])


def _is_func_list(obj):
    return isinstance(obj, list) and all([callable(x) for x in obj])


def _is_func_dict(obj):
    return isinstance(obj, dict) and _is_str_list(list(obj.keys())) and all([callable(x) for x in list(obj.values())])


def _is_func_or_list_list(obj):
    return isinstance(obj, list) and all([callable(x) or isinstance(x, list) for x in obj])


def _is_func_or_list_dict(obj):
    return isinstance(obj, dict) and _is_str_list(list(obj.keys())) and all(
        [callable(x) or isinstance(x, list) for x in list(obj.values())])


def _make_selector_func(x: list):
    def my_selector(size: int):
        return random.choices(population=x, k=size)

    return my_selector


def _process_row_and_column_specs(n_rows, columns_spec, column_names_generator, warn=True):
    # Process number of rows
    mn_rows = n_rows
    if isinstance(mn_rows, type(None)):
        mn_rows = int(numpy.random.poisson(lam=20, size=1))
        mn_rows = 1 if mn_rows == 0 else mn_rows
    elif not isinstance(mn_rows, int) and mn_rows > 0:
        raise ValueError("The first argument 'n_rows' is expected to be a positive integer or None.")

    # Process columns spec
    mn_cols = None
    column_names = None
    if columns_spec is None:
        mn_cols = int(numpy.random.poisson(lam=7, size=1)[0])
        mn_cols = 1 if mn_cols == 0 else mn_cols
    elif _is_str_list(columns_spec):
        column_names = list(dict.fromkeys(columns_spec))
        mn_cols = len(column_names)
    elif isinstance(columns_spec, int) and columns_spec > 0:
        mn_cols = columns_spec
    else:
        raise TypeError("""The second, columns specification argument is expected to be a positive integer,
        a list of strings, or None.""")

    # Column names generator
    if isinstance(columns_spec, type(None)) or isinstance(columns_spec, int):
        if isinstance(column_names_generator, type(None)):
            column_names = random_word(size=mn_cols, kind='Common')
        elif isinstance(column_names_generator, type(random_word)):
            column_names = column_names_generator(mn_cols)
        elif isinstance(column_names_generator, type(numpy.random.poisson)):
            column_names = column_names_generator(size=mn_cols)
        elif isinstance(column_names_generator, list):
            my_selector = _make_selector_func(column_names_generator)
            column_names = my_selector(size=mn_cols)
        else:
            raise TypeError(
                "The column names generator is expected to be None, a function, or an object of type " +
                str(type(numpy.random.poisson)) + ".")

        # Unique column names
        column_names = list(dict.fromkeys(column_names))

    # Handling the case when the generated column names are too few
    if len(column_names) < mn_cols:

        if columns_spec is None:

            mn_cols = len(column_names)

        else:
            # E.g. isinstance(columns_spec, int) and len(column_names) < columns_spec:

            if warn:
                warnings.warn("The obtained column names are too few. Adding ordinal suffixes.",
                              UserWarning)

            column_names = [x + "_" + str(i) for (x, i) in zip(numpy.resize(column_names, mn_cols), range(mn_cols))]

    return [mn_rows, mn_cols, column_names]


def random_data_frame(n_rows=None,
                      columns_spec=None,
                      column_names_generator=None,
                      form="wide",
                      generators=None,
                      min_number_of_values=None, max_number_of_values=None,
                      row_names=False):
    """Generates random tabular data frame."""
    # Process rows and columns specs
    mn_rows, mn_cols, column_names = _process_row_and_column_specs(n_rows=n_rows,
                                                                   columns_spec=columns_spec,
                                                                   column_names_generator=column_names_generator)

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

    elif _is_func_or_list_list(generators):

        aGenerators = generators
        aGenerators = [x if callable(x) else _make_selector_func(x) for x in aGenerators]
        while len(aGenerators) < mn_cols:
            aGenerators = aGenerators + aGenerators
        aGenerators = dict(zip(column_names, aGenerators[0:mn_cols]))

    elif _is_func_or_list_dict(generators):

        common_keys = set(aDefaultGenerators) & set(generators)
        # This is version 3.9+ only:
        # aGenerators = aDefaultGenerators | {
        #     x: generators[x] if callable(generators[x]) else _make_selector_func(generators[x])
        #     for x in common_keys}
        aGenerators = {**aDefaultGenerators,
                       **{x: generators[x] if callable(generators[x]) else _make_selector_func(generators[x]) for x in
                          common_keys}}

    elif callable(generators):

        aGenerators = dict(zip(column_names, numpy.resize(generators, len(column_names))))

    else:
        raise TypeError("Unknown type of generators specification.")

    # Max Number Of Values
    if isinstance(max_number_of_values, type(None)):
        mmax_number_of_values = mn_rows * mn_cols
    elif isinstance(max_number_of_values, int) and max_number_of_values > 0:
        mmax_number_of_values = max_number_of_values
    else:
        raise TypeError("The argument max_number_of_values is expected to be a non-negative integer or None.")

    # Min Number Of Values
    if isinstance(min_number_of_values, type(None)):
        mmin_number_of_values = mmax_number_of_values
    elif isinstance(min_number_of_values, int) and min_number_of_values > 0:
        mmin_number_of_values = min_number_of_values
        if mmin_number_of_values > mmax_number_of_values:
            mmin_number_of_values = mmax_number_of_values
    else:
        raise TypeError("The argument min_number_of_values is expected to be a non-negative integer or None.")

    # Form
    if isinstance(form, type(None)):
        form = "long" if random.random() < 0.3 else "wide"

    if not (isinstance(form, str) and form.lower() in {"long", "wide"}):
        warnings.warn(
            "The argument form is expected to be None or one of 'Long' or 'Wide'. Continuing using 'Wide'.",
            UserWarning)
        mform = "wide"
    else:
        mform = form.lower()

    # Generate coordinate pairs for the random values
    dfPairs = []
    # This is probably a "premature optimization" implementation,
    # but it has to be considered for large n_rows * n_cols values.
    k = 0
    while len(dfPairs) < mmin_number_of_values and k < 4:

        dfPairs2 = numpy.random.randint(low=0,
                                        high=mn_rows * mn_cols,
                                        size=numpy.random.randint(low=mmin_number_of_values,
                                                                  high=mmax_number_of_values + 1))
        dfPairs2 = list(dfPairs2)

        old_len = len(dfPairs)

        if len(dfPairs) == 0:
            dfPairs = list(dict.fromkeys(sorted(dfPairs2)))
        else:
            dfPairs = list(dict.fromkeys(sorted(dfPairs + dfPairs2)))

        new_len = len(dfPairs)

        # This if-else and the loop condition k < 4
        # will break the loop if there is no data increment for "too many" iterations.
        if old_len == new_len:
            k = k + 1
        else:
            k = 0

    if len(dfPairs) > mmax_number_of_values:
        dfPairs = numpy.resize(dfPairs, mmax_number_of_values)

    dfPairs = [(x // mn_rows, x % mn_rows) for x in dfPairs]
    dfPairs.sort(key=lambda x: x[0])
    colGroups = [(key, [x for (_, x) in value]) for key, value in itertools.groupby(dfPairs, lambda x: x[0])]

    # Generate data frame columns
    dfRand = {column_names[k]: dict(zip(rowInds, aGenerators[column_names[k]](size=mn_rows)))
              for (k, rowInds) in colGroups}
    dfRand = pandas.DataFrame(dfRand)
    dfRand = dfRand.reindex(columns=column_names)

    if row_names:
        dfRand.index = ["id." + str(x) for x in range(dfRand.shape[0])]

    if mform == "long":
        if row_names:
            dfRowNames = pandas.DataFrame({"row_name": dfRand.index})
            dfRand = pandas.concat([dfRand.reset_index(drop=True), dfRowNames], axis=1)
            dfRand = dfRand.melt(id_vars="row_name")
        else:
            dfRand = dfRand.melt()

    return dfRand
