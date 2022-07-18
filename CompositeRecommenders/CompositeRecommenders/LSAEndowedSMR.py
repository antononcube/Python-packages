from SparseMatrixRecommender.SparseMatrixRecommender import SparseMatrixRecommender
from LatentSemanticAnalyzer.LatentSemanticAnalyzer import LatentSemanticAnalyzer
import warnings


# ======================================================================
# Utilities
# ======================================================================

# Normalize
def _normalize(x, norm_spec="max-norm"):
    if not isinstance(x, dict):
        raise TypeError("The first argument is expected to be a dictionary.")

    if norm_spec == "max_norm":
        x_max = max(list(x.values()))
        xRes = x
        if x_max > 0:
            xRes = {k: v / x_max for (k, v) in xRes.items()}

    elif norm_spec == "euclidean":
        x_norm = pow(sum([y * y for y in list(x.values())]), 0.5)

        xRes = x
        if x_norm > 0:
            xRes = {k: v / x_norm for (k, v) in xRes.items()}

    else:
        raise ValueError("Unknown norm spec.")

    return xRes


# ======================================================================
# Class definition
# ======================================================================
class LSAEndowedSMR:
    _smrObj: SparseMatrixRecommender = None
    _lsaObj: LatentSemanticAnalyzer = None
    _profileNormalizer: str = "max-norm"
    _value = None

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Creation of a LSAEndowedSMR object.
           Two arguments are expected of arguments are given: SMR object and LSA object.
        """
        self.set_profileNormalizer("max_norm")
        if len(args) == 2 and \
                isinstance(args[0], SparseMatrixRecommender) and \
                isinstance(args[1], LatentSemanticAnalyzer):
            self.set_SMR(args[0])
            self.set_LSA(args[1])

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------
    def take_SMR(self):
        """Take the SparseMatrixRecommender object."""
        return self._smrObj

    def take_LSA(self):
        """Take the LatentSemanticAnalyzer object."""
        return self._lsaObj

    def take_value(self):
        """Take the pipeline value."""
        return self._value

    def take_profileNormilizer(self):
        """Take the pipeline value."""
        return self._profileNormalizer

    # ------------------------------------------------------------------
    # Echoers
    # ------------------------------------------------------------------
    def echo_SMR(self):
        """Echo the SparseMatrixRecommender object."""
        print(self._smrObj)
        return self

    def echo_LSA(self):
        """Echo the LatentSemanticAnalyzer object."""
        print(self._LSA)
        return self

    def echo_value(self):
        """Echo the pipeline value."""
        print(self._value)
        return self

    def echo_profileNormilizer(self):
        """Echo the profile normalzier."""
        print(self._profileNormalizer)
        return self

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------
    def set_SMR(self, arg):
        """Set SparseMatrixRecommender object."""
        if isinstance(arg, SparseMatrixRecommender):
            self._smrObj = arg
        else:
            raise TypeError("The first argument is expected to be a SparseMatrixRecommender object.")

        return self

    def set_LSA(self, arg):
        """Set LatentSemanticAnalyzer object."""
        if isinstance(arg, LatentSemanticAnalyzer):
            self._lsaObj = arg
        else:
            raise TypeError("The first argument is expected to be a LatentSemanticAnalyzer object.")

        return self

    def set_value(self, arg):
        """Set pipeline value."""
        self._value = arg
        return self

    def set_profileNormalizer(self, arg):
        """Set profile normalizer."""
        self._profileNormalizer = arg
        return self

    # ------------------------------------------------------------------
    # Recommend by profile
    # ------------------------------------------------------------------
    def recommend_by_profile(self, profile,
                             nrecs: int = 10,
                             normalize: bool = True,
                             ignore_unknown: bool = False,
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

        if not isinstance(self._smrObj, SparseMatrixRecommender):
            raise ValueError("No core SMR object.")

        self._smrObj.recommend_by_profile(profile=profile,
                                          nrecs=nrecs,
                                          normalize=normalize,
                                          ignore_unknown=ignore_unknown,
                                          vector_result=vector_result)

        return self

    # ------------------------------------------------------------------
    # Recommend by profile and text
    # ------------------------------------------------------------------
    def recommend_by_profile_and_text(self,
                                      profile,
                                      text,
                                      nrecs=10,
                                      normalize=True,
                                      ignore_unknown=False,
                                      vector_result: bool = False):
        """Recommend by profile.

        :type profile: str|list|dict
        :param profile: A tag, a list of tags, a dictionary of scored tags.

        :type text: str
        :param text: Text query

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

        if not isinstance(self._smrObj, SparseMatrixRecommender):
            raise ValueError("No core SMR object.")

        if not isinstance(self._lsaObj, LatentSemanticAnalyzer):
            raise ValueError("No core LSA object.")

        if not (isinstance(profile, (list, dict)) and len(profile) > 0 or len(text) > 0):
            raise ValueError("Empty profile and text.")

        if isinstance(profile, (list, dict)) and len(profile) == 0:
            profileLocal = {}
        else:
            profileLocal = self.take_SMR().to_profile_vector(profile, ignore_unknown=True)

        # Make a profile corresponding to the text.
        textProf = {}
        if len(text) > 0:
            # Represent by terms
            textWordsProf = self._lsaObj.represent_by_terms(text).take_value().column_sums_dict()

            # Represent by topics
            textTopicsProf = self._lsaObj.represent_by_topics(text).take_value().column_sums_dict()

            # Appropriate verifications have to be made for concatenating with 'Word:' and 'Topic:'.
            textWordsProf = {"Word:" + k: v for (k, v) in textWordsProf.items()}
            textTopicsProf = {"Topics:" + k: v for (k, v) in textTopicsProf.items()}

            # Normalize each profile
            textWordsProf = _normalize(textWordsProf, self._profileNormalizer)
            textTopicsProf = _normalize(textTopicsProf, self._profileNormalizer)

            # Make the words-and-topics profile.
            textProf = textTopicsProf | textWordsProf

        # Make the combined profile.
        profCombined = profileLocal | textProf
        profCombined = _normalize(profCombined, self._profileNormalizer)

        # Get recommendations
        self._smrObj.recommend_by_profile(profile=profCombined,
                                          nrecs=nrecs,
                                          normalize=normalize,
                                          ignore_unknown=ignore_unknown,
                                          vector_result=vector_result)

        self.set_value(self._smrObj.take_value())

        return self

    # ------------------------------------------------------------------
    # To dictionary form
    # ------------------------------------------------------------------
    def to_dict(self):
        """Convert to dictionary form.

        Returns dictionary representation of the LSAEndowedSMR object with keys:
        ['SMR', 'LSA', 'profileNormalizer']

        (Ideally) this function facilitates rapid conversion and serialization.
        """

        res = {"SMR": self.take_SMR().to_dict(),
               "LSA": self.take_LSA().to_dict(),
               "profileNormalizer": self.take_profileNormilizer()}
        return res

    # ------------------------------------------------------------------
    # From dictionary form
    # ------------------------------------------------------------------

    def from_dict(self, arg):
        """Convert from dictionary form.

        Creates a LatentSemanticAnalyzer object from a dictionary representation with keys:
        ['matrices', 'W', 'H', 'stemmingRules', 'stopWords', ...].

        The value of the keys 'matrices' is expected to be a dictionary of dictionaries.

        (Ideally) this function facilitates rapid conversion and serialization.
        """
        if not (isinstance(arg, dict) and
                all([x in arg for x in ["SMR", "LSA", "profileNormalizer"]])):
            raise TypeError("""The first argument is expected to be a dictionary with keys:
            'SMR', 'LSA', 'profileNormalizer'.""")

        self.set_SMR(arg["SMR"])
        self.set_LSA(arg["LSA"])
        self.set_profileNormalizer(arg["profileNormalizer"])
        return self

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------
    def __str__(self):
        """String for LSAEndowedSMR object."""
        res = ""
        if isinstance(self.take_SMR(), SparseMatrixRecommender):
            res = "SMR:\n\t" + str(self.take_SMR())
        else:
            res = "SMR: None"

        if isinstance(self.take_LSA(), LatentSemanticAnalyzer):
            res = res + "\nLSA:\n\t" + str(self.take_LSA())
        else:
            res = res + "\nLSA: None"

        return res

    def __repr__(self):
        """Representation of LSAEndowedSMR object."""
        res = ""
        if isinstance(self.take_SMR(), SparseMatrixRecommender):
            res = "SMR:\n\t" + repr(self.take_SMR())
        else:
            res = "SMR: None"

        if isinstance(self.take_LSA(), LatentSemanticAnalyzer):
            res = res + "\nLSA:\n\t" + repr(self.take_LSA())
        else:
            res = res + "\nLSA: None"

        return res
