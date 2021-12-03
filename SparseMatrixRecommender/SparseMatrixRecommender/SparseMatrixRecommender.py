from SSparseMatrix import SSparseMatrix
from SSparseMatrix import column_bind
from SSparseMatrix import is_s_sparse_matrix
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
    def _to_smr_vector(self, arg, things_dict, thing_name, ref_name):
        """To SMR vector

        :type arg: str|dict
        :param arg: A list of items or tags, or a dictionary of scored items or tags.

        :param things_dict: Set items or tags.
        :param thing_name: Which matrix axis, one of "column" or "row"

        :param ref_name: Reference name, one of "item" or "tag"

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")

        if is_str_list(arg):
            dvec = dict.fromkeys(arg, 1)
            return self._to_smr_vector(dvec, things_dict, thing_name, ref_name)
        elif is_scored_tags_dict(arg):
            known_keys = {key: value for (key, value) in arg.items() if key in things_dict}
            if len(known_keys) == 0:
                raise LookupError("None of the tags is a valid recommendation matrix " + thing_name + " name.")
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

    # ------------------------------------------------------------------
    # To profile vector
    # ------------------------------------------------------------------
    def to_profile_vector(self, arg):
        """Convert a list or a dictionary into a profile SSparseMatrix (with one column.)

        :type arg: str|list|dict
        :param arg: A tag, a list of tags, or dictionary of scored tags.

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")

        return self._to_smr_vector(arg, things_dict=self._M.column_names_dict(), thing_name="column", ref_name="tags")

    # ------------------------------------------------------------------
    # To history vector
    # ------------------------------------------------------------------
    def to_history_vector(self, arg):
        """Convert a list or a dictionary into a profile SSparseMatrix (with one column.)

        :type arg: str|list|dict
        :param arg: A item, a list of item, or dictionary of scored items.

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        if not isinstance(self._M, SSparseMatrix):
            raise TypeError("Cannot find recommendation matrix.")

        return self._to_smr_vector(arg, things_dict=self._M.row_names_dict(), thing_name="row", ref_name="items")

    # ------------------------------------------------------------------
    # Recommend by profile
    # ------------------------------------------------------------------
    def recommend_by_profile(self, profile, nrecs=10, vector_result: bool = False):
        """Recommend by profile.

        :type profile: str|list|dict
        :param profile: A tag, a list of tags, a dictionary of scored tags.

        :type nrecs: int|None
        :param nrecs: A positive integer or None. If it is None, then all items with non-zero scores are returned.

        :type vector_result: bool
        :param vector_result: Should the result be a (SSparseMatrix) vector or a dictionary.

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        # Make scored tags vector
        if isinstance(profile, str):
            vec = self.to_profile_vector([profile]).take_value()
        elif isinstance(profile, dict) or isinstance(profile, list):
            vec = self.to_profile_vector(profile).take_value()
        elif is_s_sparse_matrix(profile):
            vec = profile
        else:
            raise TypeError("The first argument is expected to be a list of tags or a dictionary of scored tags.")

        # Compute the recommendations
        recs = self.take_M().dot(vec)

        if not vector_result:
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
    def recommend(self, history, nrecs=10, remove_history=True):
        """Recommend by history.

        :type history: str|list|dict
        :param history: An item (string), a list of items, a dictionary of scored items.

        :type nrecs: int|None
        :param nrecs: A positive integer or None. If it is None, then all items with non-zero scores are returned.

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
        # Hence using merge.
        self.set_value(dfRecs.merge(data, on=mon, how="left"))

        return self

    # ------------------------------------------------------------------
    # Classify by profile
    # ------------------------------------------------------------------
    def classify_by_profile(self, tag_type, profile,
                            n_top_nearest_neighbors=100,
                            voting=False,
                            drop_zero_scored_labels=True,
                            max_number_of_labels=None,
                            normalize: bool = True):
        """Clasify by profile vector.

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

        :rtype SparseMatrixRecommender
        :return self: The object itself or None. The result is stored in self._value.
        """
        # Verify tag_type
        if tag_type not in self.take_matrices():
            raise ValueError("The value of the first argument, 'tag_type' is not a known tag type.")

        # Compute the recommendations
        recs = self.recommend_by_profile(profile=profile,
                                         nrecs=n_top_nearest_neighbors,
                                         vector_result=True).take_value()
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
