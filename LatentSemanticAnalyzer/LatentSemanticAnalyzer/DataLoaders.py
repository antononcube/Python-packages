import pandas

try:
    from importlib.resources import files
except ImportError:
    raise "Cannot use importlib_resources to import package files."


# ===========================================================
# Load abstracts data
# ===========================================================
def load_abstracts_data_frame():
    """Return a data frame with Titanic data.

    Abstract
    ----------------
    Abstracts of Wolfram Research Technology conferences.

    Each row represents one talk.

    :format: A data frame with 567 rows and 5 columns.
    :field ID: Presentation identifier.
    :field Name: Presenter(s) name.
    :field Title: Presentation title.
    :field Abstract: Abstract of the presentation.
    :field Track: Presentation track.
    """
    resource = files("LatentSemanticAnalyzer").joinpath("resources", "dfAbstracts.csv.gz")
    with resource.open("rb") as stream:
        dfData = pandas.read_csv(stream, compression="gzip", encoding='latin-1')
    return dfData
