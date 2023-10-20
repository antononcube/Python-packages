# Latent Semantic Analysis (LSA) Python package 

## In brief

This Python package, `LatentSemanticAnalyzer`, has different functions for computations of 
Latent Semantic Analysis (LSA) workflows
(using Sparse matrix Linear Algebra.) The package mirrors
the Mathematica implementation [AAp1]. 
(There is also a corresponding implementation in R; see [AAp2].) 

The package provides: 
- Class `LatentSemanticAnalyzer`
- Functions for applying Latent Semantic Indexing (LSI) functions on matrix entries
- "Data loader" function for obtaining a `pandas` data frame ~580 abstracts of conference presentations

------

## Installation

To install from GitHub use the shell command:

```shell
python -m pip install git+https://github.com/antononcube/Python-packages.git#egg=LatentSemanticAnalyzer\&subdirectory=LatentSemanticAnalyzer
```

To install from PyPI:

```shell
python -m pip install LatentSemanticAnalyzer
```

----- 

## LSA workflows

The scope of the package is to facilitate the creation and execution of the workflows encompassed in this
flow chart:

![LSA-workflows](https://raw.githubusercontent.com/antononcube/MathematicaForPrediction/master/MarkdownDocuments/Diagrams/A-monad-for-Latent-Semantic-Analysis-workflows/LSA-workflows.jpg)

For more details see the article 
["A monad for Latent Semantic Analysis workflows"](https://mathematicaforprediction.wordpress.com/2019/09/13/a-monad-for-latent-semantic-analysis-workflows/),
[AA1].

------

## Usage example

Here is an example of a LSA pipeline that:
1. Ingests a collection of texts
2. Makes the corresponding document-term matrix using stemming and removing stop words
3. Extracts 40 topics
4. Shows a table with the extracted topics
5. Shows a table with statistical thesaurus entries for selected words  

```
import random
from LatentSemanticAnalyzer.LatentSemanticAnalyzer import *
from LatentSemanticAnalyzer.DataLoaders import *
import snowballstemmer

# Collection of texts
dfAbstracts = load_abstracts_data_frame()
docs = dict(zip(dfAbstracts.ID, dfAbstracts.Abstract))
print(len(docs))

# Remove non-strings
docs2 = { k:v for k, v in docs.items() if isinstance(v, str) }
print(len(docs2))

# Stemmer object (to preprocess words in the pipeline below)
stemmerObj = snowballstemmer.stemmer("english")

# Words to show statistical thesaurus entries for
words = ["notebook", "computational", "function", "neural", "talk", "programming"]

# Reproducible results
random.seed(12)

# LSA pipeline
lsaObj = (LatentSemanticAnalyzer()
          .make_document_term_matrix(docs=docs2,
                                     stop_words=True,
                                     stemming_rules=True,
                                     min_length=3)
          .apply_term_weight_functions(global_weight_func="IDF",
                                       local_weight_func="None",
                                       normalizer_func="Cosine")
          .extract_topics(number_of_topics=40, min_number_of_documents_per_term=10, method="NNMF")
          .echo_topics_interpretation(number_of_terms=12, wide_form=True)
          .echo_statistical_thesaurus(terms=stemmerObj.stemWords(words),
                                      wide_form=True,
                                      number_of_nearest_neighbors=12,
                                      method="cosine",
                                      echo_function=lambda x: print(x.to_string())))
```

------

## Related Python packages

This package is based on the Python package 
["SSparseMatrix"](https://pypi.org/project/SSparseMatrix/), [AAp3]

The package 
["SparseMatrixRecommender"](https://pypi.org/project/SparseMatrixRecommender/)
also uses LSI functions -- this package uses LSI methods of the class `SparseMatrixRecommender`.

------

## Related Mathematica and R packages

### Mathematica

The Python pipeline above corresponds to the following pipeline for the Mathematica package
[AAp1]:

```mathematica
lsaObj =
  LSAMonUnit[aAbstracts]⟹
   LSAMonMakeDocumentTermMatrix["StemmingRules" -> Automatic, "StopWords" -> Automatic]⟹
   LSAMonEchoDocumentTermMatrixStatistics["LogBase" -> 10]⟹
   LSAMonApplyTermWeightFunctions["IDF", "None", "Cosine"]⟹
   LSAMonExtractTopics["NumberOfTopics" -> 20, Method -> "NNMF", "MaxSteps" -> 16, "MinNumberOfDocumentsPerTerm" -> 20]⟹
   LSAMonEchoTopicsTable["NumberOfTerms" -> 10]⟹
   LSAMonEchoStatisticalThesaurus["Words" -> Map[WordData[#, "PorterStem"]&, {"notebook", "computational", "function", "neural", "talk", "programming"}]];
```

### R 

The package 
[`LSAMon-R`](https://github.com/antononcube/R-packages/tree/master/LSAMon-R), 
[AAp2], implements a software monad for LSA workflows. 

------

## LSA packages comparison project

The project "Random mandalas deconstruction with R, Python, and Mathematica", [AAr1, AA2],
has documents, diagrams, and (code) notebooks for comparison of LSA application to a collection of images
(in multiple programming languages.)

A big part of the motivation to make the Python package 
["RandomMandala"](https://pypi.org/project/RandomMandala), [AAp6], 
was to make easier the LSA package comparison. 
Mathematica and R have fairly streamlined connections to Python, hence it is easier
to propagate (image) data generated in Python into those systems. 

------

## Code generation with natural language commands

### Using grammar-based interpreters

The project "Raku for Prediction", [AAr2, AAv2, AAp7], has a Domain Specific Language (DSL) grammar and interpreters 
that allow the generation of LSA code for corresponding Mathematica, Python, R packages. 

Here is Command Line Interface (CLI) invocation example that generate code for this package:

```shell
> ToLatentSemanticAnalysisWorkflowCode Python 'create from aDocs; apply LSI functions IDF, None, Cosine; extract 20 topics; show topics table'
# LatentSemanticAnalyzer(aDocs).apply_term_weight_functions(global_weight_func = "IDF", local_weight_func = "None", normalizer_func = "Cosine").extract_topics(number_of_topics = 20).echo_topics_table( )
```

### NLP Template Engine

Here is an example using the NLP Template Engine, [AAr2, AAv3]:

```mathematica
Concretize["create from aDocs; apply LSI functions IDF, None, Cosine; extract 20 topics; show topics table", 
  "TargetLanguage" -> "Python"]
(* 
lsaObj = (LatentSemanticAnalyzer()
          .make_document_term_matrix(docs=aDocs, stop_words=None, stemming_rules=None,min_length=3)
          .apply_term_weight_functions(global_weight_func='IDF', local_weight_func='None',normalizer_func='Cosine')
          .extract_topics(number_of_topics=20, min_number_of_documents_per_term=20, method='SVD')
          .echo_topics_interpretation(number_of_terms=10, wide_form=True)
          .echo_statistical_thesaurus(terms=stemmerObj.stemWords([\"topics table\"]), wide_form=True, number_of_nearest_neighbors=12, method='cosine', echo_function=lambda x: print(x.to_string())))
*)

```

------

## References

### Articles

[AA1] Anton Antonov,
["A monad for Latent Semantic Analysis workflows"](https://mathematicaforprediction.wordpress.com/2019/09/13/a-monad-for-latent-semantic-analysis-workflows/),
(2019),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

[AA2] Anton Antonov,
["Random mandalas deconstruction in R, Python, and Mathematica"](https://mathematicaforprediction.wordpress.com/2022/03/01/random-mandala-deconstruction-in-r-python-and-mathematica/),
(2022),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

### Mathematica and R Packages 

[AAp1] Anton Antonov, 
[Monadic Latent Semantic Analysis Mathematica package](https://github.com/antononcube/MathematicaForPrediction/blob/master/MonadicProgramming/MonadicLatentSemanticAnalysis.m),
(2017),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp2] Anton Antonov,
[Latent Semantic Analysis Monad in R](https://github.com/antononcube/R-packages/tree/master/LSAMon-R)
(2019),
[R-packages at GitHub/antononcube](https://github.com/antononcube/R-packages).

### Python packages

[AAp3] Anton Antonov,
[SSparseMatrix Python package](https://pypi.org/project/SSparseMatrix),
(2021),
[PyPI](https://pypi.org).

[AAp4] Anton Antonov,
[SparseMatrixRecommender Python package](https://pypi.org/project/SparseMatrixRecommender),
(2021),
[PyPI](https://pypi.org).

[AAp5] Anton Antonov,
[RandomDataGenerators Python package](https://pypi.org/project/RandomDataGenerators),
(2021),
[PyPI](https://pypi.org).

[AAp6] Anton Antonov,
[RandomMandala Python package](https://pypi.org/project/RandomMandala),
(2021),
[PyPI](https://pypi.org).

[MZp1] Marinka Zitnik and Blaz Zupan,
[Nimfa: A Python Library for Nonnegative Matrix Factorization](https://pypi.org/project/nimfa/),
(2013-2019),
[PyPI](https://pypi.org).

[SDp1] Snowball Developers,
[SnowballStemmer Python package](https://pypi.org/project/snowballstemmer/),
(2013-2021),
[PyPI](https://pypi.org).

### Raku packages

[AAp7] Anton Antonov,
[DSL::English::LatentSemanticAnalysisWorkflows Raku package](https://github.com/antononcube/Raku-DSL-English-LatentSemanticAnalysisWorkflows),
(2018-2022),
[GitHub/antononcube](https://github.com/antononcube/Raku-DSL-English-LatentSemanticAnalysisWorkflows).
([At raku.land]((https://raku.land/zef:antononcube/DSL::English::LatentSemanticAnalysisWorkflows))).

### Repositories

[AAr1] Anton Antonov,
["Random mandalas deconstruction with R, Python, and Mathematica" presentation project](https://github.com/antononcube/SimplifiedMachineLearningWorkflows-book/tree/master/Presentations/Greater-Boston-useR-Group-Meetup-2022/RandomMandalasDeconstruction),
(2022)
[SimplifiedMachineLearningWorkflows-book at GitHub/antononcube](https://github.com/antononcube/SimplifiedMachineLearningWorkflows-book).

[AAr2] Anton Antonov,
["Raku for Prediction" book project](https://github.com/antononcube/RakuForPrediction-book),
(2021-2022),
[GitHub/antononcube](https://github.com/antononcube).


### Videos

[AAv1] Anton Antonov,
["TRC 2022 Implementation of ML algorithms in Raku"](https://www.youtube.com/watch?v=efRHfjYebs4),
(2022),
[Anton A. Antonov's channel at YouTube](https://www.youtube.com/channel/UC5qMPIsJeztfARXWdIw3Xzw).

[AAv2] Anton Antonov,
["Raku for Prediction"](https://www.youtube.com/watch?v=frpCBjbQtnA),
(2021),
[The Raku Conference (TRC) at YouTube](https://www.youtube.com/channel/UCnKoF-TknjGtFIpU3Bc_jUA).

[AAv3] Anton Antonov,
["NLP Template Engine, Part 1"](https://www.youtube.com/watch?v=a6PvmZnvF9I),
(2021),
[Anton A. Antonov's channel at YouTube](https://www.youtube.com/channel/UC5qMPIsJeztfARXWdIw3Xzw).

[AAv4] Anton Antonov
["Random Mandalas Deconstruction in R, Python, and Mathematica (Greater Boston useR Meetup, Feb 2022)"](https://www.youtube.com/watch?v=nKlcts5aGwY),
(2022),
[Anton A. Antonov's channel at YouTube](https://www.youtube.com/channel/UC5qMPIsJeztfARXWdIw3Xzw).