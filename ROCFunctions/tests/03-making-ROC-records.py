import unittest

import pandas
from ROCFunctions import to_roc_dict


class ROCRecords(unittest.TestCase):

    def test_to_roc_dict_1(self):
        rocs2 = to_roc_dict(
            true_label='True',
            false_label='False',
            actual=["True", "True", "False"],
            predicted=["False", "True", "False"],
            sep='@@')

        self.assertEqual(rocs2, {'TruePositive': 1, 'FalsePositive': 0, 'TrueNegative': 1, 'FalseNegative': 1})


if __name__ == '__main__':
    unittest.main()
