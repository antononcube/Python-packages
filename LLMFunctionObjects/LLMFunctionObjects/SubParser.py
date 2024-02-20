import json
import re
from typing import List, Callable, Union, Dict
import warnings
from json import JSONDecoder


def catch_by_pattern(p, s, converter=None, drop: bool = False):
    res = []
    if re.search(p, s) is not None:
        for catch in re.finditer(p, s):
            # catch is a match object
            if callable(converter):
                res.append(converter(catch[0]))
            elif not drop:
                res.append(catch[0])
    return res


def numify_text(p, text, converter=None, drop: bool = False):
    res = []
    repl_str = re.compile(r'^\d+$')
    # t = r'\d+.?\d*'
    line = text.split()
    for word in line:
        word = re.sub(r'(\d),(\d)', r'\1\2', word, count=0)
        match = re.search(repl_str, word)
        if match:
            res.append(converter(match.group()))
        elif not drop:
            res.append(word)

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


def from_json(text):
    res = text.replace("```json", "").replace("```", "").strip()
    return json.loads(res)


def jsonify_text(text, drop: bool = False):
    line_parts = []
    textLocal = text
    if drop:
        textLocal = re.sub(r"^```json|```$", "", textLocal)
    for result in extract_json_objects(textLocal):
        if isinstance(result, dict):  # got a JSON obj
            line_parts.append(result)
        elif not drop:  # got text/non-JSON-obj
            line_parts.append(result)
    if len(line_parts) == 0:
        return json.loads(textLocal)
    # (don't make that a list comprehension, quite un-readable)
    return line_parts


def sub_parser(spec, drop=False):
    return SubParser(spec, exact=False, drop=drop)


def exact_parser(spec, drop=False):
    return SubParser(spec, exact=True, drop=drop)


class SubParser:
    def __init__(self,
                 spec: Union[str, Callable, None] = None,
                 exact: bool = False,
                 drop: bool = False):
        self.spec = spec
        self.exact = exact
        self.drop = drop

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
            return numify_text(p=p, text=inpt, converter=int, drop=self.drop)

        elif isinstance(self.spec, str) and self.spec.lower() == 'float':

            p = r'[+|-]?[\d]*[.]\d+'
            return numify_text(p=p, text=inpt, converter=float)

        elif isinstance(self.spec, str) and self.spec.lower() == 'number':

            p = r'[+|-]?[\d]+[_.\d]+|[\d]*[.][\d]+|[\d]+'
            return numify_text(p=p, text=inpt, converter=float, drop=self.drop)

        elif isinstance(self.spec, str) and self.spec.lower() == 'json':

            if exact:
                res = json.loads(inpt)
                # Error handling?
                return res
            else:
                return jsonify_text(text=inpt, drop=self.drop)

        elif callable(self.spec):

            return self.spec(inpt)

        else:
            warnings.warn("Do not know what to do with sub-parser spec.")
            return inpt
