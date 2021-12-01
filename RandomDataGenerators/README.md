# Random Data Generators Python package

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

    ## ['3749', '4572', '9812', '7395', '2388', '7625']

    random_string(6, chars=4, pattern = "[\l]") # letters only

    ## ['FhSd', 'DNSu', 'YggC', 'ajqA', 'dIBt', 'Mjdc']

    random_string(6, chars=4, pattern = "[\l\d]") # both digits and letters

    ## ['yp4u', '2Shk', 'pvpS', 'M43O', 'm5SX', 'It3L']

------------------------------------------------------------------------

## Random words

The function `random_word` generates random words.

Here we generate a list with 12 random words:

    random_word(12)

    ## ['arteria', 'Sauria', 'mentation', 'elope', 'expositor', 'planetarium', 'agglutinin', 'Faunus', 'flab', 'slub', 'Chasidic', 'Jirrbal']

Here we generate a table of random words of different types (kinds):

    dfWords = pandas.DataFrame({k: random_word(6, kind = k) for k in ["Any", "Common", "Known", "Stop"]})
    print(dfWords.transpose().to_string())

    ##                0              1          2                 3            4              5
    ## Any     stuffing  mind-altering    angrily        Embothrium       sorbet        smoking
    ## Common    reason       mackerel  alignment        calculator     halfback      paranoiac
    ## Known     tannoy    double-date    deckled  gynandromorphous  gravitative  steganography
    ## Stop       about              N      noone              next         back          alone

**Remark:** `None` can be used instead of `'Any'`.

------------------------------------------------------------------------

## Random pet names

The function `random_pet_name` generates random pet names.

The pet names are taken from publicly available data of pet license
registrations in the years 2015–2020 in Seattle, WA, USA. See \[DG1\].

The following command generates a list of six random pet names:

    random.seed(32)
    random_pet_name(6)

    ## ['Oskar', 'Bilbo "Bobo" Waggins', 'Maximus', 'Gracie', 'Osa', 'Fabio']

The named argument `species` can be used to specify specie of the random
pet names. (According to the specie-name relationships in \[DG1\].)

Here we generate a table of random pet names of different species:

    dfPetNames = pandas.DataFrame({ wt: random_pet_name(6, species = wt) for wt in ["Any", "Cat", "Dog", "Goat", "Pig"] })
    dfPetNames.transpose()

    ##             0                1         2        3          4         5
    ## Any     Lumen             Asha      Echo     Yuki    Francis   Charlie
    ## Cat     Ellie      Roxie Grace    Norman     Bean  Mr. Darcy  Hermione
    ## Dog   Brewski            Matzo      Joey    K. C.      Oscar    Gracie
    ## Goat     Lula  Brussels Sprout     Grace   Moppet     Frosty      Arya
    ## Pig    Millie         Guinness  Guinness  Atticus   Guinness    Millie

**Remark:** `None` can be used instead of `'Any'`.

The named argument `weighted` can be used to specify random pet name
choice based on known real-life number of occurrences:

    random.seed(32);
    random_pet_name(6, weighted=True)

    ## ['Zorro', 'Beeker', 'Lucy', 'Blanco', 'Winston', 'Petunia']

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

    ##          Meryl   Oreo  Douglas Fur Sprockett
    ## id.0 -1.053990  QhFlT            0     o7p5f
    ## id.1 -0.707621  G90kh            0     yBupF
    ## id.2  0.494162  eMVtF            0     Ez2Df
    ## id.3  0.400718  tx3HL            2     3Tz7I
    ## id.4 -1.345948  r3NRa            0     whfam

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

    ##       alpha      beta  gamma  zetta             omega
    ## 0    Frayda  0.811681      4  1V05P             swing
    ## 1     Rosie  0.591327      3  tg7yn           Carolus
    ## 2      Jovi  0.563906      7  imaDl            sailor
    ## 3     Pilot  0.607250      7  WAg8u           echinus
    ## 4    Brodie  0.279003     12  yXEao          Ramayana
    ## 5  Springer -1.394703      5  JFBoz            simper
    ## 6       Uma -0.538088      8  7ATV1        consecrate
    ## 7      Diva  0.343234      4  GeJUh            blight
    ## 8    Fezzik  1.506241      6  yEPI5  misappropriation
    ## 9      Hana -1.359908      4  PG3IS          diploidy

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
