# Trie with frequencies usage examples

Anton Antonov   
[Python-packages at GitHub](https://github.com/antononcube/Python-packages)   
[PythonForPrediction at WordPress](https://pythonforprediction.wordpress.com)   
September 2022   


## Introduction

This notebook has examples of the Machine Learning (ML) data structure 
[Tries with frequencies](https://mathematicaforprediction.wordpress.com/2013/12/06/tries-with-frequencies-for-data-mining/),
[AA1], creation and usage.

For the original Trie (or Prefix tree) data structure see the Wikipedia article 
["Trie"](https://en.wikipedia.org/wiki/Trie).


--------

## Setup

```python
from TriesWithFrequencies import *
```

------

## Creation examples

In this section we show a few ways to create tries with frequencies.

Consider a trie (prefix tree) created over a list of words:

```python
tr = trie_create_by_split( ["bar", "bark", "bars", "balm", "cert", "cell"] )
trie_form(tr)
```

Here we convert the trie with frequencies above into a trie with probabilities:

```python
ptr = trie_node_probabilities( tr )
trie_form(ptr)
```

------

## Shrinking

Here we shrink the trie with probabilities above:

```python
trie_form(trie_shrink(ptr))
```

Here we shrink the frequencies trie using a separator:

```python
trie_form(trie_shrink(tr, sep="~"))
```

-------

## Retrieval and sub-tries

Here we retrieve a sub-trie with a key:

```python
trie_form(trie_sub_trie(tr, list("bar")))
```

------

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

Show the trie form:

```python
trie_form(tr)
```

Classify with the letters of the word "cam":

```python
trie_classify(tr, list("cam"), prop="Probabilities")
```

---------

## References

### Articles

[AA1] Anton Antonov, ["Tries with frequencies for data mining"](https://mathematicaforprediction.wordpress.com/2013/12/06/tries-with-frequencies-for-data-mining/), (2013), [MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

[AA2] Anton Antonov, ["Removal of sub-trees in tries"](https://mathematicaforprediction.wordpress.com/2014/10/12/removal-of-sub-trees-in-tries/), (2013), [MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

[AA3] Anton Antonov, ["Tries with frequencies in Java"](https://mathematicaforprediction.wordpress.com/2017/01/31/tries-with-frequencies-in-java/) (2017), [MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).
[GitHub Markdown](https://github.com/antononcube/MathematicaForPrediction).

[WK1] Wikipedia entry, [Trie](https://en.wikipedia.org/wiki/Trie).


### Packages

[AAp1] Anton Antonov, [Tries with frequencies Mathematica Version 9.0 package](https://github.com/antononcube/MathematicaForPrediction/blob/master/TriesWithFrequenciesV9.m), (2013), [MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp2] Anton Antonov, [Tries with frequencies Mathematica package](https://github.com/antononcube/MathematicaForPrediction/blob/master/TriesWithFrequencies.m), (2013-2018), [MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp3] Anton Antonov, [Tries with frequencies in Java](https://github.com/antononcube/MathematicaForPrediction/tree/master/Java/TriesWithFrequencies), (2017), [MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp4] Anton Antonov, [Java tries with frequencies Mathematica package](https://github.com/antononcube/MathematicaForPrediction/blob/master/JavaTriesWithFrequencies.m), (2017), [MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp5] Anton Antonov, [Java tries with frequencies Mathematica unit tests](https://github.com/antononcube/MathematicaForPrediction/blob/master/UnitTests/JavaTriesWithFrequencies-Unit-Tests.wlt), (2017), [MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp6] Anton Antonov, [ML::TriesWithFrequencies Raku package](https://github.com/antononcube/Raku-ML-TriesWithFrequencies), (2021), [GitHub/antononcube](https://github.com/antononcube).


### Videos

[AAv1] Anton Antonov, ["Prefix Trees with Frequencies for Data Analysis and Machine Learning"](https://www.youtube.com/watch?v=MdVp7t8xQbQ), (2017), Wolfram Technology Conference 2017, [Wolfram channel at YouTube](https://www.youtube.com/channel/UCJekgf6k62CQHdENWf2NgAQ).

<!-- #endregion -->
