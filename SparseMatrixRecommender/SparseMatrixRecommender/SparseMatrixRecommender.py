from SSparseMatrix import SSparseMatrix
from SSparseMatrix import column_bind
from SSparseMatrix import is_sparse_matrix
from .CrossTabulate import cross_tabulate
from .DocumentTermWeightFunctions import apply_term_weight_functions
import pandas
import scipy


# ======================================================================
# Utilities
# ======================================================================
def is_smat_dict(obj):
    return isinstance(obj, dict) and all([isinstance(x, SSparseMatrix) for x in obj.values()])


def is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def is_scored_tags_dict(obj):
    return isinstance(obj, dict) and \
           all([isinstance(x, str) for x in obj.keys()]) and \
           all([isinstance(x, int) or isinstance(x, float) for x in obj.values()])


# ======================================================================
# Class definition
# ======================================================================
class SparseMatrixRecommender:
    _matrices = None
    _M = None
    _itemNames = None
    _tags = None
    _tagTypeWeights = None
    _data = None
    _value = None

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------
    def __init__(*args):
        if len(args) == 1 and isinstance(args[0], pandas.core.frame.DataFrame):
            _data = args[0]
        elif len(args) == 1 and is_smat_dict(args[0]):
            _matrices = args[0]

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------
    def take_M(self):
        return self._M

    def take_matrices(self):
        return self._matrices

    def take_value(self):
        return self._value

    def take_data(self):
        return self._data

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------
    def set_M(self, arg):
        if is_sparse_matrix(arg):
            self._M = arg
        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")
            return None
        return self

    def set_matrices(self, arg):
        if is_smat_dict(arg):
            self._matrices = arg
        else:
            raise TypeError("The first argument is expected to be a dictionary of SSparseMatrix objects.")
            return None
        return self

    def set_value(self, arg):
        self._value = arg
        return self

    def set_data(self, arg):
        self._data = arg
        return self

    # ------------------------------------------------------------------
    # Create with matrices
    # ------------------------------------------------------------------
    def create_from_matrices(self, matrices,
                             add_tag_types_to_column_names=False,
                             tag_value_separator=":",
                             numerical_columns_as_categorical=False):

        if not is_smat_dict(matrices):
            raise TypeError("The first argument is expected to be a dictionary of SSparseMatrix objects.")
            return None

        if add_tag_types_to_column_names:
            self._matrices = {k: v.set_column_names([k + tag_value_separator + y for y in v.column_names()]) for (k, v) in matrices.items()}
        else:
            self._matrices = matrices

        self._M = column_bind(self._matrices)

        return self

    # ------------------------------------------------------------------
    # Create form wide form
    # ------------------------------------------------------------------
    def create_from_wide_form(self, data, item_column_name, columns,
                              add_tag_types_to_column_names=False,
                              tag_value_separator=":",
                              numerical_columns_as_categorical=False):

        if not isinstance(data, pandas.core.frame.DataFrame):
            raise TypeError("The first argument is expected to be data frame.")
            return None

        # Make a set of column names
        dataColNames = set(data.keys())

        # Check if the specified item column name is known
        if item_column_name not in dataColNames:
            raise TypeError("Unknown item column name: " + repr(item_column_name) + ".")
            return None

        # Get automatic columns
        if isinstance(columns, type(None)):
            columns = [k for k in data.keys() if k != item_column_name]

        if not is_str_list(columns):
            raise TypeError("""The second argument is expected to be a list of strings.""")
            return None

        # Create a dictionary of matrices
        for cn in columns:
            if cn not in dataColNames:
                raise TypeError("Unknown column name: " + repr(cn) + ".")
                return None

        # Cross tabulate across all specified columns
        aSMats = cross_tabulate(data=data, index=item_column_name, columns=columns)

        # Delegate creation
        return self.create_from_matrices(matrices=aSMats,
                                         add_tag_types_to_column_names=add_tag_types_to_column_names,
                                         tag_value_separator=tag_value_separator,
                                         numerical_columns_as_categorical=numerical_columns_as_categorical)

    # ------------------------------------------------------------------
    # Create form long form
    # ------------------------------------------------------------------
    def create_from_long_form(self, data,
                              item_column_mame="Item",
                              tag_type_column_name="TagType",
                              tag_column_name="Tag",
                              weight_column_name="Weight",
                              add_tag_types_to_column_names=False,
                              tag_value_separator=":",
                              numerical_columns_as_categorical=False):

        if not isinstance(data, pandas.core.frame.DataFrame):
            raise TypeError("""The first argument is expected to be data frame with columns that correspond
            to items, tag type, tag values, and tag weights.""")
            return None

        # We make a dictionary of matrices and hand it over to create_from_matrices.

        # Group by tag type
        gb = data.groupby(tag_type_column_name)

        # Cross tabulate the data frame subset for each tag type
        aSMats = {x: cross_tabulate(gb.get_group(x),
                                    index=item_column_mame,
                                    columns=tag_column_name,
                                    values=weight_column_name) for x in gb.groups}

        # Find all row names
        all_row_names = []
        for rns in [x.row_names() for x in aSMats.values()]:
            all_row_names += rns
        all_row_names = list(set(all_row_names))

        # Impose row names over each matrix
        aSMats = {k: v.impose_row_names(all_row_names) for (k, v) in aSMats.items()}

        # Delegate creation
        return self.create_from_matrices(matrices=aSMats,
                                         add_tag_types_to_column_names=add_tag_types_to_column_names,
                                         tag_value_separator=tag_value_separator,
                                         numerical_columns_as_categorical=numerical_columns_as_categorical)

    # ------------------------------------------------------------------
    # Apply LSI functions
    # ------------------------------------------------------------------
    def apply_term_weight_functions(self,
                                    global_weight_func="IDF",
                                    local_weight_func="None",
                                    normalizer_func="Cosine"):

        self._matrices = {k: apply_term_weight_functions(v, global_weight_func, local_weight_func, normalizer_func) for
                          (k, v) in self._matrices.items()}

        self._M = column_bind(self._matrices)

        return self

    # ------------------------------------------------------------------
    # To smr vector
    # ------------------------------------------------------------------
    def _to_smr_vector(self, arg, things_dict, thing_name, ref_name):

        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")
            return None

        if is_str_list(arg):
            dvec = dict.fromkeys(arg, 1)
            return self._to_smr_vector(dvec, things_dict, thing_name, ref_name)
        elif is_scored_tags_dict(arg):
            known_keys = {key: value for (key, value) in arg.items() if key in things_dict}
            if len(known_keys) == 0:
                raise LookupError("None of the tags is a valid recommendation matrix " + thing_name + " name.")
                return None
            elif len(known_keys) < len(arg):
                raise LookupError("Not all tags are valid recommendation matrix " + thing_name + " names.")

            res_row_inds = [things_dict[k] for (k, v) in known_keys.items()]
            res_col_inds = [0 for x in range(len(res_row_inds))]
            res_vals = list(known_keys.values())
            smat = scipy.sparse.csr_matrix((res_vals, (res_row_inds, res_col_inds)), shape=(len(things_dict), 1))
            res = SSparseMatrix(smat)
            res.set_row_names(list(things_dict.keys()))
            res.set_column_names()
            self.set_value(res)
            return self
        else:
            raise TypeError(
                "The first argument is expected to be a list of " + ref_name + ", a dictionary of scored "
                + ref_name + "," + " or SSparseMatrix object.")
            return None

    # ------------------------------------------------------------------
    # To profile vector
    # ------------------------------------------------------------------
    def to_profile_vector(self, arg):

        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")
            return None

        return self._to_smr_vector(arg, things_dict=self._M.column_names_dict(), thing_name="column", ref_name="tags")

    # ------------------------------------------------------------------
    # To history vector
    # ------------------------------------------------------------------
    def to_history_vector(self, arg):

        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")
            return None

        return self._to_smr_vector(arg, things_dict=self._M.row_names_dict(), thing_name="row", ref_name="items")

    # ------------------------------------------------------------------
    # Recommend by profile
    # ------------------------------------------------------------------
    def recommend_by_profile(self, profile, nrecs=10):

        # Make scored tags vector
        if isinstance(profile, str):
            vec = self.to_profile_vector([profile]).take_value()
        elif isinstance(profile, dict) or isinstance(profile, list):
            vec = self.to_profile_vector(profile).take_value()
        elif is_sparse_matrix(profile):
            vec = profile
        else:
            raise TypeError("The first argument is expected to be a list of tags or a dictionary of scored tags.")
            return None

        # Compute the recommendations
        recs = self.take_M().dot(vec)

        # Take non-zero score recommendations
        recs = {key: value for (key, value) in recs.row_sums_dict().items() if value > 0}

        # Reverse sort
        recs = dict(sorted(recs.items(), key=lambda item: -item[1]))

        # Give top-n recs
        if isinstance(nrecs, int) and nrecs < len(recs):
            recs = dict(list(recs.items())[0:nrecs])
        elif not (isinstance(None, type(None)) or isinstance(nrecs, int) and nrecs > 0):
            raise TypeError("The second argument, nrecs, is expected to be an integer or None.")
            return None

        # Assign obtained recommendations to the pipeline value
        self.set_value(recs)

        return self

    # ------------------------------------------------------------------
    # Recommend by history
    # ------------------------------------------------------------------
    def recommend(self, history, nrecs=10, remove_history=True):

        # Make scored items vector
        if isinstance(history, str):
            vec = self.to_history_vector([history]).take_value().transpose()
        elif isinstance(history, dict) or isinstance(history, list):
            vec = self.to_history_vector(history).take_value().transpose()
        elif is_sparse_matrix(history):
            vec = history
        else:
            raise TypeError("The first argument is expected to be a list of items, a dictionary of scored items" +
                            " or a SSparseMatrix object with " + self._M.rows_count() + " columns.")
            return None

        # Compute the recommendations
        recs = self.take_M().dot(vec.dot(self.take_M()).transpose())

        # Take non-zero scores recommendations
        recs = {key: value for (key, value) in recs.row_sums_dict().items() if value > 0}

        # Remove history
        if remove_history:
            hist_set = vec.column_sums_dict()
            hist_set = set({key for (key, value) in hist_set.items() if value > 0})

            recs = {key: value for (key, value) in recs.items() if not key in hist_set}

        # Reverse sort
        recs = dict(sorted(recs.items(), key=lambda item: -item[1]))

        # Give top-n recs
        if isinstance(nrecs, int) and nrecs < len(recs):
            recs = dict(list(recs.items())[0:nrecs])
        elif not (isinstance(None, type(None)) or isinstance(nrecs, int) and nrecs > 0):
            raise TypeError("The second argument, nrecs, is expected to be an integer or None.")
            return None

        # Assign obtained recommendations to the pipeline value
        self.set_value(recs)

        return self

    # ------------------------------------------------------------------
    # Profile
    # ------------------------------------------------------------------
    def profile(self, history):

        # Make scored items vector
        if isinstance(history, str):
            vec = self.to_history_vector([history]).take_value().transpose()
        elif isinstance(history, dict) or isinstance(history, list):
            vec = self.to_history_vector(history).take_value().transpose()
        elif is_sparse_matrix(history):
            vec = history
        else:
            raise TypeError("The first argument is expected to be a list of items, a dictionary of scored items" +
                            " or a SSparseMatrix object with " + self._M.rows_count() + " columns.")
            return None

        # Compute the profile
        prof = vec.dot(self.take_M())

        # Take non-zero scores tags
        prof = {key: value for (key, value) in prof.column_sums_dict().items() if value > 0}

        # Reverse sort
        prof = dict(sorted(prof.items(), key=lambda item: -item[1]))

        # Assign obtained prof to the pipeline value
        self.set_value(prof)

        return self

    # ------------------------------------------------------------------
    # Join across
    # ------------------------------------------------------------------
    def join_across(self, data, on):

        if not isinstance(self.take_value(), dict):
            raise TypeError("The pipeline value is expected to be a dictionary of scored items.")
            return None

        if not isinstance(data, pandas.core.frame.DataFrame):
            raise TypeError("The first argument is expected to be a data frame.")
            return None

        if not isinstance(on, str):
            raise TypeError("The second argument expected to be a string.")
            return None

        # Make a data frame from the recommendations in the pipeline value
        recs = self.take_value()
        dfRecs = pandas.DataFrame()
        dfRecs[on] = list(recs.keys())
        dfRecs["Score"] = list(recs.values())

        # Left join recommendations with the given data frame
        # Using .join does not work because .join uses indexes.
        # Hence using merge
        self.set_value(dfRecs.merge(data, on=on, how="left"))

        return self

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------
    def __str__(self):
        k = 0
        res = "SparseMatrixRecommender object with %d tag types:" % len(self._matrices)
        for m in self._matrices:
            res = res + "\n" + str(k) + ". tag type: " + m + "\n"
            res = res + repr(self._matrices[m])
            k = k + 1
        return res

    def __repr__(self):
        return "<Sparse matrix recommender object with matrix dimensions %dx%d\n" \
               "\tand with %d tag types>" % \
               (self._M.sparse_matrix().shape + (len(self._matrices),))