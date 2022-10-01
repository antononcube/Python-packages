# Sparse Matrix Recommender (SMR) Python package

## Introduction

This Python package, `SparseMatrixRecommender`, has different functions for computations of recommendations
based on (user) profile or history using Sparse Linear Algebra (SLA). The package mirrors
the Mathematica implementation [AAp1]. 
(There is also a corresponding implementation in R; see [AAp2]). 

The package is based on a certain "standard" Information retrieval paradigm -- it utilizes 
Latent Semantic Indexing (LSI) functions like IDF, TF-IDF, etc. Hence, the package also has 
document-term matrix creation functions and LSI application functions. I included them in the 
package since I wanted to minimize the external package dependencies.

The package includes two data-sets `dfTitanic` and `dfMushroom` in order to make easier the
writing of introductory examples and unit tests.

For more theoretical description see the article 
["Mapping Sparse Matrix Recommender to Streams Blending Recommender"](https://github.com/antononcube/MathematicaForPrediction/blob/master/Documentation/MappingSMRtoSBR/Mapping-Sparse-Matrix-Recommender-to-Streams-Blending-Recommender.pdf)
, [AA1].

For detailed examples see the files
["SMR-experiments-large-data.py"](https://github.com/antononcube/Python-packages/blob/main/SparseMatrixRecommender/examples/SMR-experiments-large-data.py)
and
["SMR-creation-from-long-form.py"](https://github.com/antononcube/Python-packages/blob/main/SparseMatrixRecommender/examples/SMR-creation-from-long-form.py).

The list of features and its implementation status is given in the [org-mode](https://orgmode.org) file
["SparseMatrixRecommender-work-plan.org"](https://github.com/antononcube/Python-packages/blob/main/org/SparseMatrixRecommender-work-plan.org).

**Remark:** "SMR" stands for "Sparse Matrix Recommender". Most of the operations of this Python package
mirror the operations of the software monads "SMRMon-WL", "SMRMon-R", [AAp1, AAp2].

------

## Workflows 

Here is a diagram that encompasses the workflows this package supports (or will support):

[![SMR-workflows](https://github.com/antononcube/SimplifiedMachineLearningWorkflows-book/raw/master/Part-2-Monadic-Workflows/Diagrams/A-monad-for-Sparse-Matrix-Recommender-workflows/SMR-workflows.jpeg)](https://github.com/antononcube/SimplifiedMachineLearningWorkflows-book/raw/master/Part-2-Monadic-Workflows/Diagrams/A-monad-for-Sparse-Matrix-Recommender-workflows/SMR-workflows.pdf)

Here is narration of a certain workflow scenario:

1. Get a dataset.
2. Create contingency matrices for a given identifier column and a set of "tag type" columns.
3. Examine recommender matrix statistics.
4. If the assumptoins about the data hold apply LSI functions.
   - For example, the "usual trio" IDF, Frequency, Cosine.
5. Do (verify) example profile recommendations.
6. If satisfactory results are obtained use the recommender as a nearest neighbors classifier. 


------

## Monadic design

Here is a diagram of typical pipeline building using a `SparseMatrixRecommender` object:

![SMRMon-pipeline-Python](https://github.com/antononcube/SimplifiedMachineLearningWorkflows-book/raw/master/Part-2-Monadic-Workflows/Diagrams/A-monad-for-Recommender-workflows/SMRMon-pipeline-Python.jpg)

**Remark:** The **monadic design** allows "pipelining" of the SMR operations -- see the usage example section.


------

## Installation

To install from GitHub use the shell command:

```shell
python -m pip install git+https://github.com/antononcube/Python-packages.git#egg=SparseMatrixRecommender\&subdirectory=SparseMatrixRecommender
```

To install from [PyPI](https://pypi.org/project/SparseMatrixRecommender/):

```shell
python -m pip install SparseMatrixRecommender
``` 

------

## Related Python packages

This package is based on the Python package 
[`SSparseMatrix`](https://github.com/antononcube/Python-packages/tree/main/SSparseMatrix), 
[AAp5].

The package 
[LatentSemanticAnalyzer](https://github.com/antononcube/Python-packages/tree/main/LatentSemanticAnalyzer), 
[AAp6], uses the cross tabulation and LSI functions of this package.

------

## Usage example

Here is an example of an SMR pipeline for creation of a recommender
over Titanic data and recommendations for the profile "passengerSex:male" and "passengerClass:1st":

```python
from SparseMatrixRecommender.SparseMatrixRecommender import *
from SparseMatrixRecommender.DataLoaders import *

dfTitanic = load_titanic_data_frame()

smrObj = (SparseMatrixRecommender()
          .create_from_wide_form(data = dfTitanic, 
                                 item_column_name="id", 
                                 columns=None, 
                                 add_tag_types_to_column_names=True, 
                                 tag_value_separator=":")
          .apply_term_weight_functions(global_weight_func = "IDF", 
                                       local_weight_func = "None", 
                                       normalizer_func = "Cosine")
          .recommend_by_profile(profile=["passengerSex:male", "passengerClass:1st"], 
                                nrecs=12)
          .join_across(data=dfTitanic, on="id")
          .echo_value())
```

**Remark:** More examples can be found the directory 
["./examples"](https://github.com/antononcube/Python-packages/tree/main/SparseMatrixRecommender/examples).

------

## Related Mathematica packages

The software monad Mathematica package 
["MonadicSparseMatrixRecommender.m"](https://github.com/antononcube/MathematicaForPrediction/blob/master/MonadicProgramming/MonadicSparseMatrixRecommender.m)
[AAp1], provides recommendation pipelines similar to the pipelines created with this package.

Here is a Mathematica monadic pipeline that corresponds to the Python pipeline above:

```mathematica
smrObj =
  SMRMonUnit[]⟹
   SMRMonCreate[dfTitanic, "id", 
                "AddTagTypesToColumnNames" -> True, 
                "TagValueSeparator" -> ":"]⟹
   SMRMonApplyTermWeightFunctions["IDF", "None", "Cosine"]⟹
   SMRMonRecommendByProfile[{"passengerSex:male", "passengerClass:1st"}, 12]⟹
   SMRMonJoinAcross[dfTitanic, "id"]⟹
   SMRMonEchoValue[];   
```

*(Compare the pipeline diagram above with the 
[corresponding diagram using Mathematica notation](https://github.com/antononcube/SimplifiedMachineLearningWorkflows-book/raw/master/Part-2-Monadic-Workflows/Diagrams/A-monad-for-Recommender-workflows/SMRMon-pipeline.jpeg)
.)*

------

## Related R packages

The package 
[`SMRMon-R`](https://github.com/antononcube/R-packages/tree/master/SMRMon-R), 
[AAp2], implements a software monad for SMR workflows. 
Most of `SMRMon-R` functions delegate to `SparseMatrixRecommender`.

The package 
[`SparseMatrixRecommenderInterfaces`](https://github.com/antononcube/R-packages/tree/master/SparseMatrixRecommenderInterfaces), 
[AAp3], provides functions for interactive 
[Shiny](https://shiny.rstudio.com)
interfaces for the recommenders made with `SparseMatrixRecommender` and/or `SMRMon-R`.

The package 
[`LSAMon-R`](https://github.com/antononcube/R-packages/tree/master/LSAMon-R),
[AAp4], can be used to make matrices for `SparseMatrixRecommender` and/or `SMRMon-R`.

Here is the `SMRMon-R` pipeline that corresponds to the Python pipeline above:

```r
smrObj <-
  SMRMonCreate( data = dfTitanic, 
                itemColumnName = "id", 
                addTagTypesToColumnNamesQ = TRUE, 
                sep = ":") %>%
  SMRMonApplyTermWeightFunctions(globalWeightFunction = "IDF", 
                                 localWeightFunction = "None", 
                                 normalizerFunction = "Cosine") %>%
  SMRMonRecommendByProfile( profile = c("passengerSex:male", "passengerClass:1st"), 
                            nrecs = 12) %>%
  SMRMonJoinAcross( data = dfTitanic, by = "id") %>%
  SMRMonEchoValue
```

------

## Recommender comparison project

The project repository "Scalable Recommender Framework", [AAr1],
has documents, diagrams, tests, and benchmarks of a recommender system implemented in multiple programming languages.

This Python recommender package is a decisive winner in the comparison -- see the first 10 min of 
the video recording [AAv1] or the benchmarks at [AAr1].

------

## Code generation with natural language commands

### Using grammar-based interpreters

The project "Raku for Prediction", [AAr2, AAv2, AAp6], has a Domain Specific Language (DSL) grammar and interpreters 
that allow the generation of SMR code for corresponding Mathematica, Python, R, and Raku packages. 

Here is Command Line Interface (CLI) invocation example that generate code for this package:

```shell
> ToRecommenderWorkflowCode Python 'create with dfTitanic; apply the LSI functions IDF, None, Cosine;recommend by profile 1st and male' 
obj = SparseMatrixRecommender().create_from_wide_form(data = dfTitanic).apply_term_weight_functions(global_weight_func = "IDF", local_weight_func = "None", normalizer_func = "Cosine").recommend_by_profile( profile = ["1st", "male"])
```

### NLP Template Engine

Here is an example using the NLP Template Engine, [AAr2, AAv3]:

```mathematica
Concretize["create with dfTitanic; apply the LSI functions IDF, None, Cosine;recommend by profile 1st and male", 
 "TargetLanguage" -> "Python"]

(*
"smrObj = (SparseMatrixRecommender()
 .create_from_wide_form(data = None, item_column_name=\"id\", columns=None, add_tag_types_to_column_names=True, tag_value_separator=\":\")
 .apply_term_weight_functions(\"IDF\", \"None\", \"Cosine\")
 .recommend_by_profile(profile=[\"1st\", \"male\"], nrecs=profile)
 .join_across(data=None, on=\"id\")
 .echo_value())"
*)
```


------

## References

### Articles

[AA1] Anton Antonov,
["Mapping Sparse Matrix Recommender to Streams Blending Recommender"](https://github.com/antononcube/MathematicaForPrediction/blob/master/Documentation/MappingSMRtoSBR/Mapping-Sparse-Matrix-Recommender-to-Streams-Blending-Recommender.pdf)
(2017),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

### Mathematica/WL and R packages 

[AAp1] Anton Antonov, 
[Monadic Sparse Matrix Recommender Mathematica package](https://github.com/antononcube/MathematicaForPrediction/blob/master/MonadicProgramming/MonadicSparseMatrixRecommender.m),
(2018),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

[AAp2] Anton Antonov,
[Sparse Matrix Recommender Monad in R](https://github.com/antononcube/R-packages/tree/master/SMRMon-R)
(2019),
[R-packages at GitHub/antononcube](https://github.com/antononcube/R-packages).

[AAp3] Anton Antonov,
[Sparse Matrix Recommender framework interface functions](https://github.com/antononcube/R-packages/tree/master/SparseMatrixRecommenderInterfaces)
(2019),
[R-packages at GitHub/antononcube](https://github.com/antononcube/R-packages).

[AAp4] Anton Antonov,
[Latent Semantic Analysis Monad in R](https://github.com/antononcube/R-packages/tree/master/LSAMon-R)
(2019),
[R-packages at GitHub/antononcube](https://github.com/antononcube/R-packages).

### Python packages

[AAp5] Anton Antonov,
[SSparseMatrix package in Python](https://github.com/antononcube/Python-packages/tree/master/SSparseMatrix)
(2021),
[Python-packages at GitHub/antononcube](https://github.com/antononcube/Python-packages).

[AAp6] Anton Antonov,
[LatentSemanticAnalyzer package in Python](https://github.com/antononcube/Python-packages/tree/main/LatentSemanticAnalyzer)
(2021),
[Python-packages at GitHub/antononcube](https://github.com/antononcube/Python-packages).

### Raku packages

[AAp6] Anton Antonov,
[DSL::English::RecommenderWorkflows Raku package](ttps://github.com/antononcube/Raku-DSL-English-RecommenderWorkflows),
(2018-2022),
[GitHub/antononcube](https://github.com/antononcube/Raku-DSL-English-RecommenderWorkflows).
([At raku.land]((https://raku.land/zef:antononcube/DSL::English::RecommenderWorkflows))).

### Repositories

[AAr1] Anton Antonov,
[Scalable Recommender Framework project](https://github.com/antononcube/Scalable-Recommender-Framework-project),
(2022)
[GitHub/antononcube](https://github.com/antononcube).

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
