import unittest
from DataTypeSystem import deduce_type
from DataTypeSystem.TypeClasses import Assoc, Atom, Pair, Struct, Tuple, Vector
import datetime


class MyTestCase(unittest.TestCase):
    dsTitanic = [
        {"passengerSex": "male", "id": "835", "passengerClass": "3rd", "passengerSurvival": "died", "passengerAge": 30},
        {"passengerAge": 60, "passengerSex": "male", "passengerSurvival": "died", "passengerClass": "1st", "id": "280"},
        {"passengerClass": "3rd", "passengerSex": "male", "passengerAge": 10, "passengerSurvival": "survived",
         "id": "734"},
        {"id": "1029", "passengerAge": -1, "passengerSurvival": "survived", "passengerClass": "3rd",
         "passengerSex": "female"},
        {"passengerSurvival": "survived", "passengerClass": "3rd", "passengerAge": 40, "passengerSex": "female",
         "id": "760"},
        {"passengerClass": "1st", "id": "207", "passengerAge": 40, "passengerSex": "male", "passengerSurvival": "died"},
        {"passengerAge": 20, "passengerSex": "male", "id": "653", "passengerClass": "3rd", "passengerSurvival": "died"},
        {"passengerSurvival": "died", "passengerClass": "1st", "passengerAge": 60, "passengerSex": "male", "id": "301"},
        {"passengerAge": 20, "passengerSex": "male", "id": "1191", "passengerClass": "3rd",
         "passengerSurvival": "survived"},
        {"passengerAge": -1, "passengerClass": "1st", "passengerSurvival": "survived", "id": "236",
         "passengerSex": "male"},
        {"id": "1256", "passengerSurvival": "died", "passengerAge": -1, "passengerClass": "3rd",
         "passengerSex": "male"},
        {"id": "444", "passengerAge": 30, "passengerClass": "2nd", "passengerSurvival": "died", "passengerSex": "male"},
        {"passengerAge": 80, "id": "62", "passengerSurvival": "survived", "passengerSex": "female",
         "passengerClass": "1st"},
        {"passengerSurvival": "survived", "passengerClass": "1st", "id": "221", "passengerSex": "female",
         "passengerAge": 20},
        {"passengerAge": 10, "id": "1057", "passengerClass": "3rd", "passengerSurvival": "survived",
         "passengerSex": "male"},
        {"passengerAge": 30, "passengerSurvival": "died", "id": "668", "passengerClass": "3rd",
         "passengerSex": "female"},
        {"passengerSex": "female", "passengerSurvival": "survived", "passengerClass": "3rd", "id": "1068",
         "passengerAge": 20},
        {"id": "1198", "passengerSex": "male", "passengerSurvival": "died", "passengerAge": -1,
         "passengerClass": "3rd"},
        {"passengerAge": 20, "passengerSurvival": "survived", "passengerSex": "female", "id": "1261",
         "passengerClass": "3rd"},
        {"id": "937", "passengerSex": "female", "passengerClass": "3rd", "passengerAge": 30,
         "passengerSurvival": "survived"}]

    # 1
    def test_whole_set(self):
        self.assertEqual(
            str(deduce_type(self.dsTitanic)),
            'Vector(Struct([id, passengerAge, passengerClass, passengerSex, passengerSurvival], [Str, Int, Str, Str, Str]), 20)')

    # 2
    def test_record1(self):
        self.assertEqual(
            str(deduce_type(self.dsTitanic[12])),
            'Struct([id, passengerAge, passengerClass, passengerSex, passengerSurvival], [Str, Int, Str, Str, Str])')

    # 3
    def test_record2(self):
        self.assertEqual(
            str(deduce_type(self.dsTitanic[12].sort(key=lambda x: x.key), list)),
            'Tuple([Atom((Str)), Atom((Int)), Atom((Str)), Atom((Str)), Atom((Str))])')

    # 4
    def test_record3(self):
        self.assertEqual(
            str(deduce_type(self.dsTitanic[12]['passengerClass'])),
            'Atom(Str)')


if __name__ == '__main__':
    unittest.main()
