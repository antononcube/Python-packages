import numpy as np
from scipy.optimize import linprog
from scipy.sparse import identity, hstack, vstack

def _apply_f(row, f):
    return f(*row[:-1])

def _make_combined_function(funcs, sol, factor=1, shift=0, median=0):
    return lambda x: factor * (sum(f(x) * s for f, s in zip(funcs, sol)) - shift) + median

class QuantileRegressionFit:
    def __init__(self, data, funcs, probs):
        self.data = data
        self.funcs = funcs
        self.probs = np.atleast_1d(probs)
        self.validate_inputs()

    def validate_inputs(self):
        if not (isinstance(self.data, np.ndarray) and self.data.shape[1] >= 2):
            raise ValueError(
                "The first argument is expected to be a matrix of numbers with two columns, a numeric vector, or a time series.")
        if len(self.funcs) < 1:
            raise ValueError(
                "The second argument is expected to be list of functions to be fitted with at least one element.")
        if not all(0 <= p <= 1 for p in self.probs):
            raise ValueError("The third argument is expected to be a list of numbers representing probabilities.")

    def fit(self):
        # It is unlikely that methods other than the LP one will be implemented,
        # but let have this redirection method just in case.
        return self.lp_quantile_regression_fit()

    def lp_quantile_regression_fit(self, **opts):
        data = np.array(self.data)
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

        pFuncs = [lambda *args, f=fx: f(args[0]) for fx in self.funcs]
        mat = [np.apply_along_axis(_apply_f, 1, data, f1) for f1 in pFuncs]
        mat = np.array(mat).T
        mat = np.hstack([mat, identity(n).toarray(), -identity(n).toarray()])
        mat = mat.astype(float)

        qr_solutions = []
        for q in self.probs:
            c = np.concatenate([np.zeros(len(self.funcs)), np.ones(n) * q, np.ones(n) * (1 - q)])
            bounds = [(None, None)] * len(self.funcs) + [(0, None)] * (2 * n)
            res = linprog(c, A_eq=mat, b_eq=data[:, -1], bounds=bounds, method='highs', options=opts)
            if res.success and len(res.x) > len(self.funcs):
                qr_solutions.append(res.x[:len(self.funcs)])
            else:
                qr_solutions.append(np.zeros(len(self.funcs)))

        if y_median == 0 and y_factor == 1:
            return [_make_combined_function(self.funcs, sol) for sol in qr_solutions]
        else:
            return [_make_combined_function(self.funcs, sol, factor=y_factor, shift=y_shift, median=y_median)
                    for sol in qr_solutions]


def quantile_regression_fit(data, funcs, probs):
    if isinstance(data, (list, np.ndarray)) and len(data) > 0 and isinstance(data[0], (int, float)):
        data = np.column_stack((np.arange(len(data)), data))
    elif hasattr(data, 'Path'):
        data = np.array(data.Path)

    qrf = QuantileRegressionFit(data, funcs, probs)
    return qrf.fit()