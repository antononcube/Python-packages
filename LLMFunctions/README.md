# LLMFunctions

## In brief

This Python package provides functions and function objects to access, interact, and utilize 
Large Language Models (LLMs), like OpenAI, [OAI1], and PaLM, [ZG1].

The structure and implementation of this Python package close follows the design and implementation
of the Raku package "LLM::Functions", [AAp1], supported by "Text::SubParsers", [AAp4].

--------

## Installation

### Install from GitHub

```shell
pip install -e git+https://github.com/antononcube/Python-packages.git#egg=LLMFunctions-antononcube\&subdirectory=LLMFunctions
```

### From PyPi

```shell
pip install LLMFunctions
```

------

## Basic usage examples

Simple text prompt LLM function creation and invocation:

```python
from LLMFunctions import *

fPop = llm_function("What is the population of ")

print(fPop("Niger?"))
```

Parameterized prompt function creation and invocation:

```python
# Pure/lambda function
fPrompt = lambda x1, x2, x3: f'What is the {x1} of {x2} in {x3}?. Give the result as a JSON object with name-value pairs.'

# LLM function creation
fData = llm_function(fPrompt)

# Invocation over concrete parameters
resData = fData("GDP", "top 10 countries", "2020", max_tokens=600)

print(resData)
```

```
The GDP of the top 10 countries in 2020 is as follows:

{
    "United States": 21.44 trillion,
    "China": 14.14 trillion,
    "Japan": 5.15 trillion,
    "Germany": 3.86 trillion,
    "India": 2.94 trillion,
    "United Kingdom": 2.83 trillion,
    "France": 2.71 trillion,
    "Brazil": 2.14 trillion,
    "Italy": 2.04 trillion,
    "Canada": 1.73 trillion
}
```

Creation and invocation of an LLM example function:

```python
# LLM example function creation with a set of few-shot training rules
fEx = llm_example_function({"1,000": "1000",
                            "34,232,900": "34232900",
                            "5.15 trillion": "5.15E12",
                            "32.8 trillion USD": "32.8E12"})

# Invocation over the result above
print(fEx(resData))
```

```
United States: 21.44E12
China: 14.14E12
Japan: 5.15E12
Germany: 3.86E12
India: 2.94E12
United Kingdom: 2.83E12
France: 2.71E12
Brazil: 2.14E12
Italy: 2.07E12
Canada: 1.68E12
```

--------

## References

### Articles

[AA1] Anton Antonov,
["Generating documents via templates and LLMs"](https://rakuforprediction.wordpress.com/2023/07/11/generating-documents-via-templates-and-llms/),
(2023),
[RakuForPrediction at WordPress](https://rakuforprediction.wordpress.com).

[ZG1] Zoubin Ghahramani,
["Introducing PaLM 2"](https://blog.google/technology/ai/google-palm-2-ai-large-language-model/),
(2023),
[Google Official Blog on AI](https://blog.google/technology/ai/).

### Repositories, sites

[OAI1] OpenAI Platform, [OpenAI platform](https://platform.openai.com/).

[WRIr1] Wolfram Research, Inc.
[Wolfram Prompt Repository](https://resources.wolframcloud.com/PromptRepository/).

### Packages, paclets

[AAp1] Anton Antonov,
[LLM::Functions Raku package](https://github.com/antononcube/Raku-LLM-Functions),
(2023),
[GitHub/antononcube](https://github.com/antononcube).

[AAp2] Anton Antonov,
[WWW::OpenAI Raku package](https://github.com/antononcube/Raku-WWW-OpenAI),
(2023),
[GitHub/antononcube](https://github.com/antononcube).

[AAp3] Anton Antonov,
[WWW::PaLM Raku package](https://github.com/antononcube/Raku-WWW-PaLM),
(2023),
[GitHub/antononcube](https://github.com/antononcube).

[AAp4] Anton Antonov,
[Text::SubParsers Raku package](https://github.com/antononcube/Raku-Text-SubParsers),
(2023),
[GitHub/antononcube](https://github.com/antononcube).

[AAp5] Anton Antonov,
[Text::CodeProcessing Raku package](https://github.com/antononcube/Raku-Text-CodeProcessing),
(2021),
[GitHub/antononcube](https://github.com/antononcube).

[AAp6] Anton Antonov,
[ML::FindTextualAnswer Raku package](https://github.com/antononcube/Raku-ML-FindTextualAnswer),
(2023),
[GitHub/antononcube](https://github.com/antononcube).

[AAp7] Anton Antonov,
[ML::NLPTemplateEngine Raku package](https://github.com/antononcube/Raku-ML-NLPTemplateEngine),
(2023),
[GitHub/antononcube](https://github.com/antononcube).

[WRIp1] Wolfram Research, Inc.
[LLMFunctions paclet](https://resources.wolframcloud.com/PacletRepository/resources/Wolfram/LLMFunctions/),
(2023),
[Wolfram Language Paclet Repository](https://resources.wolframcloud.com/PacletRepository/).
