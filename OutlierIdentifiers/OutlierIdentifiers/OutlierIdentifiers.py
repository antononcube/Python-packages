import numpy as np


def top_outliers(pair):
    """
    Top outliers only thresholds
    Drops the bottom threshold of a pair of thresholds.

    :param pair: A pair of bottom and top thresholds.
    :return: A list with -Inf and the top threshold.
    """
    if not (isinstance(pair, (list, tuple)) and len(pair) == 2 and all(isinstance(x, (int, float)) for x in pair)):
        raise ValueError("A pair of numbers is expected as a first argument.")
    return (-float('inf'), pair[1])


def bottom_outliers(pair):
    """
    Bottom outliers only thresholds
    Drops the top threshold of a pair of thresholds.

    :param pair: A pair of bottom and top thresholds.
    :return: A list with the bottom threshold and Inf.
    """
    if not (isinstance(pair, (list, tuple)) and len(pair) == 2 and all(isinstance(x, (int, float)) for x in pair)):
        raise ValueError("A pair of numbers is expected as a first argument.")
    return (pair[0], float('inf'))


def hampel_identifier_parameters(data):
    """
    Hampel identifier parameters
    Find Hampel outlier thresholds for a data vector.

    :param data: A data vector.
    :return: A list with lower and upper Hampel thresholds.
    """
    x0 = np.median(data)
    md = 1.4826 * np.median(np.abs(data - x0))
    return (x0 - md, x0 + md)


def quartile_identifier_parameters(data):
    """
    Quartile identifier parameters
    Find Quartile outlier thresholds for a data vector.

    :param data: A data vector.
    :return: A list with lower and upper Quartile thresholds.
    """
    res = np.percentile(data, [25, 50, 75])
    xL, x0, xU = res
    return (x0 - (xU - xL), x0 + (xU - xL))


def splus_quartile_identifier_parameters(data):
    """
    SPLUS quartile identifier parameters
    Find SPLUS Quartile outlier thresholds for a data vector.

    :param data: A data vector.
    :return: A list with lower and upper SPLUS Quartile thresholds.
    """
    if len(data) <= 4:
        xL = np.min(data)
        xU = np.max(data)
    else:
        res = np.percentile(data, [25, 75])
        xL, xU = res
    return (xL - 1.5 * (xU - xL), xU + 1.5 * (xU - xL))


def outlier_identifier(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None, value=False):
    """
    Outlier identifier
    Find outliers for a data vector.

    :param data: A data vector.
    :param identifier: An outlier identifier function.
    :param lower_and_upper_thresholds: Outlier identifier parameters.
    :param value: Should values be returned or not?
    :return: A numeric vector of outliers or a logical vector.
    """
    if not isinstance(data, (list, tuple, np.ndarray)):
        raise ValueError("The argument data is expected to be a numeric vector.")
    data = np.array(data)
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    pred = (data <= lower_and_upper_thresholds[0]) | (data >= lower_and_upper_thresholds[1])
    return data[pred] if value else pred


def top_outlier_identifier(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None, value=False):
    """
    Top outlier identifier
    Find the top outliers for a data vector.

    :param data: A data vector.
    :param identifier: An outlier identifier function.
    :param lower_and_upper_thresholds: Outlier identifier parameters.
    :param value: Should values be returned or not?
    :return: A numeric vector of outliers or a logical vector.
    """
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    pred = data > lower_and_upper_thresholds[1]
    return data[pred] if value else pred


def bottom_outlier_identifier(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None, value=False):
    """
    Bottom outlier identifier
    Find the bottom outliers for a data vector.

    :param data: A data vector.
    :param identifier: An outlier identifier function.
    :param lower_and_upper_thresholds: Outlier identifier parameters.
    :param value_q: Should values be returned or not?
    :return: A numeric vector of outliers or a logical vector.
    """
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    pred = data < lower_and_upper_thresholds[0]
    return data[pred] if value else pred


def outlier_position(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None):
    """
    Outlier positions finder
    Find the outlier positions in a data vector.

    :param data: A data vector.
    :param identifier: An outlier identifier function.
    :param lower_and_upper_thresholds: Outlier identifier parameters.
    :return: Indices of outliers in the data vector.
    """
    if not isinstance(data, (list, tuple, np.ndarray)):
        raise ValueError("The argument data is expected to be a numeric vector.")
    data = np.array(data)
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    return np.where((data < lower_and_upper_thresholds[0]) | (data > lower_and_upper_thresholds[1]))[0]


def top_outlier_position(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None):
    """
    Top outlier positions finder
    Find the top outlier positions in a data vector.

    :param data: A data vector.
    :param identifier: An outlier identifier function.
    :param lower_and_upper_thresholds: Outlier identifier parameters.
    :return: Indices of top outliers in the data vector.
    """
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    return np.where(data > lower_and_upper_thresholds[1])[0]


def bottom_outlier_position(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None):
    """
    Bottom outlier positions finder
    Find the bottom outlier positions in a data vector.

    :param data: A data vector.
    :param identifier: An outlier identifier function.
    :param lower_and_upper_thresholds: Outlier identifier parameters.
    :return: Indices of bottom outliers in the data vector.
    """
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    return np.where(data < lower_and_upper_thresholds[0])[0]
