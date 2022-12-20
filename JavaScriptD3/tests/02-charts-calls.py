import unittest

from JavaScriptD3.Charts import *


class ChartCalls(unittest.TestCase):
    arrNP = numpy.random.normal(120, 4, 30)
    arrNP2D = numpy.random.normal(120, 4, (30, 2))
    arrNP3D = numpy.random.normal(120, 4, (30, 3))
    fruitsLongFormTr = [{'group': 'banana', 'variable': 'Nitrogen', 'value': 12},
                        {'group': 'poacee', 'variable': 'Nitrogen', 'value': 6},
                        {'group': 'sorgho', 'variable': 'Nitrogen', 'value': 11},
                        {'group': 'triticum', 'variable': 'Nitrogen', 'value': 19},
                        {'group': 'banana', 'variable': 'normal', 'value': 1},
                        {'group': 'poacee', 'variable': 'normal', 'value': 6},
                        {'group': 'sorgho', 'variable': 'normal', 'value': 28},
                        {'group': 'triticum', 'variable': 'normal', 'value': 6},
                        {'group': 'banana', 'variable': 'stress', 'value': 13},
                        {'group': 'poacee', 'variable': 'stress', 'value': 33},
                        {'group': 'sorgho', 'variable': 'stress', 'value': 12},
                        {'group': 'triticum', 'variable': 'stress', 'value': 1}]

    aRandXYZG = [{'x': -0.5764514571086383, 'y': 1.5822537004892718, 'z': -0.020744652301178383, 'group': 'c'},
                 {'x': -0.9112911293166143, 'y': 0.6587969785308456, 'z': -0.5506591416683007, 'group': 'b'},
                 {'x': -0.8450227742971823, 'y': -2.3136228400069228, 'z': -0.7812380341021887, 'group': 'a'},
                 {'x': 0.465744578346104, 'y': 0.14489761866247744, 'z': -0.5919198795863838, 'group': 'b'},
                 {'x': -0.07019495351255028, 'y': -0.07236706954698144, 'z': 0.39632832195732876, 'group': 'b'},
                 {'x': 0.2811620208608897, 'y': 0.3843675809015876, 'z': 0.07775065377667448, 'group': 'b'},
                 {'x': -0.5088847348184563, 'y': -0.6822764281083492, 'z': -1.2057824290040866, 'group': 'c'},
                 {'x': 0.6024003549874262, 'y': 0.022383245278385998, 'z': -0.9581092236769072, 'group': 'a'},
                 {'x': 1.2294753647433243, 'y': 0.5092849991407153, 'z': 0.5296964652287616, 'group': 'a'},
                 {'x': -1.3154411323571118, 'y': 0.06258331550802355, 'z': -1.264067931220498, 'group': 'a'}]

    def test_1(self):
        res = js_d3_bar_chart(self.arrNP, fmt="html")
        self.assertTrue(isinstance(res, str))

    def test_2(self):
        res = js_d3_bar_chart(self.fruitsLongFormTr,
                              title="First chart",
                              x_axis_label="My X",
                              y_axis_label="my Y",
                              grid_lines=12,
                              margins={"top": 140},
                              legends=True,
                              fmt="html"
                              )
        self.assertTrue(isinstance(res, str))

    def test_3(self):
        res = js_d3_histogram(self.arrNP, fmt="html")
        self.assertTrue(isinstance(res, str))

    def test_4(self):
        res = js_d3_bubble_chart(self.arrNP, fmt="html")
        self.assertTrue(isinstance(res, str))

    def test_5(self):
        res = js_d3_bubble_chart(self.arrNP2D, fmt="html")
        self.assertTrue(isinstance(res, str))

    def test_6(self):
        res = js_d3_bubble_chart(self.arrNP3D, fmt="html")
        self.assertTrue(isinstance(res, str))

    def test_7(self):
        res = js_d3_bubble_chart(self.aRandXYZG, fmt="html")
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
