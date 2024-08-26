import unittest

from QuantileRegression.QuantileRegression import QuantileRegression
import scipy
import numpy
from numpy.ma.core import array


def test_approx_under_fraction(rq, data, frac, tol=0.01):
    x, y = data[:, 0], data[:, 1]
    count = sum(y[i] <= rq(x[i]) for i in range(len(x)))
    return abs(count / len(x) - frac) <= tol


numpy.random.seed(0)


class BasicFunctionalities(unittest.TestCase):
    x = numpy.linspace(0, 2, 240)
    y = numpy.sin(2 * numpy.pi * x) + numpy.random.normal(0, 0.4, x.shape)
    data = numpy.column_stack((x, y))
    funcs = [lambda x: 1, lambda x: x, lambda x: numpy.cos(x), lambda x: numpy.cos(3 * x), lambda x: numpy.cos(6 * x)]

    def test_make_1(self):
        obj = QuantileRegression(self.data)
        self.assertTrue(isinstance(obj.take_data(), numpy.ndarray))

    def test_qr_fit_1(self):
        obj = QuantileRegression(self.data)
        res = obj.quantile_regression_fit(funcs=self.funcs, probs=[0.2, 0.5, 0.8])
        self.assertTrue(isinstance(res, QuantileRegression))
        self.assertTrue(all(callable(item) for item in obj.take_regression_quantiles()))

    def test_qr_fit_2(self):
        obj = QuantileRegression(self.data)
        res = obj.qr_fit(funcs=self.funcs, probs=[0.2, 0.5, 0.8])
        self.assertTrue(test_approx_under_fraction(res.take_regression_quantiles()[2], obj.take_data(), 0.8))

    def test_quantile_regression_1(self):
        obj = QuantileRegression(self.data)
        res = obj.quantile_regression(knots = 5, probs=[0.2, 0.5, 0.8])
        self.assertTrue(isinstance(res, QuantileRegression))
        self.assertTrue(all(callable(item) for item in obj.take_regression_quantiles()))

    def test_quantile_regression_2(self):
        obj = QuantileRegression(self.data)
        res = obj.qr(knots = 6, probs=[0.2, 0.5, 0.8])
        self.assertTrue(test_approx_under_fraction(res.take_regression_quantiles()[2], obj.take_data(), 0.8))


if __name__ == '__main__':
    unittest.main()
