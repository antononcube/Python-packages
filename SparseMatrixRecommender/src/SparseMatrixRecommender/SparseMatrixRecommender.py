from SSparseMatrix.src.SSparseMatrix import SSparseMatrix
from SSparseMatrix.src.SSparseMatrix import is_sparse_matrix
from SparseMatrixRecommender.src.SparseMatrixRecommender import CrossTabulate
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
    def create_from_matrices(self, smats, addTagTypesToColumnNames=False, tagValueSeparator=":",
                             numericalColumnsAsCategorical=False):

        if not is_smat_dict(smats):
            raise TypeError("The first argument is expected to be a dictionary of SSparseMatrix objects.")
            return None

        self._M = None
        for k in smats:
            if is_sparse_matrix(self._M):
                self._M = self._M.column_bind(smats[k])
            else:
                self._M = smats[k]

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
