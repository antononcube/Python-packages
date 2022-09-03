# Tries with frequencies

This Python package has functions for creation and manipulation of 
[Tries (Prefix trees)](https://en.wikipedia.org/wiki/Trie) 
with frequencies.

The package provides Machine Learning (ML) functionalities, not "just" a 
[Trie]((https://en.wikipedia.org/wiki/Trie)) 
data structure.

This Python implementation closely follows the Mathematica implementation [AAp2].

--------

## Installation

### From GitHub:

```shell
pip install -e git+https://github.com/antononcube/Python-packages.git#egg=TriesWithFrequencies-antononcube\&subdirectory=TriesWithFrequencies
```

### From PyPI:

```shell
python3 -m pip install TriesWithFrequencies
```

------------------------------------------------------------------------

## Setup

```python
from TriesWithFrequencies import *
```

------------------------------------------------------------------------

## Creation examples

In this section we show a few ways to create tries with frequencies.

Consider a trie (prefix tree) created over a list of words:

```python
tr = trie_create_by_split( ["bar", "bark", "bars", "balm", "cert", "cell"] )
trie_form(tr)
```


    TRIEROOT => 6.0
    ├─b => 4.0
    │ └─a => 4.0
    │   ├─r => 3.0
    │   │ └─k => 1.0
    │   │ └─s => 1.0
    │   └─l => 1.0
    │     └─m => 1.0
    └─c => 2.0
      └─e => 2.0
        ├─r => 1.0
        │ └─t => 1.0
        └─l => 1.0
          └─l => 1.0


Here we convert the trie with frequencies above into a trie with
probabilities:


```python
ptr = trie_node_probabilities( tr )
trie_form(ptr)
```


    TRIEROOT => 1.0
    ├─b => 0.6666666666666666
    │ └─a => 1.0
    │   ├─r => 0.75
    │   │ ├─k => 0.3333333333333333
    │   │ └─s => 0.3333333333333333
    │   └─l => 0.25
    │     └─m => 1.0
    └─c => 0.3333333333333333
      └─e => 1.0
        ├─r => 0.5
        │ └─t => 1.0
        └─l => 0.5
          └─l => 1.0


------------------------------------------------------------------------

## Shrinking

Here we shrink the trie with probabilities above:

```python
trie_form(trie_shrink(ptr))
```


    TRIEROOT => 1.0
    └─ba => 1.0
      └─r => 0.75
        └─k => 0.3333333333333333
        └─s => 0.3333333333333333
      └─lm => 1.0
    └─ce => 1.0
      └─rt => 1.0
      └─ll => 1.0


Here we shrink the frequencies trie using a separator:


```python
trie_form(trie_shrink(tr, sep="~"))
```


    TRIEROOT => 6.0
    └─b~a => 4.0
      └─r => 3.0
        └─k => 1.0
        └─s => 1.0
      └─l~m => 1.0
    └─c~e => 2.0
      └─r~t => 1.0
      └─l~l => 1.0


------------------------------------------------------------------------

## Retrieval and sub-tries

Here we retrieve a sub-trie with a key:

```python
trie_form(trie_sub_trie(tr, list("bar")))
```


    r => 3.0
    └─k => 1.0
    └─s => 1.0


------------------------------------------------------------------------

## Classification

Create a trie:

```python
words = [*(["bar"] * 6), *(["bark"] * 3), *(["bare"] * 2), *(["cam"] * 3), "came", *(["camelia"] * 4)]
tr = trie_create_by_split(words)
tr = trie_node_probabilities(tr)
```
Show node counts:

```python
trie_node_counts(tr)
```

    {'total': 13, 'internal': 10, 'leaves': 3}


Show the trie form:

```python
trie_form(tr)
```


    TRIEROOT => 1.0
    ├─b => 0.5789473684210527
    │ └─a => 1.0
    │   └─r => 1.0
    │     ├─k => 0.2727272727272727
    │     └─e => 0.18181818181818182
    └─c => 0.42105263157894735
      └─a => 1.0
        └─m => 1.0
          └─e => 0.625
            └─l => 0.8
              └─i => 1.0
                └─a => 1.0

Classify with the letters of the word \"cam\":

```python
trie_classify(tr, list("cam"), prop="Probabilities")
```

    {'a': 0.5, 'm': 0.375, 'e': 0.12499999999999997}



------

## References

### Articles

[AA1] Anton Antonov,
["Tries with frequencies for data mining"](https://mathematicaforprediction.wordpress.com/2013/12/06/tries-with-frequencies-for-data-mining/),
(2013),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

[AA2] Anton Antonov,
["Removal of sub-trees in tries"](https://mathematicaforprediction.wordpress.com/2014/10/12/removal-of-sub-trees-in-tries/),
(2013),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

[AA3] Anton Antonov,
["Tries with frequencies in Java"](https://mathematicaforprediction.wordpress.com/2017/01/31/tries-with-frequencies-in-java/)
(2017),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).
[GitHub Markdown](https://github.com/antononcube/MathematicaForPrediction).

[RAC1] Tib,
["Day 10: My 10 commandments for Raku performances"](https://raku-advent.blog/2020/12/10/day-10-my-10-commandments-for-raku-performances/),
(2020),
[Raku Advent Calendar](https://raku-advent.blog).

[WK1] Wikipedia entry, [Trie](https://en.wikipedia.org/wiki/Trie).

### Packages

[AAp1] Anton Antonov, 
[Tries with frequencies Mathematica Version 9.0 package](https://github.com/antononcube/MathematicaForPrediction/blob/master/TriesWithFrequenciesV9.m),
(2013), 
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp2] Anton Antonov,
[Tries with frequencies Mathematica package](https://github.com/antononcube/MathematicaForPrediction/blob/master/TriesWithFrequencies.m),
(2013-2018),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp3] Anton Antonov, 
[Tries with frequencies in Java](https://github.com/antononcube/MathematicaForPrediction/tree/master/Java/TriesWithFrequencies), 
(2017),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp4] Anton Antonov, 
[Java tries with frequencies Mathematica package](https://github.com/antononcube/MathematicaForPrediction/blob/master/JavaTriesWithFrequencies.m), 
(2017),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp5] Anton Antonov, 
[Java tries with frequencies Mathematica unit tests](https://github.com/antononcube/MathematicaForPrediction/blob/master/UnitTests/JavaTriesWithFrequencies-Unit-Tests.wlt), 
(2017), 
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp6] Anton Antonov,
[ML::TriesWithFrequencies Raku package](https://github.com/antononcube/Raku-ML-TriesWithFrequencies),
(2021),
[GitHub/antononcube](https://github.com/antononcube).


### Videos

[AAv1] Anton Antonov,
["Prefix Trees with Frequencies for Data Analysis and Machine Learning"](https://www.youtube.com/watch?v=MdVp7t8xQbQ),
(2017),
Wolfram Technology Conference 2017,
[Wolfram channel at YouTube](https://www.youtube.com/channel/UCJekgf6k62CQHdENWf2NgAQ).
