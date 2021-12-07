import pandas
import pkg_resources


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
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    with pkg_resources.resource_stream(__name__, 'resources/dfAbstracts.csv.gz') as stream:
        dfData = pandas.read_csv(stream, compression="gzip", encoding='latin-1')
    return dfData

