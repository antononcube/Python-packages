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
    def create_from_matrices(self, smats, addTagTypesToColumnNames=False, tagValueSeparator=":", numericalColumnsAsCategorical=False):

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
    # To profile vector
    # ------------------------------------------------------------------
    def to_profile_vector(self, arg):

        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")
            return None

        if is_str_list(arg):
            dvec = dict.fromkeys(arg, 1)
            return self.to_profile_vector(dvec)
        elif is_scored_tags_dict(arg):
            known_keys = {key: value for (key, value) in arg.items() if key in self._M.column_names_dict()}
            if len(known_keys) == 0:
                raise LookupError("None of the tags is a valid recommendation matrix column name.")
                return None
            elif len(known_keys) < len(arg):
                raise LookupError("Not all tags are valid recommendation matrix column names.")

            res_row_inds = [self._M.column_names_dict()[k] for (k, v) in known_keys.items()]
            res_col_inds = [0 for x in range(len(res_row_inds))]
            res_vals = list(known_keys.values())
            smat = scipy.sparse.csr_matrix((res_vals, (res_row_inds, res_col_inds)), shape=(self._M.columns_count(), 1))
            res = SSparseMatrix(smat)
            res.set_row_names(self._M.column_names())
            res.set_column_names()
            self.set_value(res)
            return self
        else:
            raise TypeError(
                "The first argument is expected to be a list of tags, a dictionary of scored tags," +
                " or SSparseMatrix objects.")
            return None

    # ------------------------------------------------------------------
    # Recommend by profile
    # ------------------------------------------------------------------
    def recommend_by_profile(self, profile):
        if isinstance(profile, dict) or isinstance(profile, list):
            vec = self.to_profile_vector(profile).take_value()
        elif is_sparse_matrix(profile):
            vec = profile
        else:
            raise TypeError("The first argument is expected to be a list of tags or a dictionary of scored tags.")
            return None

        recs = self.take_M().dot(vec)
        recs = {key: value for (key, value) in recs.row_sums_dict().items() if value > 0}
        recs = dict(sorted(recs.items(), key=lambda item: -item[1]))
        self._value = recs
        return self
