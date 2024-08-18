import numpy as np
from scipy.optimize import linprog
from scipy.sparse import identity, hstack, vstack

def _apply_f(row, f):
    return f(*row[:-1])

def _make_combined_function(funcs, sol, factor=1, shift=0, median=0):
    return lambda x: factor * (sum(f(x) * s for f, s in zip(funcs, sol)) - shift) + median


def lp_quantile_regression_fit(data, funcs, probs, **opts):
    data = np.array(data)
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
        return [_make_combined_function(funcs, sol) for sol in qr_solutions]
    else:
        return [_make_combined_function(funcs, sol, factor=y_factor, shift=y_shift, median=y_median)
                for sol in qr_solutions]