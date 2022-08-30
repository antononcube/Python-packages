# Follows the tests in
#   https://github.com/antononcube/Raku-ML-TriesWithFrequencies/blob/main/t/08-overall-from-JavaTrie.rakutest

import unittest

from TriesWithFrequencies.TriesWithFrequencies import *


class OverallFromJavaTrie(unittest.TestCase):
    words = ["bark", "barkeeper", "barkeepers", "barkeep", "barks", "barking", "barked", "barker", "barkers"]
    words2 = ["bar", "barring", "car", "care", "caress", "cold", "colder"]

    tr = trie_create_by_split(words)

    def test_overall_1(self):
        pass


if __name__ == '__main__':
    unittest.main()
