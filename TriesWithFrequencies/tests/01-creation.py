# Follows the tests in
#   https://github.com/antononcube/Raku-ML-TriesWithFrequencies/blob/main/t/01-creation.rakutest

import unittest

from TriesWithFrequencies.TriesWithFrequencies import *


class Creation(unittest.TestCase):

    def test_create_1(self):
        # make with one word
        tr = trie_create(list("bar"))
        self.assertTrue(isinstance(tr, dict))

    def test_create_2(self):
        # make with one word
        tr = trie_create_by_split(["bar"])
        self.assertTrue(isinstance(tr, dict))

    def test_create_3(self):
        # equivalence of creation
        tr1 = trie_create([list("bar")])
        tr2 = trie_create_by_split(["bar"])
        self.assertEqual(tr1, tr2)

    def test_create_4(self):
        # merge equivalence to creation-by-splitting
        tr1 = trie_merge(trie_create([list("bar")]), trie_create([list("bar")]))
        tr2 = trie_create_by_split(["bar", "bar"])
        self.assertEqual(tr1, tr2)

    def test_create_5(self):
        # insert test 1
        tr = trie_insert(trie_create_by_split(["bar"]), list("balk"))
        self.assertTrue(isinstance(tr, dict))

    def test_create_6(self):
        # creation by slit long
        tr = trie_create_by_split(["bar", "bark", "balk", "cat", "cast"])
        self.assertTrue(isinstance(tr, dict))

    def test_create_7(self):
        # equivalence test
        words1 = ["bar", "barman", "bask", "bell", "best"]
        words2 = [list(x) for x in words1]
        tr1 = trie_create_by_split(words1)
        tr2 = trie_create(words2)
        self.assertEqual(tr1, tr2)

    def test_create_8(self):
        words1 = ["bar", "barman", "bask", "bell", "best"]
        words2 = ["bar", "barman", "bask", "car", "cast"]
        tr1 = trie_create_by_split(words1)
        tr2 = trie_create_by_split(words2)
        tr3 = trie_merge(tr1, tr2)

        # same trie after merging 1
        self.assertEqual(tr1, trie_create_by_split(words1))

        # same trie after merging 2
        self.assertEqual(tr2, trie_create_by_split(words2))


if __name__ == '__main__':
    unittest.main()
