# Random Mandalas Python package

## In brief

This Python package implements the function `random_mandala` that generates plots (and images) 
of random mandalas.

The design, implementation *strategy*, and unit tests closely resemble the Wolfram Repository Function (WFR)  
[`RandomMandala`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomMandala/),
[AAf1].

------

## Installation 

To install from GitHub use the shell command:

```shell
python -m pip install git+https://github.com/antononcube/Python-packages.git#egg=RandomMandala\&subdirectory=RandomMandala
```

------

## Examples

Here we generate random mandala:

```python
random_mandala()
```

Here we generate a `matplotlib` figure with 12 (3x4) random mandalas:

```python
random_mandala_figure(n_row=3, n_col=4, connecting_function="fill")
```


------

## References

[AAf1] Anton Antonov,
[`RandomMandala`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomMandala/),
(2019),
[Wolfram Function Repository](https://resources.wolframcloud.com/FunctionRepository).

[AAf2] Anton Antonov,
[`RandomScribble`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomScribble/),
(2020),
[Wolfram Function Repository](https://resources.wolframcloud.com/FunctionRepository).