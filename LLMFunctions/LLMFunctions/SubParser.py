from typing import List, Callable, Union, Dict
import warnings


class SubParser:
    def __init__(self,
                 spec: Union[str, Callable, None] = None,
                 exact: bool = False):
        self.spec = spec
        self.exact = exact

    def process(self, inpt):
        if self.exact:
            return self.parse(inpt, True)
        else:
            return self.sub_parse(inpt)

    def sub_parse(self, inpt):
        return self.parse(inpt, False)

    def parse(self, inpt: str, exact: bool = True):
        if self.spec is None or self.isinstance(spec, str) and self.spec == 'str':
            return inpt
        elif callable(self.spec):
            return self.spec(inpt)
        else:
            warnings.warn("Do not know what to do with sub-parser spec.")
            return inpt
