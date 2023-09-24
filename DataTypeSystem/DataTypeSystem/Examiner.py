from collections import Counter

from DataTypeSystem.TypeClasses import Type, Atom, Pair, Vector, Tuple, Assoc, Struct
import datetime


class Examiner:

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

        if isinstance(data, list) and self.has_homogeneous_type(data) and not isinstance(data[0], tuple):
            types = [self.record_types(x) for x in data[0]]
        elif isinstance(data, list):
            types = [self.record_types(x) for x in data]
        elif isinstance(data, dict):
            types = {k: self.record_types(v) for k, v in data.items()}
        else:
            print('Do not know how to find the type(s) of the given record(s).')

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

        elif isinstance(data, dict):
            kType = self.deduce_type(list(data.keys())[0], tally=tally)
            vType = self.deduce_type(list(data.values())[0], tally=tally)

            if isinstance(vType, Vector):
                return Assoc(key_type=kType, type=vType.type, count=len(data))
            return Assoc(key_type=kType, type=vType, count=len(data))

        else:
            return None
