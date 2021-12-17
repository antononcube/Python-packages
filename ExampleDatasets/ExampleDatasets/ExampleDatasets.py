import random
from pathlib import Path
from typing import Optional

import pandas
import pkg_resources
import xdg


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


def example_dataset(itemSpec: Optional[str] = None,
                    packageSpec: Optional[str] = None,
                    keep: bool = False):
    """Get a data frame of an example dataset.

    :type itemSpec: str|None
    :param itemSpec: Item in a package; can be a regex.

    :type packageSpec: str|None
    :param packageSpec: Package name; can be a regex.

    :type keep: bool
    :param keep: Should the dataset be kept locally or not?

    :return res: Dataset data frame if exactly on dataset matched the specs; otherwise None.

    """

    if itemSpec is None and packageSpec is None:
        obj = dfRdatasets.iloc[[random.randint(0, dfRdatasets.shape[0])], :]
    elif packageSpec is None:
        obj = dfRdatasets[(dfRdatasets["Item"] == itemSpec)]
    else:
        obj = dfRdatasets[((dfRdatasets["Item"] == itemSpec) & (dfRdatasets["Package"] == packageSpec))]

    if obj.shape[0] == 0:

        print("No datasets found with the given source spec.")
        return None

    elif obj.shape[0] > 1:

        print("Found more than one dataset with the given spec:")
        print(obj)
        return None

    persDirPath = Path(xdg.xdg_data_home()) / 'Python' / 'ExampleDatasets'
    idName = obj["Package"].values[0] + "::" + obj["Item"].values[0] + ".csv"

    persFilePath = persDirPath / idName

    if persFilePath.exists():
        res = pandas.read_csv(persFilePath)
    else:
        url = obj["CSV"].values[0]
        res = pandas.read_csv(url)

    if keep and not persFilePath.exists():
        # 1. Make directory if it does not exist
        if not persDirPath.exists():
            persDirPath.mkdir(parents=True, exist_ok=True)

        # 2. Put the dataset file there
        keepPath = persDirPath / idName
        res.to_csv(keepPath)

    return res
