# Random Mandala Python package

***Anton Antonov***    
[Python-packages at GitHub/antononcube](https://github.com/antononcube/Python-packages)   
***November 2021***   

## Introduction

This Python package implements the function `random_mandala` that generates plots (and images) of random mandalas.

The design, implementation *strategy*, and unit tests closely resemble the Wolfram Repository Function (WFR)
[`RandomMandala`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomMandala),
[AAf1].

(Another, very similar function at WFR is
[`RandomScribble`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomScribble), [AAf2].)

The mandalas made by `random_mandala` are generated through rotational symmetry of a “seed segment”. The Bezier mandala seeds are created using the Python package
[`bezier`](https://pypi.org/project/bezier/), [DHp1].

For detailed descriptions of Machine Learning studies that use collections of random mandalas see the articles [AA1, AA2].

------

## Installation

To install from GitHub use the shell command:

```shell
python3 -m pip install git+https://github.com/antononcube/Python-packages.git#egg=RandomMandala\&subdirectory=RandomMandala
```

To install from [pypi.org](https://pypi.org):

```shell
python3 -m pip install RandomMandala
```

------

## Details and arguments

- The mandalas made by `random_mandala` are generated through rotational symmetry of a “seed segment”. 

- The function `random_mandala` returns `matplotlib` figures (objects of type `matplotlib.figure.Figure`)

- The function `random_mandala` can be given arguments of the creation function `matplotlib.pyplot.figure`.

- The `matplotlib` figures produced by `random_mandala` can be converted to `PIL` images with the package function `figure_to_image`.

- If `n_rows` and `n_columns` are both `None` then a `matplotlib` figure object with one axes object is returned.

- There are two modes of making random mandalas: (i) single-mandala mode and (ii) multi-mandala mode. The multi-mandala mode is activated by giving the `radius` argument a list of positive numbers.

- If the argument `radius` is a list of positive numbers, then a "multi-mandala" is created
  with the mandalas corresponding to each number in the radius list being overlain.  

- Here are brief descriptions of the arguments:

  - `n_rows`: Number of rows in the result figure.

  - `n_columns`: Number of columns in the result figure.

  - `radius`: Radius for the mandalas, a number or a list of numbers. If a list of numbers then the mandalas are overlain.

  - `rotational_symmetry_order`: Number of copies of the seed segment that comprise the mandala.

  - `connecting_function`: Connecting function, one of "line", "fill", "bezier", "bezier_fill", "random", or `None`. If 'random' or `None` a random choice of the rest of values is made.

  - `number_of_elements`: Controls how may graphics elements are in the seed segment.

  - `symmetric_seed`: Specifies should the seed segment be symmetric or not.
    If 'random' of None random choice between `True` and `False` is made.

  - `face_color`: Face (fill) color.

  - `edge_color`: Edge (line) color.

-----

## Setup

Load the package `RandomMandala`, `matplotlib`, and `PIL`:


```python
from RandomMandala import random_mandala, figure_to_image
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from mpl_toolkits.axes_grid1 import ImageGrid
import random
```

------

## Examples

Here we generate a random mandala:


```python
random.seed(99)
fig = random_mandala()
```


    
![png](./docs/img/output_5_0.png)
    

Here we generate a figure with 12 (3x4) random mandalas:

```python
random.seed(33)
fig2 = random_mandala(n_rows=3, n_columns=4, figsize=(6,6))
fig2.tight_layout()
plt.show()
```


    
![png](./docs/img/output_7_0.png)
    


------

## Arguments details

### n_rows, n_columns

The arguments `n_rows` and `n_columns` specify the number of rows and columns respectively in the result figure object; `n_rows * n_columns` mandalas are generated:


```python
random.seed(22)
fig=random_mandala(n_rows=1, n_columns=3)
```


    
![png](./docs/img/output_9_0.png)
    


### radius

In single-mandala mode the argument `radius` specifies the radius of the seed segment and the mandala:


```python
fig = matplotlib.pyplot.figure(figsize=(8, 4), dpi=120)
k = 1
for r in [5, 10, 15, 20]:
    random.seed(2)
    fig = random_mandala(connecting_function="line", 
                         radius=r,
                         figure = fig,
                         location = (1, 4, k))
    ax = fig.axes[-1]
    ax.set_title("radius:" + str(r))
    ax.axis("on")
    k = k + 1
plt.show()
plt.close(fig)
```


    
![png](./docs/img/output_11_0.png)
    


If the value given to `radius` is a list of positive numbers then multi-mandala mode is used.
If `radius=[r[0],...,r[k]]`, then for each `r[i]` is made a mandala with radius `r[i]` and the mandalas are drawn upon each other according to their radii order:


```python
random.seed(99)
fig3=random_mandala(radius=[8,5,3], 
                    face_color=["blue", "green", 'red'],
                    connecting_function="fill")                
```


    
![png](./docs/img/output_13_0.png)
    


**Remark:** The code above uses different colors for the different radii.

### rotational_symmetry_order

The argument `rotational_symmetry_order` specifies how many copies of the seed segment comprise the mandala:


```python
fig = matplotlib.pyplot.figure(num=2322, figsize=(6, 12), dpi=120)
k = 1
for rso in [2, 3, 4, 6]:
    random.seed(122)
    fig = random_mandala(connecting_function="fill", 
                         symmetric_seed=True,
                         rotational_symmetry_order=rso,
                         figure = fig,
                         location = (1, 4, k))
    ax = fig.axes[-1]
    ax.set_title("order:" + str(rso))
    k = k + 1
plt.show()
plt.close(fig)
```


    
![png](./docs/img/output_17_0.png)
    


### symmetric_seed

The argument `symmetric_seed` specifies should the seed segment be symmetric or not:


```python
fig = matplotlib.pyplot.figure(num=2322, figsize=(4, 4), dpi=120)
k = 1
for ssd in [True, False]:
    random.seed(2)
    fig = random_mandala(connecting_function="fill", 
                         symmetric_seed=ssd,
                         figure = fig,
                         location = (1, 2, k))
    ax = fig.axes[-1]
    ax.set_title(str(ssd))
    k = k + 1
plt.show()
plt.close(fig)
```


    
![png](./docs/img/output_19_0.png)
    


------

## Applications

### Generate a collection of images

In certain Machine Learning (ML) studies it can be useful to be able to generate large enough collections of (random) images. 

In the code block below we: 
- Generate 64 random mandala *plots*
- Convert them into `PIL` images using the package function `figure_to_image`
- Invert and binarize the images
- Plot the images in an image grid


```python
# A list to accumulate random mandala images
mandala_images = []

# Generation loop
random.seed(765)
for i in range(64):
    
    # Generate one random mandala figure
    fig2 = random_mandala(n_rows=None,
                          n_columns=None,
                          radius=[8, 6, 3],
                          rotational_symmetry_order=6,
                          symmetric_seed=True,
                          number_of_elements=4,
                          connecting_function='random',
                          face_color='0.2')
    fig2.tight_layout()
    
    # Convert the figure into an image and add it to the list
    mandala_images = mandala_images + [figure_to_image(fig2)]
    
    # Close figure to save memoru
    plt.close(fig2)

# Invert image colors    
mandala_images2 = [ImageOps.invert(img) for img in mandala_images]

# Binarize images
mandala_images3 = [im.convert('1') for im in mandala_images2]

# Make a grid of images and display it
fig3 = plt.figure(figsize=(14., 14.))
grid = ImageGrid(fig3, 111,
                 nrows_ncols=(8, 8),
                 axes_pad=0.02,
                 )

for ax, img in zip(grid, mandala_images3):
    ax.imshow(img)
    ax.set(xticks=[], yticks=[])

plt.show()
```


    
![png](./docs/img/output_21_0.png)
    


-----

## Neat examples
    
### A table of random mandalas


```python
random.seed(124)
fig=random_mandala(n_rows=6, n_columns=6, figsize=(10,10), dpi=240)
```


    
![png](./docs/img/output_23_0.png)
    


### A table of open colorized mandalas


```python
fig = matplotlib.pyplot.figure(figsize=(10, 10), dpi=120)
k = 1
random.seed(883)
for rso in [2 * random.random() + 2 for _ in range(36)]:
    random.seed(33)
    fig = random_mandala(connecting_function="bezier_fill",
                         radius=3,
                         face_color="darkblue",
                         rotational_symmetry_order=rso,
                         number_of_elements=8,
                         figure=fig,
                         location=(6, 6, k))
    ax = fig.axes[-1]
    ax.set_axis_off()
    k = k + 1

plt.show()
plt.close(fig)
```


    
![png](./docs/img/output_25_0.png)
    


------

## References

### Articles

[AA1] Anton Antonov,
["Comparison of dimension reduction algorithms over mandala images generation"](https://mathematicaforprediction.wordpress.com/2017/02/10/comparison-of-dimension-reduction-algorithms-over-mandala-images-generation/),
(2017),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

[AA2] Anton Antonov,
["Generation of Random Bethlehem Stars"](https://mathematicaforprediction.wordpress.com/2020/12/21/generation-of-random-bethlehem-stars/),
(2020),
[MathematicaForPrediction at WordPress](https://mathematicaforprediction.wordpress.com).

### Functions

[AAf1] Anton Antonov,
[`RandomMandala`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomMandala),
(2019),
[Wolfram Function Repository](https://resources.wolframcloud.com/FunctionRepository).

[AAf2] Anton Antonov,
[`RandomScribble`](https://resources.wolframcloud.com/FunctionRepository/resources/RandomScribble),
(2020),
[Wolfram Function Repository](https://resources.wolframcloud.com/FunctionRepository).

### Packages

[DHp1] Daniel Hermes,
[`bezier` Python package](https://pypi.org/project/bezier/),
(2016),
[PyPi.org](https://pypi.org).

