import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from PIL import Image, ImageOps

from RandomMandala import *
from RandomMandala import *

# ===========================================================

# fig = random_mandala(n_rows=None,
#                      n_columns=None,
#                      radius=[6, 4, 2],
#                      rotational_symmetry_order=[12, 6, 4],
#                      symmetric_seed=True,
#                      connecting_function="bezier_fill",
#                      face_color=["purple", 'red', 'darkred'],
#                      figsize=(10, 10), dpi=120)

# fig = random_mandala(n_rows=4,
#                      n_columns=4,
#                      radius=[6, 4, 2],
#                      rotational_symmetry_order=[12, 6, 4],
#                      symmetric_seed=True,
#                      connecting_function="bezier_fill",
#                      face_color=["0.8", 'lightblue', 'green'],
#                      figsize=(10, 10), dpi=120)
#
# fig.tight_layout()
# fig.show()


# ===========================================================
# A Grid of images
# ===========================================================
mandala_images = []
for i in range(100):
    fig2 = random_mandala(n_rows=None,
                          n_columns=None,
                          radius=[8, 6, 3],
                          rotational_symmetry_order=6,
                          symmetric_seed=True,
                          number_of_elements=6,
                          connecting_function="bezier_fill",
                          face_color="0.")
    fig2.tight_layout()
    mandala_images = mandala_images + [figure_to_image(fig2)]
    plt.close(fig2)

# for im in mandala_images:
#     im.show()

mandala_images2 = [ImageOps.invert(img.convert('RGB')) for img in mandala_images]

fig3 = plt.figure(figsize=(12., 12.))
grid = ImageGrid(fig3, 111,
                 nrows_ncols=(10, 10),
                 axes_pad=0.02,
                 )

for ax, img in zip(grid, mandala_images2):
    ax.imshow(img)
    ax.set(xticks=[], yticks=[])

fig3.show()