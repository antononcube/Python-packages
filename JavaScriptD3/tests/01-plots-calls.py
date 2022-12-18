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


if __name__ == '__main__':
    unittest.main()
