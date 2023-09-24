from typing import Any, List, Union


class Type:
    type = None
    count: int = 0

    def __init__(self, type=None, count: int = 1):
        self.type = type
        self.count = count

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        raise repr(self)


class Atom(Type):
    def __repr__(self) -> str:
        return f'Atom({self.type})'


class Pair(Type):
    def __init__(self, key_type=None, type=None):
        super().__init__(type)
        self.key_type = key_type

    def __repr__(self) -> str:
        return f'Pair({self.key_type}, {self.type})'


class Vector(Type):
    def __repr__(self) -> str:
        if isinstance(self.type, list):
            if len(self.type) == 1:
                return f'Vector({", ".join(map(str, self.type))}, {self.count})'
            else:
                return f'Vector([{", ".join(map(str, self.type))}], {self.count})'
        else:
            return f'Vector({str(self.type)}, {self.count})'



class Tuple(Type):
    def __repr__(self) -> str:
        if self.count == 1:
            return f'Tuple([{", ".join(map(str, self.type))}])'
        else:
            return f'Tuple([{", ".join(map(str, self.type))}], {self.count})'


class Assoc(Type):
    def __init__(self, key_type=None, type=None, count: int = 1):
        super().__init__(type, count)
        self.key_type = key_type

    def __repr__(self) -> str:
        if self.key_type == 'Tally':
            return f'Assoc([{", ".join(map(str, self.type))}], {self.count})'
        else:
            return f'Assoc({self.key_type}, {self.type}, {self.count})'


class Struct(Type):
    def __init__(self, keys: List[Type], values: List[Type]):
        super().__init__()
        self.keys = keys
        self.values = values

    def __repr__(self) -> str:
        return f'Struct([{", ".join(map(str, self.keys))}], [{", ".join(map(lambda v: str(v.__name__), self.values))}])'
