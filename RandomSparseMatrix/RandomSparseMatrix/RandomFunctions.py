import warnings

import RandomDataGenerators
from RandomDataGenerators import random_data_frame
from RandomDataGenerators import random_word
from SparseMatrixRecommender import cross_tabulate
import numpy
import random
import math


def random_sparse_matrix(n_rows=None,
                         columns_spec=None,
                         column_names_generator=None,
                         row_names_generator=None,
                         generators=None,
                         min_number_of_values=None,
                         max_number_of_values=None):
    """Generates random sparse matrices."""

    mgenerators = generators
    if isinstance(generators, type(None)):
        mgenerators = [lambda size: numpy.random.normal(loc=10, scale=2, size=size)]
    elif callable(generators):
        mgenerators = [generators, ]

    mn_rows, mn_cols, column_names = RandomDataGenerators.RandomDataFrameGenerator._process_row_and_column_specs(
        n_rows=n_rows,
        columns_spec=columns_spec,
        column_names_generator=column_names_generator)

    mrow_names_generator = row_names_generator
    if isinstance(mrow_names_generator, type(None)):
        mrow_names_generator = column_names_generator

    _, _, row_names = RandomDataGenerators.RandomDataFrameGenerator._process_row_and_column_specs(
        n_rows=mn_rows,
        columns_spec=mn_rows,
        column_names_generator=mrow_names_generator,
        warn=False)

    # If the row names generator produced number of row names that is smaller
    # than the automatically derived number of rows, then correct the number of rows.
    if n_rows is None and len(row_names) != n_rows:
        mn_rows = len(row_names)

    mmax_number_of_values = max_number_of_values
    if isinstance(max_number_of_values, type(None)):
        mmax_number_of_values = max(1, math.floor(0.1 * mn_rows * mn_cols))

    mmin_number_of_values = min_number_of_values
    if isinstance(min_number_of_values, type(None)):
        mmin_number_of_values = 2

    if isinstance(min_number_of_values, int) and max_number_of_values is None:
        mmax_number_of_values = max(1, min_number_of_values + math.floor(0.1 * mn_rows * mn_cols))

    dfRandLong = random_data_frame(n_rows=mn_rows,
                                   columns_spec=column_names,
                                   generators=mgenerators,
                                   max_number_of_values=mmax_number_of_values,
                                   min_number_of_values=mmin_number_of_values,
                                   row_names=True,
                                   form='Long')
    dfRandLong = dfRandLong.fillna(0)

    rmat = cross_tabulate(data=dfRandLong, index="row_name", columns="variable", values="value")
    smat = rmat.sparse_matrix()
    smat.eliminate_zeros()
    rmat.set_sparse_matrix(smat)
    rmat.set_row_names("RowID.")

    if rmat.rows_count() == mn_rows and len(row_names) == mn_rows:
        rmat.set_row_names(row_names)

    elif rmat.rows_count() < mn_rows or len(row_names) < mn_rows:
        # Since we are using long form to generate the sparse matrix entries
        # it can happen that some rows are not present. Hence, we have to
        # complete the obtained matrix into a matrix with the required number of rows.
        # Similar case arises if the specified row names generator produces fewer
        # unique row names than the specified number of rows.

        # Generate and annex additional row names.
        add_names = ["RowIDNew." + str(i) for i in range(mn_rows - rmat.rows_count())]
        add_names = [add_names, ] if isinstance(add_names, str) else add_names

        # Note that we make random sampling of the completed row names.
        # (The function random_data_frame does not act upon specified row names.)
        rmat = rmat.impose_row_names(random.sample(rmat.row_names() + add_names, k=mn_rows))

        row_names2 = row_names
        if len(row_names2) < mn_rows:
            warnings.warn(
                "The specified number of rows is larger than the obtained row names. Adding ordinal suffixes.",
                UserWarning)
            row_names2 = [x + "_" + str(y) for (x, y) in zip(numpy.resize(row_names2, mn_rows), range(mn_rows))]

        rmat = rmat.set_row_names(row_names2)

    if rmat.columns_count() < mn_cols:
        rmat = rmat.impose_column_names(column_names)

    return rmat
