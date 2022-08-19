from SSparseMatrix import SSparseMatrix
from SSparseMatrix import column_bind
from SSparseMatrix import is_s_sparse_matrix
from .CrossTabulate import cross_tabulate
from .DocumentTermWeightFunctions import apply_term_weight_functions
import pandas
import scipy
import warnings


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


def _get_non_zero_columns(ssmat):
    smat = ssmat.sparse_matrix().tocoo()
    cns = ssmat.column_names()
    cns2 = [cns[i] for i in smat.col]
    return dict(zip(cns2, smat.data))


def _get_non_zero_rows(ssmat):
    smat = ssmat.sparse_matrix().tocoo()
    rns = ssmat.row_names()
    rns2 = [rns[i] for i in smat.row]
    return dict(zip(rns2, smat.data))


def _reverse_sort_dict(x):
    return dict([(k, v) for k, v in sorted(x.items(), key=lambda item: -item[1])])


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
    def __init__(self, *args, **kwargs):
        """Creation of a SparseMatrixObject object.
           The first (optional) argument is expected to be a data frame or a dictionary of SSparseMatrix objects.
        """
        if len(args) == 1 and isinstance(args[0], pandas.core.frame.DataFrame):
            _data = args[1]
        elif len(args) == 1 and is_smat_dict(args[0]):
            obj = SparseMatrixRecommender().create_from_matrices(args[0])
            self.set_matrices(obj.take_matrices())
            self.set_M(obj.take_M())
            self.set_tag_type_weights(obj.take_tag_type_weights())
            self.set_data(obj.take_data())
            self.set_value(obj.take_value())

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------
    def take_M(self):
        """Take the recommendation matrix."""
        return self._M

    def take_matrices(self):
        """Take the tag-type sub-matrices."""
        return self._matrices

    def take_tag_type_weights(self):
        """Take the tag type weights."""
        return self._tagTypeWeights

    def take_data(self):
        """Take data."""
        return self._data

    def take_value(self):
        """Take the pipeline value."""
        return self._value

    def sub_matrix(self, tag_type):
        """Take sub-matrix corresponding to tag_type."""
        if not isinstance(tag_type, str):
            raise ValueError("The first argument, tag_type, is expected to be a string.")

        if not tag_type in self.take_matrices():
            raise ValueError("The tag type " + str(tag_type) + " is not known in the recommender.")

        return self.take_matrices()[tag_type]

    # ------------------------------------------------------------------
    # Echoers
    # ------------------------------------------------------------------
    def echo_M(self):
        """Echo the recommendation matrix."""
        print(self._M)
        return self

    def echo_matrices(self):
        """Echo the tag-type sub-matrices."""
        print(self._matrices)
        return self

    def echo_tag_type_weights(self):
        """Echo the tag type weights."""
        print(self._tagTypeWeights)
        return self

    def echo_data(self):
        """Echo data."""
        print(self._data)
        return self

    def echo_value(self):
        """Echo the pipeline value."""
        print(self._value)
        return self

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------
    def set_M(self, arg):
        """Set recommendation matrix."""
        if is_s_sparse_matrix(arg):
            self._M = arg
        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")

        return self

    def set_matrices(self, arg):
        """Set recommendation sub-matrices."""
        if is_smat_dict(arg):
            self._matrices = arg
        else:
            raise TypeError("The first argument is expected to be a dictionary of SSparseMatrix objects.")

        return self

    def set_tag_type_weights(self, arg):
        """Set the tag type weights."""
        self._tagTypeWeights = arg
        return self

    def set_data(self, arg):
        """Set data."""
        self._data = arg
        return self

    def set_value(self, arg):
        """Set pipeline value."""
        self._value = arg
        return self

    # ------------------------------------------------------------------
    # Create with matrices
    # ------------------------------------------------------------------
    def create_from_matrices(self, matrices: dict,
                             add_tag_types_to_column_names=False,
                             tag_value_separator=":",
                             numerical_columns_as_categorical=False):
        """Create the recommendation matrix from tag type sub-matrices.

        :type matrices: dict
        :param matrices: Tag type sub-matrices.
        :param add_tag_types_to_column_names: Should tag types be used as prefixes or not?
        :param tag_value_separator: String to separate tag-type prefixes from tags
                                   (in the column names of the recommendation matrix).
        :param numerical_columns_as_categorical: Should numerical columns be turned into categorical or not?
        :return: self: SparseMatrixObject
        """
        if not is_smat_dict(matrices):
            raise TypeError("The first argument is expected to be a dictionary of SSparseMatrix objects.")

        if add_tag_types_to_column_names:
            self._matrices = {k: v.set_column_names([k + tag_value_separator + y for y in v.column_names()]) for (k, v)
                              in matrices.items()}
        else:
            self._matrices = matrices

        self._M = column_bind(self._matrices)

        return self

    # ------------------------------------------------------------------
    # Create form wide form
    # ------------------------------------------------------------------
    def create_from_wide_form(self, data, item_column_name,
                              columns=None,
                              add_tag_types_to_column_names=False,
                              tag_value_separator=":",
                              numerical_columns_as_categorical=False):
        """Create the recommendation matrix from wide form data frame.

        :param data: A data frame with wide form(at) data.
        :param item_column_name: Name of the column with the items.
        :param columns: Which columns to use for making the recommendations matrix.
        :param add_tag_types_to_column_names: Should tag types be used as prefixes or not?
        :param tag_value_separator: String to separate tag-type prefixes from tags
                                   (in the column names of the recommendation matrix).
        :param numerical_columns_as_categorical: Should numerical columns be turned into categorical or not?
        :return: self: SparseMatrixObject
        """
        if not isinstance(data, pandas.core.frame.DataFrame):
            raise TypeError("The first argument is expected to be data frame.")

        # Make a set of column names
        dataColNames = set(data.keys())

        # Check if the specified item column name is known
        if item_column_name not in dataColNames:
            raise TypeError("Unknown item column name: " + repr(item_column_name) + ".")

        # Get automatic columns
        if isinstance(columns, type(None)):
            columns = [k for k in data.keys() if k != item_column_name]

        if not is_str_list(columns):
            raise TypeError("""The second argument is expected to be a list of strings.""")

        # Create a dictionary of matrices
        for cn in columns:
            if cn not in dataColNames:
                raise TypeError("Unknown column name: " + repr(cn) + ".")

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
                              item_column_name="Item",
                              tag_type_column_name="TagType",
                              tag_column_name="Tag",
                              weight_column_name="Weight",
                              add_tag_types_to_column_names=False,
                              tag_value_separator=":",
                              numerical_columns_as_categorical=False):
        """Create the recommendation matrix from long form data frame.

        :param data: A data frame with long form(at) data.
        :param item_column_name: Name of the column with the items.
        :param tag_type_column_name: Name of the column with the tag types.
        :param tag_column_name: Name of the column with the tags.
        :param weight_column_name: Name of the column with the tag weights.
        :param add_tag_types_to_column_names: Should tag types be used as prefixes or not?
        :param tag_value_separator: String to separate tag-type prefixes from tags
                                   (in the column names of the recommendation matrix).
        :param numerical_columns_as_categorical: Should numerical columns be turned into categorical or not?
        :return: self: SparseMatrixObject
        """
        if not isinstance(data, pandas.core.frame.DataFrame):
            raise TypeError("""The first argument is expected to be data frame with columns that correspond
            to items, tag type, tag values, and tag weights.""")

        # We make a dictionary of matrices and hand it over to create_from_matrices.

        # Group by tag type
        gb = data.groupby(tag_type_column_name)

        # Cross tabulate the data frame subset for each tag type
        aSMats = {x: cross_tabulate(gb.get_group(x),
                                    index=item_column_name,
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
        """Apply LSI functions to the entries of the recommendation matrix.

        :param global_weight_func: LSI global term weight function. One of "ColumnSum", "Entropy", "IDF", "None".
        :param local_weight_func: LSI local term weight function. One of "Binary", "Log", "None".
        :param normalizer_func: LSI normalizer function. One of "Cosine", "None", "RowSum".
        :return: self: SparseMatrixObject
        """
        self._matrices = {k: apply_term_weight_functions(v, global_weight_func, local_weight_func, normalizer_func) for
                          (k, v) in self._matrices.items()}

        self._M = column_bind(self._matrices)

        return self

    # ------------------------------------------------------------------
    # To smr vector
    # ------------------------------------------------------------------
    def _to_smr_vector(self, arg, things_dict, thing_name, ref_name, ignore_unknown=False):
        """To SMR vector

        :type arg: str|dict
        :param arg: A list of items or tags, or a dictionary of scored items or tags.

        :param things_dict: Set items or tags.

        :param thing_name: Which matrix axis, one of "column" or "row"

        :type ref_name: bool
        :param ref_name: Reference name, one of "item" or "tag"

        :type ignore_unknown: bool
        :param ignore_unknown: Should unknown items or tags be ignored or not?

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")

        if is_str_list(arg):
            dvec = dict.fromkeys(arg, 1)
            return self._to_smr_vector(dvec, things_dict, thing_name, ref_name, ignore_unknown=ignore_unknown)
        elif is_scored_tags_dict(arg):
            known_keys = {key: value for (key, value) in arg.items() if key in things_dict}
            if len(known_keys) == 0:
                raise LookupError("None of the tags is a valid recommendation matrix " + thing_name + " name.")
            elif len(known_keys) < len(arg) and not ignore_unknown:
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

    # ------------------------------------------------------------------
    # To profile vector
    # ------------------------------------------------------------------
    def to_profile_vector(self, arg, ignore_unknown=False):
        """Convert a list or a dictionary into a profile SSparseMatrix (with one column.)

        :type arg: str|list|dict
        :param arg: A tag, a list of tags, or dictionary of scored tags.

        :type ignore_unknown: bool
        :param ignore_unknown: Should unknown tags be ignored or not?

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")

        return self._to_smr_vector(arg,
                                   things_dict=self._M.column_names_dict(),
                                   thing_name="column",
                                   ref_name="tags",
                                   ignore_unknown=ignore_unknown)

    # ------------------------------------------------------------------
    # To history vector
    # ------------------------------------------------------------------
    def to_history_vector(self, arg, ignore_unknown=False):
        """Convert a list or a dictionary into a profile SSparseMatrix (with one column.)

        :type arg: str|list|dict
        :param arg: A item, a list of item, or dictionary of scored items.

        :type ignore_unknown: bool
        :param ignore_unknown: Should unknown items be ignored or not?

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")

        return self._to_smr_vector(arg,
                                   things_dict=self._M.row_names_dict(),
                                   thing_name="row",
                                   ref_name="items",
                                   ignore_unknown=ignore_unknown)

    # ------------------------------------------------------------------
    # Recommend by profile
    # ------------------------------------------------------------------
    def recommend_by_profile(self, profile, nrecs=10, normalize=True, ignore_unknown=False,
                             vector_result: bool = False):
        """Recommend by profile.

        :type profile: str|list|dict
        :param profile: A tag, a list of tags, a dictionary of scored tags.

        :type nrecs: int|None
        :param nrecs: A positive integer or None. If it is None, then all items with non-zero scores are returned.

        :type normalize: bool
        :param normalize: Should the result be normalized or not.

        :type ignore_unknown: bool
        :param ignore_unknown: Should the unknown tags be ignored or not?

        :type vector_result: bool
        :param vector_result: Should the result be a (SSparseMatrix) vector or a dictionary.

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        # Make scored tags vector
        if isinstance(profile, str):
            vec = self.to_profile_vector([profile], ignore_unknown=ignore_unknown).take_value()
        elif isinstance(profile, dict) or isinstance(profile, list):
            vec = self.to_profile_vector(profile, ignore_unknown=ignore_unknown).take_value()
        elif is_s_sparse_matrix(profile):
            vec = profile
        else:
            raise TypeError("The first argument is expected to be a list of tags or a dictionary of scored tags.")

        # Ignore unknown tags
        # Compute the recommendations
        recs = self.take_M().dot(vec)

        # Normalize
        recs_max = max(map(abs, recs.row_sums()))
        if normalize and recs_max > 0:
            recs = recs.multiply(1 / recs_max)

        if vector_result:
            # Vector result

            # Change the matrix to have nrecs columns
            # according to scores
            if isinstance(nrecs, int) and nrecs < recs.rows_count():
                recs2 = recs.row_sums_dict()
                recs2 = _reverse_sort_dict(recs2)

                recs2 = dict(list(recs2.items())[0:nrecs])
                rowNames = recs.row_names()
                recs = recs[list(recs2.keys()), :]
                recs = recs.impose_row_names(rowNames)

        else:
            # Dictionary result
            # Take non-zero score recommendations
            recs = {key: value for (key, value) in recs.row_sums_dict().items() if value > 0}

            # Reverse sort
            recs = dict(sorted(recs.items(), key=lambda item: -item[1]))

            # Give top-n recs
            if isinstance(nrecs, int) and nrecs < len(recs):
                recs = dict(list(recs.items())[0:nrecs])
            elif not (isinstance(None, type(None)) or isinstance(nrecs, int) and nrecs > 0):
                raise TypeError("The second argument, 'nrecs', is expected to be a positive integer or None.")

        # Assign obtained recommendations to the pipeline value
        self.set_value(recs)

        return self

    # ------------------------------------------------------------------
    # Recommend by history
    # ------------------------------------------------------------------
    def recommend(self, history, nrecs=10, normalize=True, remove_history=True):
        """Recommend by history.

        :type history: str|list|dict
        :param history: An item (string), a list of items, a dictionary of scored items.

        :type nrecs: int|None
        :param nrecs: A positive integer or None. If it is None, then all items with non-zero scores are returned.

        :type normalize: bool
        :param normalize: Should the result be normalized or not.

        :type remove_history: bool
        :param remove_history: Should the the history be removed from the result recommendations or not?

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        # Make scored items vector
        if isinstance(history, str):
            vec = self.to_history_vector([history]).take_value().transpose()
        elif isinstance(history, dict) or isinstance(history, list):
            vec = self.to_history_vector(history).take_value().transpose()
        elif is_s_sparse_matrix(history):
            vec = history
        else:
            raise TypeError("The first argument is expected to be a list of items, a dictionary of scored items" +
                            " or a SSparseMatrix object with " + self._M.rows_count() + " columns.")

        # Compute the recommendations
        recs = self.take_M().dot(vec.dot(self.take_M()).transpose(copy=False))

        # Take non-zero scores recommendations
        recs = {key: value for (key, value) in recs.row_sums_dict().items() if value > 0}

        # Remove history
        if remove_history:
            hist_set = vec.column_sums_dict()
            hist_set = set({key for (key, value) in hist_set.items() if value > 0})

            recs = {key: value for (key, value) in recs.items() if key not in hist_set}

        # Reverse sort
        recs = _reverse_sort_dict(recs)

        # Give top-n recs
        if isinstance(nrecs, int) and nrecs < len(recs):
            recs = dict(list(recs.items())[0:nrecs])

            # Normalize
            recs_max = max(map(abs, recs.values()))
            if normalize and recs_max > 0:
                recs = {k: v / recs_max for (k, v) in recs.items()}

        elif not (isinstance(None, type(None)) or isinstance(nrecs, int) and nrecs > 0):
            raise TypeError("The second argument, nrecs, is expected to be a positive integer or None.")

        # Assign obtained recommendations to the pipeline value
        self.set_value(recs)

        return self

    # ------------------------------------------------------------------
    # Profile
    # ------------------------------------------------------------------
    def profile(self, history):
        """Profile of a history.

        :type history: str|list|dict
        :param history: An item (string), a list of items, a dictionary of scored items.

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        # Make scored items vector
        if isinstance(history, str):
            vec = self.to_history_vector([history]).take_value().transpose()
        elif isinstance(history, dict) or isinstance(history, list):
            vec = self.to_history_vector(history).take_value().transpose()
        elif is_s_sparse_matrix(history):
            vec = history
        else:
            raise TypeError("The first argument is expected to be a list of items, a dictionary of scored items" +
                            " or a SSparseMatrix object with " + self._M.rows_count() + " columns.")

        # Compute the profile
        prof = vec.dot(self.take_M())

        # Take non-zero scores tags
        prof = {key: value for (key, value) in prof.column_sums_dict().items() if value > 0}

        # Reverse sort
        prof = _reverse_sort_dict(prof)

        # Assign obtained prof to the pipeline value
        self.set_value(prof)

        return self

    # ------------------------------------------------------------------
    # Filter by profile
    # ------------------------------------------------------------------
    def filter_by_profile(self,
                          profile,
                          filter_type="intersection",
                          ignore_unknown=False):
        """
        Filter by profile
        -----------------
        The result is a vector of scored items that is assigned to \code{smrObj$Value}.
        If filter_type is "union" each item that has at least one of the tags in profile is in the result.
        (Essentially, that is the same as taking all non-zero score recommendations by profile.)
        If filter_type is "intersection" each item in the result has all tags in profile.

        :param profile: A profile specification used to filter with.
        :param filter_type: The type of filtering one of "union" or "intersection".
        :param ignore_unknown:
        :return self: The object itself or None. The result is stored in self._value.
        """

        # Make scored tags vector
        if isinstance(profile, str):
            vec = self.to_profile_vector([profile], ignore_unknown=ignore_unknown).take_value()
        elif isinstance(profile, dict) or isinstance(profile, list):
            vec = self.to_profile_vector(profile, ignore_unknown=ignore_unknown).take_value()
        elif is_s_sparse_matrix(profile):
            vec = profile
        else:
            raise TypeError("The first argument is expected to be a list of tags or a dictionary of scored tags.")

        # Unitize
        profileVec = vec.unitize()

        # Find the items corresponding to the profile and type spec
        if isinstance(filter_type, str) and filter_type.lower() == "union":

            sVec = self.recommend_by_profile(profileVec, nrecs=None).take_value()
            sVec = sVec.keys()

        elif isinstance(filter_type, str) and filter_type.lower() == "intersection":

            sVec = self.take_M().unitize().dot(profileVec).row_sums_dict()

            n = profileVec.column_sums()[0]
            sVec = [k for (k, v) in sVec.items() if v >= n]
        else:
            raise TypeError("The argument filter_type is expected to be one of \"union\" or \"intersection\".")

        # Result
        self.set_value(sVec)
        return self

    # ------------------------------------------------------------------
    # Retrieve by query elements
    # ------------------------------------------------------------------
    def retrieve_by_query_elements(self,
                                   should=[],
                                   must=[],
                                   must_not=[],
                                   must_type="intersection",
                                   must_not_type="union",
                                   ignore_unknown=False):
        """
        Retrieve by query elements
        --------------------------
        Applies a profile filter to the rows of the recommendation matrix.
 
        :param should: A profile specification used to recommend with.
        :param must: A profile specification used to filter with. The items in the result must have the tags in the given list.
        :param must_not: A profile specification used to filter with. The items in the result must not have the tags in given list
        :param must_type: The type of filtering with the must tags; one of "union" or "intersection".
        :param must_not_type: The type of filtering with the must not tags; one of "union" or "intersection".
        :param ignore_unknown: Should the unknown tags be ignored or not?
        :return self:  The object itself or None. The result is stored in self._value.
        """

        if not is_str_list(should):
            raise TypeError("The first argument, should, is expected to be a list of tags.")

        if not is_str_list(must):
            raise TypeError("The second argument, must, is expected to be a list of tags.")

        if not is_str_list(must_not):
            raise TypeError("The third argument, must_not, is expected to be a list of tags.")

        if len(should) + len(must) + len(must_not) == 0:
            warnings.warn("All query elements are empty.")
            return self

        # Should
        if len(should) > 0 and len(must) > 0:
            # Both should and must are present
            pVecShould = self.to_profile_vector(should, ignore_unknown=ignore_unknown).take_value()
            pVecMust = self.to_profile_vector(must, ignore_unknown=ignore_unknown).take_value()

            shouldItems = self.recommend_by_profile(pVecShould.add(pVecMust),
                                                    nrecs=None,
                                                    ignore_unknown=ignore_unknown).take_value()

        elif len(should) > 0 and len(must) == 0 and len(must_not) == 0:
            # Only should is not empty

            pVecShould = self.to_profile_vector(should, ignore_unknown=ignore_unknown).take_value()
            self.recommend_by_profile(pVecShould,
                                      nrecs=None,
                                      ignore_unknown=ignore_unknown)

            return self

        else:
            shouldItems = dict.fromkeys(self.take_M().row_names(), 1)

        res = shouldItems

        # Must
        if len(must) > 0:
            mustItems = self.filter_by_profile(must,
                                               filter_type=must_type,
                                               ignore_unknown=ignore_unknown).take_value()

            if len(mustItems) == 0:
                warnings.warn("No items were obtained by querying with the must tags.")

        else:
            mustItems = []

        if len(mustItems) > 0:
            res = set.intersection(set(res), set(mustItems))

        # Must not
        if len(must_not) > 0:
            mustNotItems = self.filter_by_profile(must_not,
                                                  filter_type=must_not_type,
                                                  ignore_unknown=ignore_unknown).take_value()

            if len(mustNotItems) == 0:
                warnings.warn("No items were obtained by querying with the must not tags.")

        else:
            mustNotItems = []

        if len(mustNotItems) > 0:
            res = set.difference(set(res), set(mustNotItems))

        # Result
        self.set_value(dict.fromkeys(res, 1))
        return self

    # ------------------------------------------------------------------
    # Join across
    # ------------------------------------------------------------------
    def join_across(self, data, on=None):
        """Join recommendations dictionary (scored items) with a corresponding data frame.

        :type data: pandas.core.DataFrame
        :param data: A data frame.

        :type on: str|None
        :param on: Field corresponding to the items, i.e. row-names of self._M.

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        if not isinstance(self.take_value(), dict):
            raise TypeError("The pipeline value is expected to be a dictionary of scored items.")

        if not isinstance(data, pandas.core.frame.DataFrame):
            raise TypeError("The first argument is expected to be a data frame.")

        if not (isinstance(on, str) or isinstance(on, type(None))):
            raise TypeError("The second argument expected to be a string.")

        # Automatic on values
        mon = on
        if isinstance(on, type(None)):
            mon = [x for x in list(data.columns) if x.lower() == "id"]
            mon = data.columns[0] if len(mon) == 0 else mon[0]

        # Make a data frame from the recommendations in the pipeline value
        recs = self.take_value()
        dfRecs = pandas.DataFrame()
        dfRecs[mon] = list(recs.keys())
        dfRecs["Score"] = list(recs.values())

        # Left join recommendations with the given data frame
        # Using .join does not work because .join uses indexes.
        # Hence, using merge.
        self.set_value(dfRecs.merge(data, on=mon, how="left"))

        return self

    # ------------------------------------------------------------------
    # Remove tag types
    # ------------------------------------------------------------------
    def remove_tag_types(self,
                         tag_types,
                         warn: bool = True):
        """Remove tag types.

        :type tag_types: str|list
        :param tag_types: A list of tag types to be removed from the SMR object.

        :type warn: bool
        :param warn: Should warning messages be issued or not?

        :rtype SparseMatrixRecommender
        :return self: The object itself or None.
        """

        # There are several ways to do this:
        # 1. Work with newSMR$TagTypeRanges, take the indices corresponding to tag types not to be removed.
        # 2. Construct a metadata matrix by taking sub-matrices of the tag types not to be removed.

        removeTagTypes = tag_types

        # Process tag_types
        if isinstance(removeTagTypes, str):
            removeTagTypes = [removeTagTypes, ]

        if not is_str_list(removeTagTypes):
            raise ValueError("The argument tag_types is expected to be a string or a list of strings.")

        tagTypes = list(self.take_matrices().keys())
        tagTypesKnown = list(set.intersection(set(tagTypes), set(removeTagTypes)))

        if len(tagTypesKnown) == 0:
            raise ValueError("None of the specified tag types is a known tag type in the recommender object.")

        if len(tagTypesKnown) < len(tagTypes):
            warnings.warn("Some tags are not known in the recommender.")

        tagTypes = set.difference(set(tagTypes), set(removeTagTypes))

        res = SparseMatrixRecommender({t: self.take_matrices()[t] for t in tagTypes})

        return res

    # ------------------------------------------------------------------
    # Classify by profile
    # ------------------------------------------------------------------
    def classify_by_profile(self, tag_type, profile,
                            n_top_nearest_neighbors=100,
                            voting=False,
                            drop_zero_scored_labels=True,
                            max_number_of_labels=None,
                            normalize: bool = True,
                            ignore_unknown: bool = False):
        """Classify by profile vector.

        :type tag_type: str
        :param tag_type: Tag type to classify to.

        :type profile: str|list|dict
        :param profile: A tag, a list of tags, a dictionary of scored tags.

        :type n_top_nearest_neighbors: int
        :param n_top_nearest_neighbors: Number of top nearest neighbors to use.

        :type voting: bool
        :param voting: Should simple voting be used or a weighted sum?

        :param max_number_of_labels: The maximum number of labels to be returned; if None all found labels are returned.

        :type drop_zero_scored_labels: bool
        :param drop_zero_scored_labels: Should the labels with zero scores be dropped or not?

        :type normalize: bool
        :param normalize: Should the scores be normalized?

        :type ignore_unknown: bool
        :param ignore_unknown: Should the unknown tags be ignored or not?

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        # Verify tag_type
        if tag_type not in self.take_matrices():
            raise ValueError("The value of the first argument, 'tag_type' is not a known tag type.")

        # Compute the recommendations
        recs = self.recommend_by_profile(profile=profile,
                                         nrecs=n_top_nearest_neighbors,
                                         vector_result=True,
                                         ignore_unknown=ignore_unknown).take_value()

        # "Nothing" result
        if recs.column_sums()[0] == 0:
            self.set_value({None: 1})
            return self

        # Get the tag type matrix
        matTagType = self.take_matrices()[tag_type]

        # Transpose in place
        recs.transpose(copy=False)

        # Respect voting
        if voting:
            recs.unitize()

        # Get scores
        clRes = recs.dot(matTagType)

        # Convert to dictionary
        clRes = clRes.column_sums_dict()

        # Drop zero scored labels
        if drop_zero_scored_labels:
            clRes = {k: v for (k, v) in clRes.items() if v > 0}

        # Normalize
        if normalize:
            cl_max = max(list(clRes.values()))
            if cl_max > 0:
                clRes = {k: v / cl_max for (k, v) in clRes.items()}

        # Reverse sort
        clRes = _reverse_sort_dict(clRes)

        # Pick max-top labels
        if max_number_of_labels and max_number_of_labels > len(clRes):
            clRes = dict(list(recs.items())[0:max_number_of_labels])

        # Result
        self.set_value(clRes)

        return self

    # ------------------------------------------------------------------
    # To metadata recommender
    # ------------------------------------------------------------------
    def to_metadata_recommender(self, tag_type_to, tag_types=None, tag_type_matrix=None, normalizer_func=None):
        """Convert to a metadata recommender

         Converts the recommender object into a recommender for a
         specified tag type using replacements in the long form representation of the recommender matrix.

         The following steps are taken:

           - If `tag_type_matrix` is None then tag_type_matrix = self.sub_matrix(tag_type_to)

           - Normalize the columns of `tag_type_matrix` using `normalizer_func`

           - Each recommender sub-matrix `m` is multiplied by `tag_type_matrix`, i.e. `tag_type_matrix.transpose().dot(m)`

           - A new recommender is created with items that are the tags of `tag_type_to`

         :type tag_type_to: Str
         :param tag_type_to: Tag type to make a recommender for.

         :type tag_types: List
         :param tag_types: A vector tag types (strings) to make the data frame with. If None then all tag types are used.

         :type tag_type_matrix: SSparseMatrix|None
         :param tag_type_matrix: A sparse matrix of item IDs vs tags of tag_type_to.
         If None then self.sub_matrix(tag_type_to) is used.

         :type normalizer_func:
         :param normalizer_func: An LSI normalizer function. One of None, "None", "Cosine", "Sum", or "Max".
         If None then it is same as "None". See self.apply_term_weight_functions.

         :rtype: SparseMatrixRecommender
         :return A sparse matrix recommender
         """

        # Process tag_type_to
        if not isinstance(tag_type_to, str):
            raise ValueError("The argument tag_type_to is expected to be a string.")

        # Verify tag_type_to
        if tag_type_to not in self.take_matrices():
            raise ValueError("The value of the first argument, 'tag_type_to' is not a known tag type.")

        my_tag_type_to = tag_type_to

        # Process tag_types
        allTagTypes = set(self.take_matrices().keys())
        my_tag_types = tag_types
        if tag_types is None:
            my_tag_types = allTagTypes.difference({my_tag_type_to})

        if my_tag_type_to in set(my_tag_types):
            warnings.warn("Removing the value of tag_type_to from value of tag_types.")
            my_tag_types = my_tag_types.difference({my_tag_type_to})

        if len(allTagTypes.intersection(my_tag_types)) == 0:
            raise ValueError("The argument tag_types has no known tag type of the recommender object.")

        # Process tag_type_matrix
        my_tag_type_matrix = tag_type_matrix
        if not (tag_type_matrix is None or isinstance(tag_type_matrix, SSparseMatrix)):
            raise ValueError("The argument tag_type_matrix is expected to be None or a sparse matrix.")

        if tag_type_matrix is None:
            my_tag_type_matrix = self.sub_matrix(tag_type_to)

        if not my_tag_type_matrix.row_names() == self.take_M().row_names():
            raise ValueError(
                "The argument tag_type_matrix has row names that are different than the row names of recommender matrix.")

        # Process normalizer_func
        my_normalizer_func = normalizer_func
        if not (normalizer_func is None or isinstance(normalizer_func, str)):
            raise ValueError("The argument normalizerFunc is expected to be None or a string.")

        # Obtain tag_type_matrix
        my_tag_type_matrix = my_tag_type_matrix.transpose()

        # Normalize the columns of tagTypeMatrix
        if not (normalizer_func is None or normalizer_func == "None"):
            my_tag_type_matrix = apply_term_weight_functions(doc_term_matrix=my_tag_type_matrix,
                                                             global_weight_func="None",
                                                             local_weight_func="None",
                                                             normalizer_func=my_normalizer_func)

        # Get the recommender contingency matrices
        smats = {k: m for (k, m) in self.take_matrices().items() if k in my_tag_types}

        # Multiply sub-matrices
        smats = {k: my_tag_type_matrix.dot(m) for (k, m) in smats.items()}

        # Create recommender
        return SparseMatrixRecommender().create_from_matrices(matrices=smats)

    # ------------------------------------------------------------------
    # SMR join
    # ------------------------------------------------------------------
    def join(self, smr2, join_type="left", **kwargs):

        allRowNames = self.take_M().row_names()
        if join_type != "same":

            if join_type in set(["outer", "union"]):

                allRowNames = list(set.union(set(self.take_M().row_names()),
                                             set(smr2.take_M().row_names())))

            elif join_type == "inner":

                allRowNames = list(set.intersection(set(self.take_M().row_names()),
                                                    set(smr2.take_M().row_names())))

            elif join_type == "left":

                allRowNames = self.take_M().row_names()

            else:
                raise ValueError(
                    "The second argument is expected to be one of \"same\", \"outer\", \"inner\", \"left\".")

        aSMats1 = self.take_matrices()
        aSMats2 = smr2.take_matrices()

        commonTags = set.intersection(set(aSMats1.keys()), set(aSMats2.keys()))
        if len(commonTags) > 0:
            warnings.warn(
                "The tag types " + str(commonTags) + " are also in the SMR argument, hence will be dropped.")

        if join_type != "same":
            aSMats1 = {k: v.impose_row_names(allRowNames) for (k, v) in aSMats1.items()}
            aSMats2 = {k: v.impose_row_names(allRowNames) for (k, v) in aSMats2.items()}

        # Not using this nice way, since it is "only" for >=3.9
        # matrices = aSMats1 | aSMats2
        matrices = {**aSMats1, **aSMats2}

        return SparseMatrixRecommender(matrices)

    # ------------------------------------------------------------------
    # Annex matrices
    # ------------------------------------------------------------------
    def annex_sub_matrices(self, mats):
        """Enhance recommender matrix with nearest neighbors sub-matrix.

        :tupe mats: dict
        :param mats: A dictionary of matrices to be annexed.

        :rtype: SparseMatrixRecommender
        :return A sparse matrix recommender
        """

        if not is_smat_dict(mats):
            raise ValueError("The second argument, mats, is expected to be a dictionary of SSparseMatrix.")

        smr2 = SparseMatrixRecommender(mats)
        return self.join(smr2=smr2)

    # ------------------------------------------------------------------
    # Annex matrix
    # ------------------------------------------------------------------
    # I consider the definition of this function to be redundant.
    # def annex_sub_matrix(self, new_tag_type, new_mat):
    #    return self.annex_sub_matrices({new_tag_type: new_mat})

    # ------------------------------------------------------------------
    # To metadata recommender
    # ------------------------------------------------------------------
    def enhance_with_nearest_neighbors(self,
                                       tag_types=None,
                                       number_of_nearest_neighbors=20,
                                       nearest_neighbors_tag_type="neighbor",
                                       batch_size=None):
        """Enhance recommender matrix with nearest neighbors sub-matrix.

        :tupe tag_types: str|list|None
        :param tag_types: Tag types to use make compute the similarities.

        :type number_of_nearest_neighbors: Int
        :param number_of_nearest_neighbors: Number of nearest neighbors per item.

        :type nearest_neighbors_tag_type: str
        :param nearest_neighbors_tag_type: Tag type of the nearest neighbor sub-matrix.

        :type batch_size: int|None
        :param batch_size: Number of nearest neighbors per item.

        :rtype: SparseMatrixRecommender
        :return A sparse matrix recommender
        """

        tagTypes = tag_types
        # Filter tag types
        if isinstance(tag_types, str):
            tagTypes = [tagTypes, ]

        if tag_types is None:
            tagTypes = list(self.take_matrices().keys())

        if not is_str_list(tagTypes):
            raise ValueError("The argument tag_types is expected to be a string, a list of string, or None.")

        removeTagTypes = set.difference(set(self.take_matrices().keys()), set(tagTypes))

        if len(removeTagTypes) > 0:
            smrRes = self.remove_tag_types(tag_types=removeTagTypes)
        else:
            smrRes = self

        # Similarities computations
        # This implementation is far from optimal.
        dfNNs = None
        for itemID in smrRes.take_M().row_names():

            aRecs = smrRes.recommend(history=itemID,
                                     nrecs=number_of_nearest_neighbors,
                                     remove_history=False,
                                     normalize=True).take_value()

            dfRecs = pandas.DataFrame(
                {"SearchID": itemID, "NearestNeighborID": list(aRecs.keys()), "Score": list(aRecs.values())})

            if dfNNs is None:
                dfNNs = dfRecs
            else:
                dfNNs = pandas.concat([dfNNs, dfRecs], ignore_index=True)

        # Annex sub-matrix
        smatNNs = cross_tabulate(dfNNs, "SearchID", "NearestNeighborID", "Score")

        smrRes = self.annex_sub_matrices(mats={nearest_neighbors_tag_type: smatNNs})

        # Result
        return smrRes

    # ------------------------------------------------------------------
    # To dictionary form
    # ------------------------------------------------------------------
    def to_dict(self):
        """Convert to dictionary form.

        Returns dictionary representation of the SparseMatrixRecommender object with keys:
        ['matrices', 'tagTypeWeights', 'data', 'value'].

        The value of the keys 'matrices' is a dictionary of dictionaries.

        (Ideally) this function facilitates rapid conversion and serialization.
        """
        res = {"matrices": {k: v.to_dict() for (k, v) in self.take_matrices().items()},
               "tagTypeWeights": self.take_tag_type_weights(),
               "data": self.take_data(),
               "value": self.take_value()}
        return res

    # ------------------------------------------------------------------
    # From dictionary form
    # ------------------------------------------------------------------
    def from_dict(self, arg):
        """Convert from dictionary form.

        Creates a SparseMatrixRecommender object from a dictionary representation with keys:
        ['matrices', 'tagTypeWeights', 'data', 'value'].

        The value of the keys 'matrices' is expected to be a dictionary of dictionaries.

        (Ideally) this function facilitates rapid conversion and serialization.
        """
        if not (isinstance(arg, dict) and
                all([x in {'matrices', 'tagTypeWeights', 'data', 'value'} for x in list(arg.keys())])):
            raise TypeError("""The first argument is expected to be a dictionary with keys:
            'matrices', 'tagTypeWeights', 'data', 'value'.""")

        if not (isinstance(arg["matrices"], dict) and
                all([isinstance(x, dict) for x in list(arg["matrices"].values())])):
            raise TypeError("""The value of 'matrices' is expected to be a dictionary of dictionaries.""")

        self.create_from_matrices({k: SSparseMatrix().from_dict(v) for (k, v) in arg["matrices"].items()})
        self.set_tag_type_weights(arg["tagTypeWeights"])
        self.set_data(arg["data"])
        self.set_value(arg["value"])
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
        """Representation of SparseMatrixRecommender object."""
        return "<Sparse matrix recommender object with matrix dimensions %dx%d\n" \
               "\tand with %d tag types>" % \
               (self._M.sparse_matrix().shape + (len(self._matrices),))
