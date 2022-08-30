# Follows the tests in
#   https://github.com/antononcube/Raku-ML-TriesWithFrequencies/blob/main/t/02-basic-use.rakutest

import unittest

from TriesWithFrequencies.TriesWithFrequencies import *


class BasicUse(unittest.TestCase):
    words = ["bar", "barman", "bask", "bell", "best"]
    tr = trie_create_by_split(words)

    def test_basic_use_1(self):
        # make with one word

        # trie_form(tr)
        # print(trie_node_counts(tr))

        # The commands above should produce the trie:
        # TRIE_ROOT = > 5.0
        # └─b = > 5.0
        # ├─a = > 3.0
        # │ ├─r = > 2.0
        # │ │ └─m = > 1.0
        # │ │   └─a = > 1.0
        # │ │     └─n = > 1.0
        # │ └─s = > 1.0
        # │   └─k = > 1.0
        # └─e = > 2.0
        # ├─l = > 1.0
        # │ └─l = > 1.0
        # └─s = > 1.0
        # └─t = > 1.0
        #
        # {'total': 14, 'internal': 10, 'leaves': 4}

        # created trie
        self.assertTrue(isinstance(self.tr, dict))

    def test_basic_use_2(self):
        # node probabilities comparison';
        tr2 = trie_node_probabilities(self.tr)

        self.assertTrue(isinstance(tr2, dict))

        tr3 = {'TRIE_ROOT': {'b': {'a': {
            'r': {'m': {'a': {'n': {'TRIE_VALUE': 1.0}, 'TRIE_VALUE': 1.0}, 'TRIE_VALUE': 0.5},
                  'TRIE_VALUE': 0.6666666666666666}, 's': {'k': {'TRIE_VALUE': 1.0}, 'TRIE_VALUE': 0.3333333333333333},
            'TRIE_VALUE': 0.6}, 'e': {'l': {'l': {'TRIE_VALUE': 1.0}, 'TRIE_VALUE': 0.5},
                                      's': {'t': {'TRIE_VALUE': 1.0}, 'TRIE_VALUE': 0.5}, 'TRIE_VALUE': 0.4},
            'TRIE_VALUE': 1.0}, 'TRIE_VALUE': 1.0}}

        self.assertEqual(tr2, tr3)

    def test_basic_use_3(self):
        self.assertEqual(trie_node_counts(self.tr), {'total': 14, 'internal': 10, 'leaves': 4})

    def test_basic_use_4(self):
        # trie node counts are the same for tries with same words and different frequencies
        tr2 = trie_create_by_split([*self.words, *self.words])
        self.assertEqual(trie_node_counts(self.tr), trie_node_counts(tr2))


if __name__ == '__main__':
    unittest.main()
