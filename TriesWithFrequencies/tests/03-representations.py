# Follows the tests in
#   https://github.com/antononcube/Raku-ML-TriesWithFrequencies/blob/main/t/03-representations.rakutest

import unittest

from TriesWithFrequencies.TriesWithFrequencies import *


class Representations(unittest.TestCase):
    words = ["bar", "barman", "bask", "bell", "best"]
    tr = trie_create_by_split(words)

    def test_representation_1(self):
        pass


if __name__ == '__main__':
    unittest.main()
