# DSL translation

## Introduction

This Python package provides the function `dsl_translation` that translated natural language commands
into executable code.

The translations are made via a dedicated Web service.
Here is the corresponding interactive interface: https://antononcube.shinyapps.io/DSL-evaluations .

------

## Usage examples

```python
from DSLTranslation import *

print(dsl_translation("use dfTitanic; group by passengerSex; counts"))

print(dsl_translation("use dfTitanic; group by passengerSex; counts", fmt="json"))

```

**Remark:** By default the generated code is automatically copied to the clipboard.
(Using the Python package ["pyperclip"](https://pypi.org/project/pyperclip/).)

------

## References

### Articles

[AA1] Anton Antonov,
["Introduction to data wrangling with Raku"](https://rakuforprediction.wordpress.com/2021/12/31/introduction-to-data-wrangling-with-raku/),
(2021),
[RakuForPredicion at WordPress](https://rakuforprediction.wordpress.com).

### Packages

[AAp1] Anton Antonov,
[DSL::English::ClassificationWorkflows Raku package](https://github.com/antononcube/Raku-DSL-English-ClassificationWorkflows),
(2020-2022),
[GitHub/antononcube](https://github.com/antononcube).

### Videos

[AAv1] Anton Antonov, 
["Raku for Prediction"](https://conf.raku.org/talk/157), 
(2021), 
[The Raku Conference 2021](https://conf.raku.org/).

[AAv2] Anton Antonov, 
["Doing it like a Cro (Raku data wrangling Shortcuts demo)"](https://youtu.be/wS1lqMDdeIY), 
(2021), 
[YouTube/Anton.Antonov.Antonov](https://www.youtube.com/channel/UC5qMPIsJeztfARXWdIw3Xzw).
