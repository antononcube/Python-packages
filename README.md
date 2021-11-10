# Python-packages

Miscellaneous Python packages. 
Some correspond to the packages in the repositories 
[MathematicaForPrediction](https://github.com/antononcube/MathematicaForPrediction/) 
and
[R-packages](https://github.com/antononcube/R-packages).


## On package licensing

Some loosely adhered to rules for the package licenses in this repository follow.

- The "computer science" packages have BSD-3 or LGPL-3 licenses.

  - For example, the monad code generation package 
    [StateMonadCodeGenerator](https://github.com/antononcube/R-packages/tree/master/StateMonadCodeGenerator). 

- The more "academic" packages have GPL-3 licenses.

- In general the simple packages have BSD-3 or LGPL-3 licenses.

  - For example, the package [OutlierIdentifiers](https://github.com/antononcube/R-packages/tree/master/OutlierIdentifiers) 
    is very simple. (Hence with BSD-3.)

- The package license is based on the license(s) of the most important package(s) it builds upon.

  - For example, if a package from this repository is based on one package, 
    and the latter is with MIT license, 
    then the package from this repository is also with MIT license. 

- If a package is with a GPL-3 license that is because:
 
  - At least one of the underlying important packages is with GPL-3
   
  - The original version of the package was published with GPL-3
  
  - GPL-3 is the default and preferred license


