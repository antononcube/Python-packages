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
        # TRIEROOT = > 5.0
        # └─b = > 5.0
        #   ├─a = > 3.0
        #   │ ├─r = > 2.0
        #   │ │ └─m = > 1.0
        #   │ │   └─a = > 1.0
        #   │ │     └─n = > 1.0
        #   │ └─s = > 1.0
        #   │   └─k = > 1.0
        #   └─e = > 2.0
        #     ├─l = > 1.0
        #     │ └─l = > 1.0
        #     └─s = > 1.0
        #       └─t = > 1.0
        #
        # {'total': 14, 'internal': 10, 'leaves': 4}

        # created trie
        self.assertTrue(isinstance(self.tr, dict))

    def test_basic_use_2(self):
        # node probabilities comparison';
        tr2 = trie_node_probabilities(self.tr)

        self.assertTrue(isinstance(tr2, dict))

        tr3 = {'TRIEROOT': {'b': {'a': {
            'r': {'m': {'a': {'n': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 1.0}, 'TRIEVALUE': 0.5},
                  'TRIEVALUE': 0.6666666666666666}, 's': {'k': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 0.3333333333333333},
            'TRIEVALUE': 0.6}, 'e': {'l': {'l': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 0.5},
                                     's': {'t': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 0.5}, 'TRIEVALUE': 0.4},
            'TRIEVALUE': 1.0}, 'TRIEVALUE': 1.0}}

        self.assertEqual(tr2, tr3)

    def test_basic_use_3(self):
        self.assertEqual(trie_node_counts(self.tr), {'total': 14, 'internal': 10, 'leaves': 4})

    def test_basic_use_4(self):
        # trie node counts are the same for tries with same words and different frequencies
        tr2 = trie_create_by_split([*self.words, *self.words])
        self.assertEqual(trie_node_counts(self.tr), trie_node_counts(tr2))

    def test_shrink_1(self):
        trShrunk = trie_shrink(self.tr)
        # trie_form(trShrunk)
        # TRIEROOT => 5.0
        # └─b => 5.0
        #   └─a => 3.0
        #     └─r => 2.0
        #       └─man => 1.0
        #     └─sk => 1.0
        #   └─e => 2.0
        #     └─ll => 1.0
        #     └─st => 1.0

        trExpected = {'TRIEROOT': {'TRIEVALUE': 5.0, 'b': {'TRIEVALUE': 5.0, 'a': {'TRIEVALUE': 3.0,
                                                                                   'r': {'TRIEVALUE': 2.0,
                                                                                         'man': {'TRIEVALUE': 1.0}},
                                                                                   'sk': {'TRIEVALUE': 1.0}},
                                                           'e': {'TRIEVALUE': 2.0, 'll': {'TRIEVALUE': 1.0},
                                                                 'st': {'TRIEVALUE': 1.0}}}}}
        self.assertEqual(trShrunk[TRIE_ROOT]["b"][TRIE_VALUE], len(self.words))
        self.assertEqual(trShrunk, trExpected)

    def test_shrink_2(self):
        ptrShrunk = trie_shrink(trie_node_probabilities(self.tr))
        # trie_form(ptrShrunk)
        # TRIEROOT => 1.0
        # └─b => 1.0
        #   └─a => 0.6
        #     └─r => 0.6666666666666666
        #       └─man => 1.0
        #     └─sk => 1.0
        #   └─e => 0.4
        #     └─ll => 1.0
        #     └─st => 1.0

        trExpected = {'TRIEROOT': {'TRIEVALUE': 1.0, 'b': {'TRIEVALUE': 1.0, 'a': {'TRIEVALUE': 0.6, 'r': {
            'TRIEVALUE': 0.6666666666666666, 'man': {'TRIEVALUE': 1.0}}, 'sk': {'TRIEVALUE': 1.0}},
                                                           'e': {'TRIEVALUE': 0.4, 'll': {'TRIEVALUE': 1.0},
                                                                 'st': {'TRIEVALUE': 1.0}}}}}

        self.assertEqual(ptrShrunk[TRIE_ROOT]["b"][TRIE_VALUE], 1.0)
        self.assertEqual(ptrShrunk, trExpected)


if __name__ == '__main__':
    unittest.main()
