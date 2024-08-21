import numpy as np


def top_outliers_only_thresholds(pair):
    if not (isinstance(pair, (list, tuple)) and len(pair) == 2 and all(isinstance(x, (int, float)) for x in pair)):
        raise ValueError("A pair of numbers is expected as a first argument.")
    return (-float('inf'), pair[1])


def bottom_outliers_only_thresholds(pair):
    if not (isinstance(pair, (list, tuple)) and len(pair) == 2 and all(isinstance(x, (int, float)) for x in pair)):
        raise ValueError("A pair of numbers is expected as a first argument.")
    return (pair[0], float('inf'))


def hampel_identifier_parameters(data):
    x0 = np.median(data)
    md = 1.4826 * np.median(np.abs(data - x0))
    return (x0 - md, x0 + md)


def quartile_identifier_parameters(data):
    res = np.percentile(data, [25, 50, 75])
    xL, x0, xU = res
    return (x0 - (xU - xL), x0 + (xU - xL))


def splus_quartile_identifier_parameters(data):
    if len(data) <= 4:
        xL = np.min(data)
        xU = np.max(data)
    else:
        res = np.percentile(data, [25, 75])
        xL, xU = res
    return (xL - 1.5 * (xU - xL), xU + 1.5 * (xU - xL))


def outlier_identifier(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None, value=False):
    if not isinstance(data, (list, np.ndarray)):
        raise ValueError("The argument data is expected to be a numeric vector.")
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    pred = (data <= lower_and_upper_thresholds[0]) | (data >= lower_and_upper_thresholds[1])
    return data[pred] if value else pred


def top_outlier_identifier(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None, value=False):
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    pred = data > lower_and_upper_thresholds[1]
    return data[pred] if value else pred


def bottom_outlier_identifier(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None, value=False):
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    pred = data < lower_and_upper_thresholds[0]
    return data[pred] if value else pred


def outlier_position(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None):
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    return np.where((data < lower_and_upper_thresholds[0]) | (data > lower_and_upper_thresholds[1]))[0]


def top_outlier_position(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None):
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    return np.where(data > lower_and_upper_thresholds[1])[0]


def bottom_outlier_position(data, identifier=splus_quartile_identifier_parameters, lower_and_upper_thresholds=None):
    if lower_and_upper_thresholds is None:
        lower_and_upper_thresholds = identifier(data)
    return np.where(data < lower_and_upper_thresholds[0])[0]
