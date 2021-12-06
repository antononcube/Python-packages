import pandas
import pkg_resources


# ===========================================================
# Load USA arrests data
# ===========================================================
def load_usa_arrests_data_frame():
    """Return a data frame with USA arrests data.

    Description
    ----------------
    50 US states arrests data in 1973.

    Each row represents one state.

    :format: A data frame with 50 rows and 5 columns.
    :field StateName: US states names.
    :field Murder: Murder arrests per 100,000.
    :field Assault: Assault arrests per 100,000.
    :field UrbanPopulation: Urban population percentage.
    :field Rape: Rape arrests per 100,000.
    """
    # This is a stream-like object. If you want the actual info, call
    with pkg_resources.resource_stream(__name__, 'resources/dfUSAArrests.csv') as stream:
        dfData = pandas.read_csv(stream, encoding='latin-1')
    return dfData


# ===========================================================
# Load employee attitude data
# ===========================================================
def load_employee_attitude_data_frame():
    """Return a data frame with Chatterjee-Price attitude data.

    Description
    ----------------
    Chatterjee-Price attitude data.

    Each row represents one employee.

    :format: A data frame with 30 rows and 7 columns.
    :field Rating: Percentage of favorable responses to overall rating.
    :field Complaints: Percentage of favorable responses to employee complaints.
    :field Privileges: Percentage of favorable responses to not allow special privileges.
    :field Learning: Percentage of favorable responses to opportunity to learn.
    :field Raises: Percentage of favorable responses to raises based on performance.
    :field Critical: Percentage of favorable responses to too critical.
    :field Advancement: Percentage of favorable responses to advancement opportunities.
    """
    # This is a stream-like object. If you want the actual info, call
    with pkg_resources.resource_stream(__name__, 'resources/dfEmployeeAttitude.csv') as stream:
        dfData = pandas.read_csv(stream, encoding='latin-1')
    return dfData
