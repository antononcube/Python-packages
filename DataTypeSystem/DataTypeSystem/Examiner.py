import warnings
from collections import Counter
from DataTypeSystem.Predicates import is_hash_of_hashes, is_array_of_pairs

from DataTypeSystem.TypeClasses import Type, Atom, Pair, Vector, Tuple, Assoc, Struct
import datetime


class Examiner:
    max_enum_elems: int = 6
    max_struct_elems: int = 16
    max_tuple_elems: int = 16

    def __init__(self, max_enum_elems=6, max_struct_elems=16, max_tuple_elems=16):
        self.max_enum_elems = max_enum_elems
        self.max_struct_elems = max_struct_elems
        self.max_tuple_elems = max_tuple_elems

    def has_homogeneous_shape(self, l):
        return all(x.elems == l[0].elems for x in l)

    def has_homogeneous_type(self, l):
        if len(l) > 0 and (l[0] in [dict, list]):
            return all(type(x) == type(l[0]) for x in l)
        else:
            return all(type(x) == type(l[0]) for x in l[1:])

    def is_reshapable(self, data, iterable_type=list, record_type=dict):
        return isinstance(data, iterable_type) and all(isinstance(x, record_type) for x in data)

    def record_types(self, data):
        types = []

        if is_array_of_pairs(data):
            types = [(x[0], type(x[1])) for x in data]
        elif self.is_reshapable(data, list, dict):
            types = [self.record_types(x) for x in data]
        elif is_hash_of_hashes(data):
            types = {k: self.record_types(v) for k, v in data.items()}
        elif isinstance(data, list):
            types = [type(x) for x in data]
        elif isinstance(data, dict):
            types = {k: type(v) for k, v in data.items()}
        else:
            warnings.warn('Do not know how to find the type(s) of the given record(s).')

        return types

    def deduce_type(self, data, tally=False):
        if isinstance(data, int):
            return Atom(int, 1)
        elif isinstance(data, float):
            return Atom(float, 1)
        elif isinstance(data, str):
            return Atom(str, 1)
        elif isinstance(data, datetime.datetime):
            return Atom(datetime, 1)
        elif isinstance(data, tuple):
            return Pair(self.deduce_type(data[0]), self.deduce_type(data[1]))

        elif isinstance(data, list) and self.has_homogeneous_type(data) and not isinstance(data[0], tuple):
            return Vector(self.deduce_type(data[0]), len(data))
        elif isinstance(data, list):
            t = [self.deduce_type(x) for x in data]
            tBag = Counter([repr(v) for v in t])
            if len(tBag) == 1 and not tally:
                return Vector(t[0], len(data))
            elif tally:
                return Tuple([(k, v) for k, v in sorted(tBag.items(), key=lambda x: x[0])], len(data))
            if len(data) <= self.max_tuple_elems:
                return Tuple(t, 1)
            else:
                return Vector(None, len(data))

        elif is_hash_of_hashes(data):
            kType = self.deduce_type(list(data.keys())[0], tally=tally)
            vType = self.deduce_type(list(data.values())[0], tally=tally)

            if isinstance(vType, Vector):
                return Assoc(key_type=kType, type=vType.type, count=len(data))
            return Assoc(key_type=kType, type=vType, count=len(data))

        elif isinstance(data, dict):
            res = [(k, type(v)) for k, v in data.items()]
            res = sorted(res, key=lambda x: x[0])

            if not self.has_homogeneous_type(list(data.values())) and len(data) <= self.max_struct_elems:
                return Struct(keys=[pair[0] for pair in res], values=[pair[1] for pair in res])
            elif self.has_homogeneous_type(list(data.values())):
                return Assoc(key_type=self.deduce_type(list(data.keys())[0]),
                             type=self.deduce_type(list(data.values())[0]), count=len(data))
            elif tally:
                t = [self.deduce_type(x) for x in data.items()]
                tBag = Counter([repr(v) for v in t])
                return Assoc(key_type='Tally', type=sorted(tBag.items(), key=lambda x: x[0]), count=len(data))
            else:
                return Assoc(
                    key_type=self.deduce_type(list(data.keys()), tally=True),
                    type=self.deduce_type(list(data.values()), tally=True),
                    count=len(data))

        else:
            warnings.warn(f"Do not know how to process the given argument of type {type(data)}.")
            return None
