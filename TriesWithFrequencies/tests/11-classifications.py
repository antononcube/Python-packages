# Follows the tests in
#   https://github.com/antononcube/Raku-ML-TriesWithFrequencies/blob/main/t/11-classificaitons.rakutest

import unittest

from TriesWithFrequencies.TriesWithFrequencies import *


class Classifications(unittest.TestCase):
    words1 = [*(["bar"] * 6), *(["bark"] * 3), *(["bare"] * 2), *(["cam"] * 3), "came", *(["camelia"] * 4)]

    tr0 = trie_create_by_split(words1)
    tr1 = trie_node_probabilities(tr0)

    # TRIE_ROOT = > 1.0
    # ├─b = > 0.5789473684210527
    # │ └─a = > 1.0
    # │   └─r = > 1.0
    # │     ├─k = > 0.2727272727272727
    # │     └─e = > 0.18181818181818182
    # └─c = > 0.42105263157894735
    #   └─a = > 1.0
    #     └─m = > 1.0
    #       └─e = > 0.625
    #         └─l = > 0.8
    #           └─i = > 1.0
    #             └─a = > 1.0

    def test_classifications_1(self):
        # Simple classify call
        self.assertTrue(trie_classify(self.tr1, list("bar")) in set(["r", "e"]))

    def test_classifications_2(self):
        # Classify and give probabilities
        res = trie_classify(self.tr1, list("bar"), prop="Probabilities")
        self.assertEqual(res, {'r': 0.5454545454545454, 'k': 0.2727272727272727, 'e': 0.18181818181818182})


if __name__ == '__main__':
    unittest.main()
