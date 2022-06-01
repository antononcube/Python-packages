import pandas
import pkg_resources


# ===========================================================
# Load Titanic survival
# ===========================================================
def load_titanic_data_frame():
    """Return a data frame with Titanic data.

    Titanic survival
    ----------------
    This data set contains the survival status of 1309 passengers aboard
    the maiden voyage of the RMS Titanic in 1912 (the ships crew are not included),
    along with the passengers age, sex and class (which serves as a proxy for economic status).

    Each row represents one person.
    The columns describe different attributes about the person.
    The first column "id" has simple ID's derived from ordering the data (in some way.)
    The names of the rest of the columns are self-explanatory.
    The column "passengerAge" has values "rounded" into age-groups, `range(0,80,10)`.
    If the passenger age is unknown/missing the value is -1.

    :format: A data frame with 1309 rows and 5 columns.
    :field id: Simple, order derived ID.
    :field passengerClass: Passenger class.
    :field passengerAge: Passenger age rounded into age groups.
    :field passengerSex: Passenger sex.
    :field passengerSurvival: Passenger survival.

    :source url: https://datarepository.wolframcloud.com/resources/Sample-Data-Titanic-Survival
    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    with pkg_resources.resource_stream(__name__, 'resources/dfTitanic.csv') as stream:
        dfData = pandas.read_csv(stream, encoding='latin-1')
        dfData["id"] = ["id." + str(x) for x in dfData["id"]]
    return dfData


# ===========================================================
# Load mushrooms data
# ===========================================================
def load_mushroom_data_frame():
    """Return a dataframe with mushroom edibility.

    Mushroom edibility
    ------------------
    This data set consists of 8124 records of the physical
    characteristics of gilled mushrooms in the Agaricus and Lepiota family,
    along with their edibility.
    Each row represents one mushroom.
    :format: A data frame with 8124 rows and 24 columns.
    :source url: https://datahub.io/machine-learning/mushroom
    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    with pkg_resources.resource_stream(__name__, 'resources/dfMushroom.csv.gz') as stream:
        dfData = pandas.read_csv(stream, compression='gzip')
        dfData["id"] = ["id." + str(x) for x in dfData["id"]]
    return dfData


# ===========================================================
# Load financial data
# ===========================================================
def load_mint_bubbles_transactions_data_frame():
    """Return a dataframe with mint bubbles transactions.

    Mint bubbles transactions
    -------------------------
    This data set consists of some person's banking financial transactions.
    :format: A data frame with 384 rows and 6 columns.
    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    with pkg_resources.resource_stream(__name__, 'resources/dfMintBubblesTransactions.csv') as stream:
        dfData = pandas.read_csv(stream, encoding='latin-1')
        dfData["id"] = ["id." + str(x) for x in range(0, dfData.shape[0])]
    return dfData
