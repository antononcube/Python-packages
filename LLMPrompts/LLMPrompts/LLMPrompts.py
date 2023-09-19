import random
from pathlib import Path
from typing import Optional

import pandas
import xdg
import pkg_resources
import json
import re


# ===========================================================
# Ingest prompt data
# ===========================================================

def ingest_prompt_data():
    # It is expected that resource file "prompts.json" is an array of dictionaries.
    # with open("resources/prompts.json", "r") as f:
    #     records = json.load(f)

    with pkg_resources.resource_stream(__name__, 'resources/prompts.json') as stream:
        records = json.load(stream)

    # Get a list of all unique record fields
    record_fields = set()
    for record in records:
        record_fields.update(record.keys())
    record_fields = sorted(record_fields)

    # Get a list of all unique categories
    categories = set()
    for record in records:
        categories.update(record["Categories"].keys())
    categories = sorted(categories)

    # Get a list of all unique topics
    topics = set()
    for record in records:
        topics.update(record["Topics"].keys())
    topics = sorted(topics)

    # Remove empty categories and topics from each record
    for record in records:
        record["Categories"] = [
            k for (k, v) in record["Categories"].items() if v
        ]
        record["Topics"] = [
            k for (k, v) in record["Topics"].items() if v
        ]

    return {
        "records": records,
        "categories": categories,
        "topics": topics,
    }


aRecordsData = ingest_prompt_data()


# ===========================================================
# Get prompt
# ===========================================================

def _llm_prompt_data_simple(fields=None):
    # Get the prompts database
    prompts = aRecordsData["records"].copy()

    # Make a dictionary
    prompts = {r["Name"]: r for r in prompts}

    # No fields spec
    if fields is None:
        return prompts

    # Handle fields spec
    fieldsLocal = fields

    if isinstance(fieldsLocal, str) and fieldsLocal.lower() in ['any', 'whatever', 'automatic']:
        fieldsLocal = "Description"

    if isinstance(fieldsLocal, str):
        fieldsLocal = [fieldsLocal]

    # Filter the prompts database by fields if specified
    prompts = {k: [v1 for k1, v1 in v.items() if k1 in fieldsLocal] for k, v in prompts.items()}

    # Just one field
    if len(fieldsLocal) == 1:
        prompts = {k: v[0] for k, v in prompts.items()}

    # Result
    return prompts


def _llm_prompt_data_by_name(name, fields='Description'):
    prompts = _llm_prompt_data_simple(fields)
    prompts = {k: v for k, v in prompts.items() if re.match(name, k)}

    return prompts


def llm_prompt_data(name=None, fields=None):
    """Gets the prompts database as a dictionary with the keys being the prompt titles, filtered by name.

    Args:
      name: A regular expression to match the prompt titles.
      fields: A list of fields to include in the returned dictionary. None to include all fields.

    Returns:
      A dictionary of prompts, with the keys being the prompt titles and the values being the prompt data.
    """

    if name is None:
        return _llm_prompt_data_simple(fields=fields)
    return _llm_prompt_data_by_name(name=name, fields=fields)


# ===========================================================
# Get prompt
# ===========================================================

def llm_prompt(name=None, warn=True):
    """Gets the prompt string or pure function for a given prompt name.

    Args:
      name: The name of the prompt.
      warn: Whether to warn if the prompt name is unknown.

    Returns:
      The prompt string or pure function, or None if the prompt name is unknown.
    """

    # Get the prompts database
    prompts = llm_prompt_data()

    # If the prompt name is None, get a random prompt name
    if name is None:
        name = random.choice(list(prompts.keys()))

    # Failed expectations message
    if not isinstance(name, str):
        ValueError("The first argument is expected to be a string or None.")

    # If the prompt name does not exist, warn and return None
    if name not in prompts:
        if warn:
            print(f"Unknown prompt name: '{name}'.")
        return None

    # Get the prompt record
    prompt_record = prompts[name]

    # Get the prompt code
    prompt_code = prompt_record["PromptText"]

    # If the prompt text represents a constant string, return it
    if len(prompt_record["PositionalArguments"]) == 0 and len(prompt_record["NamedArguments"]) == 0:
        return prompt_code

    # Turn Raku code into Python code
    # Drop signature
    prompt_code = re.sub(r'^->.*?\{', '', prompt_code)
    prompt_code = re.sub(r'}$', '', prompt_code)

    # Replace arguments
    for pa in prompt_record["PositionalArguments"]:
        prompt_code = prompt_code.replace(pa, "{" + re.sub(r'^\$', '', pa) + "}")

    for pa in prompt_record["NamedArguments"]:
        prompt_code = prompt_code.replace(pa, "{" + re.sub(r'^\$', '', pa) + "}")

    # Otherwise, return a pure function that takes the positional and named arguments
    # of the prompt and returns the evaluated prompt code
    posArgs = ""
    if len(prompt_record["PositionalArguments"]) > 0:
        for k, v in prompt_record["PositionalArguments"].items():
            if len(posArgs) > 0:
                posArgs = posArgs + ", "

            posArgs = posArgs + re.sub(r'^\$', '', k) + "='" + v + "'"

    namedArgs = ""
    if len(prompt_record["NamedArguments"]) > 0:
        for k, v in prompt_record["NamedArguments"].items():
            if len(namedArgs) > 0:
                namedArgs = namedArgs + ", "

            namedArgs = namedArgs + re.sub(r'^\$', '', k) + "='" + v + "'"

    # Lambda function code
    lambdaCode = "lambda " + posArgs
    if len(namedArgs) > 0:
        if len(posArgs) > 0:
            lambdaCode = lambdaCode + ", "
        lambdaCode = lambdaCode + namedArgs

    lambdaCode = lambdaCode + ': f""' + prompt_code + '""'

    # Make the function
    resFunc = eval(lambdaCode)

    # Result
    return resFunc
