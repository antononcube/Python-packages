import unittest

import pandas
from ROCFunctions import roc_functions


class ROCFuncCalculations(unittest.TestCase):
    rocs = [{'TruePositive': 61, 'FalsePositive': 14, 'TrueNegative': 108, 'FalseNegative': 131},
            {'TruePositive': 77, 'FalsePositive': 22, 'TrueNegative': 100, 'FalseNegative': 115},
            {'TruePositive': 102, 'FalsePositive': 27, 'TrueNegative': 95, 'FalseNegative': 90},
            {'TruePositive': 120, 'FalsePositive': 30, 'TrueNegative': 92, 'FalseNegative': 72},
            {'TruePositive': 130, 'FalsePositive': 31, 'TrueNegative': 91, 'FalseNegative': 62},
            {'TruePositive': 141, 'FalsePositive': 31, 'TrueNegative': 91, 'FalseNegative': 51},
            {'TruePositive': 145, 'FalsePositive': 33, 'TrueNegative': 89, 'FalseNegative': 47},
            {'TruePositive': 150, 'FalsePositive': 37, 'TrueNegative': 85, 'FalseNegative': 42},
            {'TruePositive': 154, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 38},
            {'TruePositive': 159, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 33},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 38, 'TrueNegative': 84, 'FalseNegative': 32},
            {'TruePositive': 160, 'FalsePositive': 40, 'TrueNegative': 82, 'FalseNegative': 32},
            {'TruePositive': 164, 'FalsePositive': 44, 'TrueNegative': 78, 'FalseNegative': 28},
            {'TruePositive': 165, 'FalsePositive': 48, 'TrueNegative': 74, 'FalseNegative': 27},
            {'TruePositive': 166, 'FalsePositive': 49, 'TrueNegative': 73, 'FalseNegative': 26},
            {'TruePositive': 172, 'FalsePositive': 54, 'TrueNegative': 68, 'FalseNegative': 20},
            {'TruePositive': 176, 'FalsePositive': 63, 'TrueNegative': 59, 'FalseNegative': 16},
            {'TruePositive': 183, 'FalsePositive': 71, 'TrueNegative': 51, 'FalseNegative': 9},
            {'TruePositive': 183, 'FalsePositive': 80, 'TrueNegative': 42, 'FalseNegative': 9},
            {'TruePositive': 188, 'FalsePositive': 89, 'TrueNegative': 33, 'FalseNegative': 4},
            {'TruePositive': 189, 'FalsePositive': 99, 'TrueNegative': 23, 'FalseNegative': 3},
            {'TruePositive': 190, 'FalsePositive': 103, 'TrueNegative': 19, 'FalseNegative': 2},
            {'TruePositive': 190, 'FalsePositive': 110, 'TrueNegative': 12, 'FalseNegative': 2},
            {'TruePositive': 191, 'FalsePositive': 115, 'TrueNegative': 7, 'FalseNegative': 1}]

    def test_FPR_over_ROC_record(self):
        self.assertTrue(isinstance(roc_functions('FPR')(self.rocs[12]), float))

    def test_FPR_over_array_of_ROC_records(self):
        self.assertTrue(isinstance(roc_functions('FPR')(self.rocs), list))

    def test_AUROC(self):
        self.assertTrue(isinstance(roc_functions('AUROC')(self.rocs), float))

    def test_array_of_arrays(self):
        funcs = ["PPV", "NPV", "TPR", "ACC", "SPC", "MCC"]

        rocRes = [{f: roc_functions(f)(x) for f in funcs} for x in self.rocs]

        self.assertTrue(isinstance(rocRes, list))

        dfROCs = pandas.DataFrame(rocRes)
        self.assertTrue(isinstance(dfROCs, pandas.DataFrame))



if __name__ == '__main__':
    unittest.main()
