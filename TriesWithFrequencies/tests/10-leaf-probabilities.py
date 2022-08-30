# Follows the tests in
#   https://github.com/antononcube/Raku-ML-TriesWithFrequencies/blob/main/t/10-leaf-probabilities.rakutest

import unittest

from TriesWithFrequencies.TriesWithFrequencies import *


class LeafProbabilities(unittest.TestCase):
    words = ["bar", "bark", "bare", "cam", "came", "camelia"]

    tr = trie_create_by_split(words)

    def test_overall_1(self):
        pass


if __name__ == '__main__':
    unittest.main()
