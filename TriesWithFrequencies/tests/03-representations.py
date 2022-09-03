# Follows the tests in
#   https://github.com/antononcube/Raku-ML-TriesWithFrequencies/blob/main/t/03-representations.rakutest

import unittest

from TriesWithFrequencies.TriesWithFrequencies import *


class Representations(unittest.TestCase):
    words = ["bar", "barman", "bask", "bell", "best"]
    tr = trie_create_by_split(words)

    # TRIEROOT => 5.0
    # └─b => 5.0
    #   ├─a => 3.0
    #   │ ├─r => 2.0
    #   │ │ └─m => 1.0
    #   │ │   └─a => 1.0
    #   │ │     └─n => 1.0
    #   │ └─s => 1.0
    #   │   └─k => 1.0
    #   └─e => 2.0
    #     ├─l => 1.0
    #     │ └─l => 1.0
    #     └─s => 1.0
    #       └─t => 1.0
    def test_representation_1(self):

        ptr = trie_node_probabilities(self.tr)
        # trie_form(ptr) :
        # TRIEROOT => 1.0
        # └─b => 1.0
        #   ├─a => 0.6
        #   │ ├─r => 0.6666666666666666
        #   │ │ └─m => 0.5
        #   │ │   └─a => 1.0
        #   │ │     └─n => 1.0
        #   │ └─s => 0.3333333333333333
        #   │   └─k => 1.0
        #   └─e => 0.4
        #     ├─l => 0.5
        #     │ └─l => 1.0
        #     └─s => 0.5
        #       └─t => 1.0

        ptrExpected = {'TRIEROOT': {'b': {'a': {
            'r': {'m': {'a': {'n': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 1.0}, 'TRIEVALUE': 0.5},
                  'TRIEVALUE': 0.6666666666666666}, 's': {'k': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 0.3333333333333333},
            'TRIEVALUE': 0.6}, 'e': {'l': {'l': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 0.5},
                                     's': {'t': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 0.5}, 'TRIEVALUE': 0.4},
                                          'TRIEVALUE': 1.0}, 'TRIEVALUE': 1.0}}

        self.assertEqual(ptr, ptrExpected)
        self.assertEqual(ptr[TRIE_ROOT]["b"][TRIE_VALUE], 1.0)

        trExpected = {'TRIEROOT': {'b': {
            'a': {'r': {'TRIEVALUE': 2.0, 'm': {'a': {'n': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 1.0}, 'TRIEVALUE': 1.0}},
                  'TRIEVALUE': 3.0, 's': {'k': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 1.0}}, 'TRIEVALUE': 5.0,
            'e': {'l': {'l': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 1.0}, 'TRIEVALUE': 2.0,
                  's': {'t': {'TRIEVALUE': 1.0}, 'TRIEVALUE': 1.0}}}, 'TRIEVALUE': 5.0}}

        self.assertEqual(self.tr[TRIE_ROOT]["b"][TRIE_VALUE], 5.0)
        self.assertEqual(self.tr, trExpected)


if __name__ == '__main__':
    unittest.main()
