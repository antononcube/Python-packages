"""Command-line interface for LLMPrompts."""

import re
import sys

from LLMPrompts.LLMPrompts import llm_prompt
from LLMPrompts.LLMPrompts import llm_prompt_data


def _parse_named_token(token, next_token=None):
    body = token[2:]

    if "=" in body:
        key, value = body.split("=", 1)
        return key.replace("-", "_"), value, False

    if next_token is not None and not next_token.startswith("--"):
        return body.replace("-", "_"), next_token, True

    return body.replace("-", "_"), True, False


def _parse_cli_tokens(tokens):
    name = None
    positional = []
    named = {}

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.startswith("--") and len(token) > 2:
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            key, value, consumed_next = _parse_named_token(token, next_token=next_token)
            named[key] = value
            if consumed_next:
                i += 1
        elif name is None:
            name = token
        else:
            positional.append(token)

        i += 1

    return name, positional, named


def _to_bool(value):
    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", ""}:
        return False

    print('bool(text) : ' + bool(text))
    return False


def _to_fields(value):
    if value is None:
        return None

    return [part.strip() for part in re.split(r"[,\s]+", str(value)) if part.strip()]


def _is_regex_spec(text):
    return isinstance(text, str) and text.startswith("rx/") and text.endswith("/")


def _compile_regex_spec(text):
    pattern = text[3:-1]
    try:
        return re.compile(pattern)
    except re.error as exc:
        raise ValueError("The first argument is expected to be a string or a valid regex code.") from exc


def main(argv=None):
    tokens = list(sys.argv[1:] if argv is None else argv)
    name, positional, named = _parse_cli_tokens(tokens)

    if name is None:
        print("Usage: llm_prompt <name|rx/.../> [args] [--key value|--key=value]", file=sys.stderr)
        return 2

    _pairs = False
    if _is_regex_spec(name):
        try:
            rx_name = _compile_regex_spec(name)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

        fields = _to_fields(named["fields"]) if "fields" in named else None
        pairs = _to_bool(named["pairs"]) if "pairs" in named else False
        result = llm_prompt_data(rx_name, fields=fields, pairs=pairs)
    else:
        result = llm_prompt(name)

    if callable(result):
        try:
            result = result(*positional, **named)
        except TypeError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(result)
        return 0

    if isinstance(result, dict):
        for key in sorted(result.keys()):
            print(f"{key} => {result[key]}")
        return 0

    if result is not None:
        print(result)
        return 0

    llm_prompt_data().keys()
    print("To get all known prompt names use regex specification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
