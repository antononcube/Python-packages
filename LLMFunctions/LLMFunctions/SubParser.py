import json
import re
from typing import List, Callable, Union, Dict
import warnings
from json import JSONDecoder


def catch_by_pattern(p, s, converter=None):
    res = []
    if re.search(p, s) is not None:
        for catch in re.finditer(p, s):
            # catch is a match object
            if callable(converter):
                res.append(converter(catch[0]))
            else:
                res.append(catch[0])
    return res


# Taken from https://stackoverflow.com/a/61384796/14163984
def extract_json_objects(text, decoder=JSONDecoder()):
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            yield text[pos:]  # return the remaining text
            break
        yield text[pos:match]  # modification for the non-JSON parts
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1


def jsonify_line(line):
    line_parts = []
    for result in extract_json_objects(line):
        if isinstance(result, dict):  # got a JSON obj
            line_parts.append(result)
        else:  # got text/non-JSON-obj
            line_parts.append(result)
    # (don't make that a list comprehension, quite un-readable)

    return line_parts


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
        if self.spec is None or isinstance(self.spec, str) and self.spec.lower() == 'str':
            return inpt
        elif isinstance(self.spec, str) and self.spec.lower() == 'int':

            p = r'[+|-]?[\d]+'
            return catch_by_pattern(p, inpt, int)

        elif isinstance(self.spec, str) and self.spec.lower() == 'float':

            p = r'[+|-]?[\d]*[.][\d]+'
            return catch_by_pattern(p, inpt, float)

        elif isinstance(self.spec, str) and self.spec.lower() == 'number':

            p = '[+|-]?[\d]+[_.\d]+|[\d]*[.][\d]+|[\d]+'
            return catch_by_pattern(p, inpt, float)

        elif isinstance(self.spec, str) and self.spec.lower() == 'json':

            if exact:
                res = json.loads(inpt)
                # Error handling?
                return res
            else:
                return jsonify_line(inpt)

        elif callable(self.spec):

            return self.spec(inpt)

        else:
            warnings.warn("Do not know what to do with sub-parser spec.")
            return inpt
