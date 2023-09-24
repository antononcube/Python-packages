from DataTypeSystem import deduce_type
from DataTypeSystem import record_types
from DataTypeSystem.Examiner import Examiner
from DataTypeSystem.Predicates import is_hash_of_hashes, is_array_of_pairs, is_array_of_hashes

import datetime

from RandomDataGenerators import *

ex = Examiner()

print(100 * '=')
ls1 = [2, 12, 2, 3, 23]
print(ls1)
print(ex.deduce_type(ls1))

print(100 * '=')
ls2 = random_word(5)
print(ls2)
print(ex.deduce_type(ls2))

print(100 * '=')
ls3 = [3, 340, "some", "choice", "words"]
print(ls3)
print(ex.deduce_type(ls3))
print(ex.deduce_type(ls3, tally=True))

print(100 * "=")
dc1 = {random_pet_name(1): v for v in range(12)}
print(dc1)
print(ex.deduce_type(dc1))

print(100 * "-")
print(list(dc1.items())[0])
print(type(list(dc1.items())[0]))

print(100 * "=")

dsTable = [
    {"Date": datetime.date(2020, 12, 23), "Nick": "Watson", "Weekday": 3 / 7},
    {"Date": datetime.date(2019, 10, 29), "Nick": "Roxy", "Weekday": 2 / 3},
    {"Date": datetime.date(2020, 8, 6), "Nick": "Jimi", "Weekday": 4 / 5},
    {"Date": datetime.date(2021, 11, 18), "Nick": "Tucker", "Weekday": 4 / 9},
]

print(is_array_of_hashes(dsTable))
ex = Examiner()
print(ex.is_reshapable(dsTable))
print(record_types(dsTable))