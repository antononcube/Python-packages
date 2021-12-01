## Introduction

This Python package has functions for generating random strings, words,
pet names, and (tabular) data frames.

### Motivation

The primary motivation for this package is to have simple, intuitively
named functions for generating random vectors (lists) and data frames of
different objects.

Although, Python has support of random vector generation, it is assumed
that commands like the following are easier to use:

    random_string(6, chars = 4, pattern = "[\l\d]")

------------------------------------------------------------------------

## Installation

To install from GitHub use the shell command:

    python -m pip install git+https://github.com/antononcube/Python-packages.git#egg=RandomDataGenerators\&subdirectory=RandomDataGenerators

To install from [PyPi.org](https://pypi.org):

    python -m pip install RandomDataGenerators

------------------------------------------------------------------------

## Setup

    from RandomDataGenerators import *

The import command above is equivalent to the import commands:

    from RandomDataGenerators.RandomDataFrameGenerator import random_data_frame
    from RandomDataGenerators.RandomFunctions import random_string
    from RandomDataGenerators.RandomFunctions import random_word
    from RandomDataGenerators.RandomFunctions import random_pet_name
    from RandomDataGenerators.RandomFunctions import random_pretentious_job_title

We are also going to use the packages `random`, `numpy`, and `pandas`:

    import random
    import numpy
    import pandas
    pandas.set_option('display.max_columns', None)

------------------------------------------------------------------------

## Random strings

The function `random_string` generates random strings. (It is based on
the package
[`StringGenerator`](https://pypi.org/project/StringGenerator/),
\[PW1\].)

Here we generate a vector of random strings with length 4 and characters
that belong to specified ranges:

    random_string(6, chars=4, pattern = "[\d]") # digits only

    ## ['2576', '7266', '8755', '2603', '5398', '4338']

    random_string(6, chars=4, pattern = "[\l]") # letters only

    ## ['JpUD', 'JdwF', 'tBRw', 'gHSE', 'GDtw', 'dFUu']

    random_string(6, chars=4, pattern = "[\l\d]") # both digits and letters

    ## ['3T4W', 'R128', 'SfrA', 'FEJQ', 'qUBU', 'o5Ni']

------------------------------------------------------------------------

## Random words

The function `random_word` generates random words.

Here we generate a list with 12 random words:

    random_word(12)

    ## ['decolorise', 'mailboat', 'decameter', 'conceit', 'Carnosaura', 'frenetically', 'antidiabetic', 'dogmatic', 'hurdler', 'Batrachoididae', 'pastorship', 'apneic']

Here we generate a table of random words of different types (kinds):

    dfWords = pandas.DataFrame({k: random_word(6, kind = k) for k in ["Any", "Common", "Known", "Stop"]})
    print(dfWords.transpose().to_string())

    ##                      0           1            2          3            4           5
    ## Any            squared  pinnatifid       Exocet  Signorina  heartlessly     Yisrael
    ## Common  microbiologist       recap  masterpiece        nee    protector    essayist
    ## Known    gubernatorial    savannah     skywards     sundry      heckler  cellulosic
    ## Stop                 g        give         into          W        would       why's

**Remark:** `None` can be used instead of `'Any'`.

------------------------------------------------------------------------

## Random pet names

The function `random_pet_name` generates random pet names.

The pet names are taken from publicly available data of pet license
registrations in the years 2015–2020 in Seattle, WA, USA. See \[DG1\].

The following command generates a list of six random pet names:

    random.seed(32)
    random_pet_name(6)

    ## ['Summa', 'Loki', 'Winnie', 'Sirius', 'Daisy', 'Edith']

The named argument `species` can be used to specify specie of the random
pet names. (According to the specie-name relationships in \[DG1\].)

Here we generate a table of random pet names of different species:

    dfPetNames = pandas.DataFrame({ wt: random_pet_name(6, species = wt) for wt in ["Any", "Cat", "Dog", "Goat", "Pig"] })
    dfPetNames.transpose()

    ##             0        1       2         3        4        5
    ## Any    Muffin    Raina     Ned    Poloma     Kona    Forte
    ## Cat    BooBoo  Ophelia    Lucy      Roux    Mante     Jack
    ## Dog     Agnes     Luke   Lucca    Phoebe   Beacon     Aida
    ## Goat    Teddy    Piper    Tati     Aggie  Estelle  Phyllis
    ## Pig   Atticus   Millie  Millie  Guinness   Millie  Atticus

**Remark:** `None` can be used instead of `'Any'`.

The named argument `weighted` can be used to specify random pet name
choice based on known real-life number of occurrences:

    random.seed(32);
    random_pet_name(6, weighted=True)

    ## ['Isabella', 'Fire', 'Kava', 'Angus', 'Angelica', 'LEO']

The weights used correspond to the counts from \[DG1\].

**Remark:** The implementation of `random-pet-name` is based on the
Mathematica implementation
[`RandomPetName`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomPetName),
\[AAf1\].

------------------------------------------------------------------------

## Random pretentious job titles

The function `random_pretentious_job_title` generates random pretentious
job titles.

The following command generates a list of six random pretentious job
titles:

    random_pretentious_job_title(6)

    ## ['Direct Identity Officer', 'District Group Synergist', 'Lead Brand Liason', 'Central Configuration Administrator', 'Senior Accountability Facilitator', 'Dynamic Web Producer']

The named argument `number_of_words` can be used to control the number
of words in the generated job titles.

The named argument `language` can be used to control in which language
the generated job titles are in. At this point, only Bulgarian and
English are supported.

Here we generate pretentious job titles using different languages and
number of words per title:

    random.seed(2)
    random_pretentious_job_title(12, number_of_words = None, language = None)

    ## ['Manager', 'Клиентов Асистент на Инфраструктурата', 'Customer Quality Strategist', 'Наследствен Анализатор по Идентичност', 'Administrator', 'Изпълнител на Фактори', 'Administrator', 'Architect', 'Investor Assurance Agent', 'Прогресивен Служител по Сигурност', 'Координатор', 'Анализатор по Оптимизация']

**Remark:** `None` can be used as values for the named arguments
`number_of_words` and `language`.

**Remark:** The implementation uses the job title phrases in
<https://www.bullshitjob.com> . It is, more-or-less, based on the
Mathematica implementation
[`RandomPretentiousJobTitle`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomPretentiousJobTitle),
\[AAf2\].

------------------------------------------------------------------------

## Random tabular datasets

The function `random_data_frame` can be used generate tabular *data
frames*.

**Remark:** In this package a *data frame* is an object produced and
manipulated by the package `pandas`.

Here are basic calls:

    random_data_frame()
    random_data_frame(None, row_names=True)
    random_data_frame(None, None)
    random_data_frame(12, 4)
    random_data_frame(None, 4)
    random_data_frame(5, None, column_names_generator = random_pet_name)
    random_data_frame(15, 5, generators = [random_pet_name, random_string, random_pretentious_job_title])
    random_data_frame(None, ["Col1", "Col2", "Col3"], row-names=False)

Here is example of a generated data frame with column names that are cat
pet names:

    random_data_frame(5, 4, column_names_generator = lambda size: random_pet_name(size, species = 'Cat'), row_names=True)

    ##       Girl Dave   Luna  Mango   Miso
    ## id.0  -1.119327  mg0nJ      0  FdJ1f
    ## id.1   2.281908  1rKBx      0  0wwRB
    ## id.2  -0.414357  7jaLx      1  AdVGy
    ## id.3  -0.375464  b6awf      0  lMtJi
    ## id.4   0.600464  iDTGN      0  d8bLa

**Remark:** Both [*wide format* and *long
format*](https://en.wikipedia.org/wiki/Wide_and_narrow_data) data frames
can be generated.

**Remark:** The signature design and implementation are based on the
Mathematica implementation
[`RandomTabularDataset`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomTabularDataset),
\[AAf3\]. There are also corresponding packages written in R, \[AAp1\],
and Raku, \[AAp2\].

Here is an example in which some of the columns have specified
generators:

    random.seed(66)
    random_data_frame(10, 
                      ["alpha", "beta", "gamma", "zetta", "omega"], 
                      generators = {"alpha" : random_pet_name, 
                                    "beta" :  numpy.random.normal, 
                                    "gamma" : lambda size: numpy.random.poisson(lam=5, size=size) } )

    ##                     alpha      beta  gamma  zetta             omega
    ## 0                  Baxter -0.222219      4  03SRn             swing
    ## 1                 Grayson -0.059046      4  mSMyh           Carolus
    ## 2  Sebastian Etris-Scully  0.883341      2  7HzMZ            sailor
    ## 3                  Winnie  0.702750      8  dKdE9           echinus
    ## 4                   Samba -0.533832      6  nrihK          Ramayana
    ## 5                   Bella  0.556321      9  z2QBn            simper
    ## 6               Luna Tuna -0.084652      5  JcXyk        consecrate
    ## 7                  Wasabi -0.558906      6  psF3B            blight
    ## 8                   Grace  0.626227      8  gztEk  misappropriation
    ## 9                   Rocky  0.343531      6  wO1AO          diploidy

------------------------------------------------------------------------

## References

### Articles

\[AA1\] Anton Antonov, [“Pets licensing data
analysis”](https://mathematicaforprediction.wordpress.com/2020/01/20/pets-licensing-data-analysis/),
(2020), [MathematicaForPrediction at
WordPress](https://mathematicaforprediction.wordpress.com).

### Functions, packages

\[AAf1\] Anton Antonov,
[RandomPetName](https://resources.wolframcloud.com/FunctionRepository/resources/RandomPetName),
(2021), [Wolfram Function
Repository](https://resources.wolframcloud.com/FunctionRepository).

\[AAf2\] Anton Antonov,
[RandomPretentiousJobTitle](https://resources.wolframcloud.com/FunctionRepository/resources/RandomPretentiousJobTitle),
(2021), [Wolfram Function
Repository](https://resources.wolframcloud.com/FunctionRepository).

\[AAf3\] Anton Antonov,
[RandomTabularDataset](https://resources.wolframcloud.com/FunctionRepository/resources/RandomTabularDataset),
(2021), [Wolfram Function
Repository](https://resources.wolframcloud.com/FunctionRepository).

\[AAp1\] Anton Antonov, [RandomDataFrameGenerator R
package](https://github.com/antononcube/R-packages/tree/master/RandomDataFrameGenerator),
(2020), [R-packages at
GitHub/antononcube](https://github.com/antononcube/R-packages).

\[AAp2\] Anton Antonov, [Data::Generators Raku
package](https://modules.raku.org/dist/Data::Generators:cpan:ANTONOV),
(2021), [Raku Modules](https://modules.raku.org).

\[PW1\] Paul Wolf, [StringGenerator Python
package](https://pypi.org/project/StringGenerator),
(PyPi.org)(<https://pypi.org>).

\[WRI1\] Wolfram Research (2010),
[RandomVariate](https://reference.wolfram.com/language/ref/RandomVariate.html),
Wolfram Language function.

### Data repositories

\[DG1\] Data.Gov, [Seattle Pet
Licenses](https://catalog.data.gov/dataset/seattle-pet-licenses),
[catalog.data.gov](https://catalog.data.gov).
