import unittest

from QuantileRegression.QuantileRegression import quantile_regression_fit
import numpy as np
from scipy.stats import norm



def test_approx_under_fraction(rq, data, frac, tol=0.01):
    x, y = data[:, 0], data[:, 1]
    count = sum(y[i] <= rq(x[i]) for i in range(len(x)))
    return abs(count / len(x) - frac) <= tol


np.random.seed(0)

class QuantileRegressionFit(unittest.TestCase):
    dist_data = np.array([[x, np.exp(-x ** 2) + norm.rvs(scale=0.15)] for x in np.arange(-3, 3.2, 0.2)])
    dist_data2 = np.array([[x, np.exp(-x ** 2) + norm.rvs(scale=0.15)] for x in np.arange(-3, 3.02, 0.02)])
    fin_data = np.array([16.17, 14.11, 13.48, 14.07, 14.08, 13.61, 13.63, 12.94, 11.29, 10.10, 7.5, 7.57, 10.16, 10.39, 9.99, 10.17, 9.44, 10.5, 10.45, 8.25, 8.94, 8.89])

    def test_distribution_data(self):
        self.assertTrue(np.all(np.isfinite(self.dist_data)) and np.all(np.isfinite(self.dist_data2)), "Distribution data")
        self.assertTrue(isinstance(self.dist_data, np.ndarray) and self.dist_data.shape[1] >= 2, "Distribution data shape")

    def test_financial_data(self):
        self.assertTrue(isinstance(self.fin_data, np.ndarray), "Financial data")

    def test_quantile_regression_fit_1(self):
        probs = np.arange(0.2, 1.0, 0.2)
        funcs = [lambda x: 1, lambda x: x, lambda x: np.exp(-x**2)]
        q_funcs = quantile_regression_fit(data = self.dist_data, funcs = funcs, probs = probs)
        self.assertTrue(isinstance(q_funcs, list) and
                        len(q_funcs) == len(probs) and
                        all(isinstance(f(12), float) for f in q_funcs), "test_quantile_regression_fit_1")

    def test_quantile_regression_fit_2(self):
        probs = np.arange(0.2, 1.0, 0.2)
        funcs = [lambda x: 1, lambda x: x, lambda x: x**2]
        q_funcs = quantile_regression_fit(data = self.dist_data, funcs = funcs, probs = probs)
        self.assertTrue(isinstance(q_funcs, list) and
                        len(q_funcs) == len(probs) and
                        all(isinstance(f(12), float) for f in q_funcs), "test_quantile_regression_fit_2")

    def test_quantile_regression_fit_3(self):
        probs = np.arange(0.2, 1.0, 0.2)
        funcs = [lambda x: 1, lambda x: x, lambda x: x**2]
        q_funcs = quantile_regression_fit(data = self.fin_data, funcs = funcs, probs = probs)
        self.assertTrue(isinstance(q_funcs, list) and
                        len(q_funcs) == len(probs) and
                        all(isinstance(f(12), float) for f in q_funcs), "test_quantile_regression_fit_3")

    def test_quantile_regression_fit_4(self):
        probs = np.arange(0.2, 1.0, 0.2)
        funcs = [lambda x: 1, lambda x: x, lambda x: np.exp(-x**2)]
        q_funcs = quantile_regression_fit(data = [self.dist_data[i][1] for i in range(len(self.dist_data))],
                                          funcs = funcs,
                                          probs = probs)
        self.assertTrue(isinstance(q_funcs, list) and
                        len(q_funcs) == len(probs) and
                        all(isinstance(f(12), float) for f in q_funcs), "test_quantile_regression_fit_4")

    def test_quantile_regression_fit_separation_1(self):
        probs = np.arange(0.2, 1.0, 0.2)
        funcs = [(lambda x, i=i: np.cos(x * i)) for i in range(17)]
        q_funcs = quantile_regression_fit(data = self.dist_data2,
                                          funcs = funcs,
                                          probs = probs)
        sep_tests = [test_approx_under_fraction(q_funcs[i], data = self.dist_data2, frac= probs[i], tol = 0.03) for i in range(len(probs))]
        self.assertTrue(all(sep_tests), "test_quantile_regression_fit-separation-1")

if __name__ == '__main__':
    unittest.main()