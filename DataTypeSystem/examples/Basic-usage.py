import DataTypeSystem.TypeSystem
from DataTypeSystem.Examiner import Examiner

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
