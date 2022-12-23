import unittest

from JavaScriptD3.Plots import *


class PlotCalls(unittest.TestCase):
    arrXY = [{"x": 1, "y": 2}, {"x": 3, "y": 2}, {"x": 10, "y": 12}, {"x": -1, "y": 6}]
    arrNP = numpy.array([1, 3, 13, 23, 5, 3])
    arrXYG = [{'x': 0.9987770286477529, 'y': -0.1669808909993505, 'group': 'barista'},
              {'x': 1.3719915949567854, 'y': -0.3228045137866323, 'group': 'barista'},
              {'x': 1.4214077061088088, 'y': -0.51161730864072, 'group': 'c'},
              {'x': -0.03844414485091125, 'y': 0.1295896384396334, 'group': 'barista'},
              {'x': 1.4303715809006776, 'y': 0.9872612652722519, 'group': 'c'},
              {'x': -0.4008885191335476, 'y': 0.8700794132137347, 'group': 'a'},
              {'x': -0.3973281647300204, 'y': -0.5411389561920639, 'group': 'a'},
              {'x': -0.18697491664232196, 'y': -0.6156595219377975, 'group': 'barista'},
              {'x': 2.1998496714777893, 'y': -0.3161493421241798, 'group': 'c'},
              {'x': 0.5068763463111668, 'y': 0.15463026938869173, 'group': 'a'}]
    tsRand1 = [["1970-04-15", 3713.567898300845e0], ["1970-05-19", 4466.645127680633e0],
               ["1970-07-28", 4962.707644206486e0],
               ["1970-08-07", 4528.997415904021e0], ["1970-08-13", 5365.402079145894e0],
               ["1971-11-08", 8945.23867847915e0],
               ["1971-12-17", 9116.73075372545e0], ["1972-05-01", 10273.836690623637e0],
               ["1973-06-24", 10881.867233348434e0],
               ["1973-12-09", 13651.519872995486e0], ["1974-04-26", 13848.96559635215e0],
               ["1974-05-24", 13374.12844167666e0],
               ["1974-10-12", 16104.790409557521e0], ["1974-11-12", 14592.645875545222e0],
               ["1975-09-12", 14009.729561951815e0],
               ["1976-04-21", 14981.351834039335e0], ["1976-09-19", 17399.95561782246e0],
               ["1976-11-28", 15864.213638829973e0],
               ["1976-12-15", 16465.55117213528e0], ["1977-06-02", 19407.501334451685e0]]
    tsRand2 = [{"date": x[0], "value": x[1]} for x in tsRand1]

    def test_1(self):
        res = js_d3_list_plot(self.arrXY, fmt="html")
        self.assertTrue(isinstance(res, str))

    def test_2(self):
        res = js_d3_list_plot(self.arrNP,
                              title="First plot",
                              x_axis_label="My X",
                              y_axis_label="my Y",
                              grid_lines=12,
                              margins={"top": 140},
                              legends=True,
                              fmt="html"
                              )
        self.assertTrue(isinstance(res, str))

    def test_3(self):
        res = js_d3_list_plot(self.arrXYG, fmt="html")
        self.assertTrue(isinstance(res, str))

    def test_4(self):
        res = js_d3_list_line_plot(self.arrXY, fmt="html")
        self.assertTrue(isinstance(res, str))

    def test_5(self):
        res = js_d3_list_line_plot(self.arrNP,
                                   title="Some plot",
                                   x_axis_label="My X",
                                   y_axis_label="My Y",
                                   grid_lines=12,
                                   margins={"top": 140},
                                   legends=True,
                                   fmt="html"
                                   )
        self.assertTrue(isinstance(res, str))

    def test_6(self):
        res = js_d3_list_line_plot(self.arrXYG, fmt="html")
        self.assertTrue(isinstance(res, str))

    def test_7(self):
        res = js_d3_date_list_plot(self.tsRand1, fmt="script")
        self.assertTrue(isinstance(res, str))

    def test_8(self):
        res = js_d3_date_list_plot(self.tsRand2, fmt="script")
        self.assertTrue(isinstance(res, str))

    def test9(self):
        res = js_d3_list_plot(
            list(zip(numpy.random.uniform(30, 70, 400), numpy.random.normal(120, 10, 400))),
            x_axis_label='random-real',
            y_axis_label='N[12,19]',
            title='Real 2D data')
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
