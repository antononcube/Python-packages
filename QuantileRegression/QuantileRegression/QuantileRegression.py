import math
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import identity, hstack, vstack
from scipy.interpolate import BSpline

def _apply_f(row, f):
    return f(*row[:-1])


def _make_combined_function(funcs, sol, factor=1, shift=0, median=0):
    return lambda x: factor * (sum(f(x) * s for f, s in zip(funcs, sol)) - shift) + median


class QuantileRegression:
    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------
    def __init__(self, data=None):
        if data is None:
            data = []
        self._data = data
        self._basis_funcs = []
        self._probs = []  # np.atleast_1d(probs)
        self._regression_quantiles = []

    def validate_inputs(self, funcs, probs):
        if not (isinstance(self._data, np.ndarray) and self._data.shape[1] >= 2):
            raise ValueError(
                "The data argument is expected to be a matrix of numbers with two columns, a numeric vector, or a time series.")
        if len(funcs) < 1:
            raise ValueError(
                "The second argument is expected to be list of functions to be fitted with at least one element.")
        if not all(0 <= p <= 1 for p in probs):
            raise ValueError("The third argument is expected to be a list of numbers representing probabilities.")

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------
    def take_data(self):
        """Take the data."""
        return self._data

    def take_basis_funcs(self):
        """Take the basis functions."""
        return self._basis_funcs

    def take_probs(self):
        """Take the probabilities."""
        return self._probs

    def take_regression_quantiles(self):
        """Take the regression quantiles."""
        return self._regression_quantiles

    # ------------------------------------------------------------------
    # Fit function basis
    # ------------------------------------------------------------------
    def qr_fit(self, funcs, probs=None, **opts):
        if probs is None:
            probs = [0.25, 0, 5, 0.75]
        return self.quantile_regression_fit(funcs, probs, **opts)

    def quantile_regression_fit(self, funcs, probs, **opts):
        # It is unlikely that methods other than the LP one will be implemented,
        # but let have this redirection method just in case.
        if probs is None:
            probs = [0.25, 0, 5, 0.75]
        return self.lp_quantile_regression_fit(funcs, probs, **opts)

    def lp_quantile_regression_fit(self, funcs, probs, **opts):

        # Validate basis functions and probabilities
        self.validate_inputs(funcs, probs)

        # Assign for later retrieval / reference
        data = np.array(self._data)
        self._basis_funcs = funcs
        self._probs = probs

        y_median = 0
        y_factor = 1
        y_shift = 0
        n = data.shape[0]

        if np.min(data[:, -1]) < 0:
            y_median = np.median(data[:, -1])
            y_factor = np.percentile(data[:, -1], 75) - np.percentile(data[:, -1], 25)
            data[:, -1] = (data[:, -1] - y_median) / y_factor
            y_shift = np.abs(np.min(data[:, -1]))
            data[:, -1] += y_shift

        pFuncs = [lambda *args, f=fx: f(args[0]) for fx in funcs]
        mat = [np.apply_along_axis(_apply_f, 1, data, f1) for f1 in pFuncs]
        mat = np.array(mat).T
        mat = np.hstack([mat, identity(n).toarray(), -identity(n).toarray()])
        mat = mat.astype(float)

        qr_solutions = []
        for q in probs:
            c = np.concatenate([np.zeros(len(funcs)), np.ones(n) * q, np.ones(n) * (1 - q)])
            bounds = [(None, None)] * len(funcs) + [(0, None)] * (2 * n)
            res = linprog(c, A_eq=mat, b_eq=data[:, -1], bounds=bounds, method='highs', options=opts)
            if res.success and len(res.x) > len(funcs):
                qr_solutions.append(res.x[:len(funcs)])
            else:
                qr_solutions.append(np.zeros(len(funcs)))

        if y_median == 0 and y_factor == 1:
            self._regression_quantiles = [_make_combined_function(funcs, sol) for sol in qr_solutions]
        else:
            self._regression_quantiles = [
                _make_combined_function(funcs, sol, factor=y_factor, shift=y_shift, median=y_median)
                for sol in qr_solutions]

        return self
    
    # ------------------------------------------------------------------
    # Fit with B-splines
    # -----------------------------------------------------------------
    def qr(self, knots, probs=None, order: int = 3, **opts):
        return self.lp_spline_quantile_regression(knots, probs, order, **opts)

    def quantile_regression(self, knots, probs=None, order: int = 3, **opts):
        if probs is None:
            probs = [0.25, 0, 5, 0.75]
        return self.lp_spline_quantile_regression(knots, probs, order, **opts)

    def lp_spline_quantile_regression(self, knots, probs, order: int, **opts):

        # Validated probs
        if not all(0 <= p <= 1 for p in probs):
            raise ValueError("The argument probs is expected to be a list of numbers representing probabilities.")
        self._probs = probs

        # Knots is an integer
        if isinstance(knots, int):
            min_data = np.min(self._data[:, 0])
            max_data = np.max(self._data[:, 0])
            knots = np.linspace(0, 1, knots + 1) * (max_data - min_data) + min_data
            return self.lp_spline_quantile_regression(knots, probs, order, **opts)

        # Knots is an array
        data = np.array(self._data)
        knots = np.sort(knots)
        y_median = 0
        y_factor = 1
        y_shift = 0
        n = data.shape[0]

        if np.min(data[:, 1]) < 0:
            y_median = np.median(data[:, 1])
            y_factor = np.percentile(data[:, 1], 75) - np.percentile(data[:, 1], 25)
            data[:, 1] = (data[:, 1] - y_median) / y_factor
            y_shift = abs(np.min(data[:, 1]))
            data[:, 1] += y_shift

        knots = np.concatenate(([knots[0]] * order, knots, [knots[-1]] * order))

        if len(knots) - order - 2 < 0:
            raise ValueError(
                f"The specified knots {knots} and interpolation order {order} produce no B-Spline basis functions. " +
                "The expression n - i - 2 should be non-negative, where n is the number of knots and i is the interpolation order.")

        pFuncs = [BSpline.basis_element(knots[i:i + order + 2]) for i in range(len(knots) - order - 1)]

        t = knots[math.ceil(len(knots) / 2)]
        if all(np.allclose(p(t), 0) for p in pFuncs):
            raise ValueError(
                f"The specified knots {knots} and interpolation order {order} " +
                "produced a list of zeroes instead of a list of B-Spline basis functions.")

        mat = np.vstack([np.hstack([p(data[i, 0]) for p in pFuncs]) for i in range(n)])
        mat = np.hstack([mat, np.identity(n), -np.identity(n)])
        mat = mat.astype(float)

        qr_solutions = []
        for q in probs:
            c = np.concatenate([np.zeros(len(pFuncs)), np.ones(n) * q, np.ones(n) * (1 - q)])
            bounds = [(None, None)] * len(pFuncs) + [(0, None)] * (2 * n)
            res = linprog(c, A_eq=mat, b_eq=data[:, -1], bounds=bounds, method='highs', options=opts)
            if res.success and len(res.x) > len(pFuncs):
                qr_solutions.append(res.x[:len(pFuncs)])
            else:
                qr_solutions.append(np.zeros(len(pFuncs)))

        if y_median == 0 and y_factor == 1:
            self._regression_quantiles = [_make_combined_function(pFuncs, sol) for sol in qr_solutions]
        else:
            self._regression_quantiles = [
                _make_combined_function(pFuncs, sol, factor=y_factor, shift=y_shift, median=y_median)
                for sol in qr_solutions]

        return self


# ===================================================================
# Quantile regression functions
# ===================================================================
def quantile_regression_fit(data, funcs, probs):
    if isinstance(data, (list, np.ndarray)) and len(data) > 0 and isinstance(data[0], (int, float)):
        data = np.column_stack((np.arange(len(data)), data))

    if isinstance(probs, float | int):
        probs = [probs, ]

    qrf = QuantileRegression(data).quantile_regression_fit(funcs=funcs, probs=probs)
    return qrf.take_regression_quantiles()


def quantile_regression(data, knots, probs=None, order: int = 3):
    if isinstance(data, (list, np.ndarray)) and len(data) > 0 and isinstance(data[0], (int, float)):
        data = np.column_stack((np.arange(len(data)), data))

    if isinstance(probs, float | int):
        probs = [probs, ]

    qrf = QuantileRegression(data).quantile_regression(knots=knots, probs=probs, order=order)
    return qrf.take_regression_quantiles()