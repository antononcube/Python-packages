import random
import pandas
import numpy
from strgen import StringGenerator
import pkg_resources


# ===========================================================
# Load words
# ===========================================================
def load_words():
    """Return a dataframe with words.

    Contains the following fields:
        Word          word
        KnownWordQ    is a known word True/False
        KnownWordQ    is a known word True/False
        KnownWordQ    is a known word True/False
    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    stream = pkg_resources.resource_stream(__name__, 'resources/dfEnglishWords.csv')
    return pandas.read_csv(stream, encoding='latin-1')


# ===========================================================
# Load pet names
# ===========================================================
def load_pet_names():
    """Return a dataframe with pet names.

    Contains the following fields:
        Species       species
        Name          pet name
        Count         how many licenses with that specie-name pair
    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    stream = pkg_resources.resource_stream(__name__, 'resources/dfPetNameCounts.csv')
    dfData = pandas.read_csv(stream, encoding='latin-1')
    wsum = sum(dfData.Count)
    dfData["Weight"] = [x / wsum for x in dfData.Count]
    return dfData


# ===========================================================
# Random words
# ===========================================================

def random_string(size=1, chars=5):
    """Generates random strings with specified size and number of characters."""

    if isinstance(chars, type(None)):
        nchars = numpy.random.poisson(lam=5, size=1)
        nchars = 1 if nchars == 0 else nchars
    elif isinstance(chars, int) and chars > 1:
        nchars = chars
    else:
        raise TypeError("The second argument is expected to be positive integer of None.")
        return None

    if isinstance(size, int) and size == 1:
        return StringGenerator("[\l\d]{" + str(nchars) + "}").render()
    elif isinstance(size, int) and size > 1:
        return StringGenerator("[\l\d]{" + str(nchars) + "}").render_list(size, unique=True)
    elif isinstance(size, type(None)):
        return random_string(1)
    else:
        raise TypeError("The first argument is expected to be positive integer of None.")
        return None


# ===========================================================
# Random words
# ===========================================================

# Read resources
dfWords = load_words()


def random_word(size=1, kind=None, language="English"):
    """Generates random words with specified size and kind"""

    if not isinstance(size, int) and size > 0:
        raise TypeError("The first argument is expected to be positive integer.")
        return None

    if not isinstance(language, str) and language.lower() == 'english':
        raise """The argument language is expected to be one of 'English' or Whatever. 
        (Only English words are supported at this time.)"""
        return None

    if isinstance(kind, type(None)):
        mkind = "any"
    elif isinstance(kind, str):
        mkind = kind
    else:
        raise TypeError("The argument 'kind' is expected to be string or None.")
        return None

    if mkind.lower() == "any":
        res = random.sample(list(dfWords["Word"]), k=size)
    elif mkind.lower() in "known":
        res = random.sample(list(dfWords[dfWords.KnownWordQ]["Word"]), k=size)
    elif mkind.lower() == "common":
        res = random.sample(list(dfWords[dfWords.CommonWordQ]["Word"]), k=size)
    elif mkind.lower() in {"stop", "stopword"}:
        res = random.sample(list(dfWords[dfWords.StopWordQ]["Word"]), k=size)
    else:
        raise TypeError("The argument 'kind' is expected to be one of 'any', 'known', 'common', 'stopword', or None.")
        return None

    if size == 1:
        return res[0]
    return res


# ===========================================================
# Random pet names
# ===========================================================

dfPetNames = load_pet_names()


def random_pet_name(size=1, species=None, weighted=True):
    if size == 0:
        raise TypeError("The first argument is expected to be a positive integer.")

    allSpecies = set(["Any", "Cat", "Dog", "Goat", "Pig"])

    if not (isinstance(species, type(None)) or isinstance(species, str) and species.capitalize() in allSpecies):
        raise ValueError("The argument 'species' is expected to be one of %, or None. Continuing with Any.")
        species = "Any"

    if weighted:
        weights = dfPetNames.Weight
    else:
        weights = None

    if isinstance(species, type(None)) or species.capitalize() == 'Any':
        res = numpy.random.choice(dfPetNames.Name, size=size, p=weights)
    else:
        res = numpy.random.choice(dfPetNames[dfPetNames.Species == species.capitalize()].Name,
                                  size=size,
                                  p=weights)

    if size == 1:
        return res[0]
    return res
