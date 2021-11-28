import numpy
import random
import matplotlib
import PIL
from RandomMandala.RandomMandala import RandomMandala


# ===========================================================
# Random mandala
# ===========================================================
def random_mandala(size=1,
                   n_rows=None,
                   n_columns=None,
                   radius=1,
                   rotational_symmetry_order=6,
                   connecting_function="fill",
                   number_of_elements=6,
                   symmetric_seed=True,
                   face_color="0.2",
                   edge_color="0.2",
                   return_type="figure"):
    """Generates random mandalas.

    :param size: Number of mandalas to generate.
    :param n_rows: Number of rows in the result figure.
    :param n_columns: Number of columns in the result figure.
    :param radius: Radius for the mandalas, a flot or a list of floats. If a list of floats the mandalas are overlain.
    :param rotational_symmetry_order: Number of copies of the seed segment that comprise the mandala.
    :param connecting_function: Connecting function, one of "line", "fill", "bezier", "bezier_fill", "random", or None.
    :param number_of_elements: Controls how may graphics elements are in the seed segment.
    :param symmetric_seed: Specifies should the seed segment be symmetric or not.
    :param face_color: Face color (string or tuple.)
    :param edge_color: Edge color (string or tuple.)
    :param return_type: Specifies the return type, one of: "figure", "image", "axes", or None.
    :return res:
    """

    if not (isinstance(symmetric_seed, str) and symmetric_seed.lower() == "random" or
            isinstance(symmetric_seed, bool) or symmetric_seed is None):
        raise TypeError("""The argument 'symmetric_seed' is expected to be
             a Boolean, 'random', or None.""")

    if not (isinstance(rotational_symmetry_order, str) and rotational_symmetry_order.lower() == "random" or
            isinstance(rotational_symmetry_order, int) and rotational_symmetry_order > 0 or
            rotational_symmetry_order is None):
        raise TypeError("""The argument 'rotational_symmetry_order' is expected to be
             a positive integer, 'random', or None.""")

    if isinstance(n_rows, int) and n_rows > 0 and isinstance(n_columns, int) and n_columns > 0:
        return _random_mandala_figure(n_rows=n_rows,
                                      n_columns=n_columns,
                                      radius=radius,
                                      rotational_symmetry_order=rotational_symmetry_order,
                                      connecting_function=connecting_function,
                                      number_of_elements=number_of_elements,
                                      symmetric_seed=symmetric_seed,
                                      face_color=face_color,
                                      edge_color=edge_color)


# ===========================================================
# Random mandala figure
# ===========================================================
def _random_mandala_figure(n_rows=None,
                           n_columns=None,
                           radius=1,
                           rotational_symmetry_order=6,
                           connecting_function="fill",
                           number_of_elements=6,
                           symmetric_seed=True,
                           face_color="0.2",
                           edge_color="0.2"):
    """Makes a figure with random mandalas."""

    fig: matplotlib.pyplot.Figure = matplotlib.pyplot.figure(figsize=(10, 10), dpi=120)

    nrow, ncol = n_rows, n_columns
    for i in range(nrow):
        for j in range(ncol):

            if isinstance(rotational_symmetry_order, str) and rotational_symmetry_order.lower() == "random" or \
                    rotational_symmetry_order is None:
                rso = random.sample([3, 4, 5, 6, 7, 12], 1)[0]
            else:
                rso = rotational_symmetry_order

            if isinstance(symmetric_seed, str) and symmetric_seed.lower() == "random" or symmetric_seed is None:
                ssb = random.random() > 0.3
            else:
                ssb = symmetric_seed

            rMandala = (RandomMandala(fig)
                        .make_seed_segment(radius=radius,
                                           angle=numpy.pi / rso,
                                           number_of_elements=6)
                        .make_seed_symmetric(ssb)
                        .rotate_and_fill(face_color=face_color,
                                         edge_color=edge_color,
                                         location=(nrow, ncol, i * ncol + j + 1)))
    return fig
