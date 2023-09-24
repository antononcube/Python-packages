import unittest
from DataTypeSystem import deduce_type
from DataTypeSystem.TypeClasses import Assoc, Atom, Pair, Struct, Tuple, Vector
import datetime


class TestDeduceType(unittest.TestCase):
    dsRandNum = [
        {'A': 5.295105534105463, 'B': 2.4765132431861057},
        {'A': 5.504432770843629, 'B': 8.252672576017405},
        {'A': 0.47585824504772667, 'B': 4.6263512559214215},
        {'A': 3.5677811370087187e0, 'B': 6.861688593804621e0},
        {'A': 8.069906679462077e0, 'B': 5.504368820762937e0},
        {'A': 2.7870773247470213e0, 'B': 3.081614241542895e0},
        {'A': 4.688921458531033e0, 'B': 8.881239727023592e0}
    ]

    hRand = {
        "Aleppo": "Zealander",
        "Karaites": 5.512476726477258,
        "McGraw": 4.141810176531181,
        "angioplasty": "audit",
        "atheism": "chow",
        "brake": "problematical",
        "cardiology": 8.947919113468533,
        "commination": 2.619295707156705,
        "eschatological": 7.442247882717225,
        "handwriting": "Helios",
        "koudou": 3.4686291412158865,
        "masturbate": 8.026980830683481,
        "politically": 0.4971539286542881,
        "pyridoxamine": "thriftiness",
        "retired": "gripes",
        "scrumpy": "Paternoster",
        "sojourner": "overrefinement",
        "tortfeasor": 1.726557224751012,
        "usage": 8.428214682624322,
        "xcviii": "sandfly"
    }

    dsRandNum_dict = dict(zip('abcdefghijklmnopqrstuvwxyz', dsRandNum))

    # 1
    def test_deduce_type_dataset1(self):
        self.assertEqual(
            str(deduce_type(self.dsRandNum)),
            "Vector(Assoc(Atom(<class 'str'>), Atom(<class 'float'>), 2), 7)")

    # 2
    def test_deduce_type_dict1(self):
        self.assertEqual(
            str(deduce_type(self.dsRandNum_dict)),
            "Assoc(Atom(<class 'str'>), Assoc(Atom(<class 'str'>), Atom(<class 'float'>), 2), 7)")

    # 3
    def test_deduce_type_dict2(self):
        self.assertEqual(
            'Vector(None, 20)',
            str(deduce_type(list(self.hRand.items()), tally=False)))

    # 4
    def test_deduce_type_dict3(self):
        self.assertEqual(
            str(deduce_type(list(self.hRand.items()), tally=True)),
            "Tuple([(\"Pair(Atom(<class 'str'>), Atom(<class 'float'>))\", 10), (\"Pair(Atom(<class 'str'>), Atom(<class 'str'>))\", 10)], 20)"
        )

    # 5
    def test_deduce_type_datetime1(self):
        dsIRC10 = [
            {
                "DateString": "2020-12-23",
                "DateTime": datetime.datetime(2020, 12, 23, 14, 7, 0),
                "Nick": "Watson",
                "TimeBucket": "2020-12-23_14",
                "Timestamp": "2020-12-23Z14:07",
                "Weekday": 3,
            },
            {
                "DateString": "2019-10-29",
                "DateTime": datetime.datetime(2019, 10, 29, 15, 13, 0),
                "Nick": "Roxy",
                "TimeBucket": "2019-10-29_15",
                "Timestamp": "2019-10-29Z15:13-0001",
                "Weekday": 2,
            },
            {
                "DateString": "2020-08-06",
                "DateTime": datetime.datetime(2020, 8, 6, 18, 52, 0),
                "Nick": "Jimi",
                "TimeBucket": "2020-08-06_18",
                "Timestamp": "2020-08-06Z18:52-0002",
                "Weekday": 4,
            },
            {
                "DateString": "2021-11-18",
                "DateTime": datetime.datetime(2021, 11, 18, 2, 36, 0),
                "Nick" : "Tucker",
                "TimeBucket": "2021-11-18_2",
                "Timestamp": "2021-11-18Z02:3",
                "Weekday": 4,
            }]

        self.assertEqual(
            str(deduce_type(dsIRC10)),
            "Vector(Assoc(Atom(<class 'str'>), Atom(<class 'str'>), 6), 4)"
        )

    # 6
    def test_deduce_type_datetime2(self):

        dsTable11 = [
            {"Date": datetime.date(2020, 12, 23), "Nick": "Watson", "Weekday": 3 / 7},
            {"Date": datetime.date(2019, 10, 29), "Nick": "Roxy", "Weekday": 2 / 3},
            {"Date": datetime.date(2020, 8, 6), "Nick": "Jimi", "Weekday": 4 / 5},
            {"Date": datetime.date(2021, 11, 18), "Nick": "Tucker", "Weekday": 4 / 9},
        ]

        self.assertEqual(str(deduce_type(dsTable11)),
                         "Vector(Assoc(Atom(<class 'str'>), None, 3), 4)")


if __name__ == '__main__':
    unittest.main()
