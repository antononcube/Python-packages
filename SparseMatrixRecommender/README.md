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


------

## Workflows 

Here is a diagram that encompasses the workflows this package supports (or will support):

![SMR-workflows](https://github.com/antononcube/SimplifiedMachineLearningWorkflows-book/raw/master/Part-2-Monadic-Workflows/Diagrams/A-monad-for-Sparse-Matrix-Recommender-workflows/SMR-workflows.jpeg)

Here is a diagram of typical pipeline building using a `SparseMatrixRecommender` object:

![SMRMon-pipeline-Python](https://github.com/antononcube/SimplifiedMachineLearningWorkflows-book/raw/master/Part-2-Monadic-Workflows/Diagrams/A-monad-for-Recommender-workflows/SMRMon-pipeline-Python.jpg)

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
over Titanic data and recommendations for the profile "male" and "1st':

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

**Remark:** More examples can be found in the 

------

## Related Mathematica packages

The software monad Mathematica package 
["MonadicSparseMatrixRecommender.m"](https://github.com/antononcube/MathematicaForPrediction/blob/master/MonadicProgramming/MonadicSparseMatrixRecommender.m)
[AAp1], provides recommendation pipelines similar to the pipelines create with this package.

here is a Mathematica monadic pipeline for creation of a recommender
over Titanic data and recommendations for the profile "male" and "1st':

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

Here is the corresponding Python pipeline:


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
[AAp4], can be used to make matrices for `SparseMatrixRecommender`.

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

## References

### Articles

[AA1] Anton Antonov,
["Mapping Sparse Matrix Recommender to Streams Blending Recommender"](https://github.com/antononcube/MathematicaForPrediction/blob/master/Documentation/MappingSMRtoSBR/Mapping-Sparse-Matrix-Recommender-to-Streams-Blending-Recommender.pdf)
(2017),
[MathematicaForPrediction at GitHub](https://github.com/antononcube/MathematicaForPrediction).

### Mathematica and R Packages 

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
