from typing import Optional

import pandas
import pkg_resources


# ===========================================================
# Load datasets metadata
# ===========================================================
def load_datasets_metadata():
    """Return a data frame with datasets metadata.

    Datasets metadata
    ----------------

    :format: A data frame with 1745 rows and 12 columns.
    :field Package: Package
    :field Item: Item (in the package)
    :field Title: Title of dataset item
    :field CSV: URL to the corresponding CSV data.
    :field Doc: URL to the corresponding documentation.
    :field Rows: Number of rows.
    :field Cols: Number of columns.
    :field n_binary: Number of binary columns.
    :field n_character: Number of character columns.
    :field n_factor: Number of factor columns.
    :field n_logical: Number of logical columns.
    :field n_numeric: Number of numeric columns.

    :source url: https://github.com/vincentarelbundock/Rdatasets/
    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    with pkg_resources.resource_stream(__name__, 'resources/dfRdatasets.csv.gz') as stream:
        dfData = pandas.read_csv(stream, compression='gzip')
    return dfData


dfRdatasets = load_datasets_metadata()


def example_dataset(itemSpec: str, packageSpec: Optional[str] = None):
    # DSL TARGET Python-pandas; use dfRdatasets; filter by Item equals “titanic”; show counts.
    obj = dfRdatasets.copy()
    if packageSpec is None:
        obj = obj[(obj["Item"] == itemSpec)]
    else:
        obj = obj[((obj["Item"] == itemSpec) & (obj["Package"] == packageSpec))]

    if obj.shape[0] == 0:

        print("No datasets found with the given source spec.")
        return None

    elif obj.shape[0] > 1:

        print("Found more than one dataset with the given spec:")
        print(obj)
        return None

    url = obj["CSV"].values[0]
    dfData = pandas.read_csv(url)
    return dfData

