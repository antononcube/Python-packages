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
                   return_type="figure",
                   **kwargs):
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
    :param kwargs: Arguments for matplotlib.pyplot.figure .
    :param return_type: Specifies the return type, one of: "figure", "image", "axes", or None.
    :return res:
    """

    if not (isinstance(symmetric_seed, str) and symmetric_seed.lower() == "random" or
            isinstance(symmetric_seed, bool) or symmetric_seed is None):
        raise TypeError("""The argument 'symmetric_seed' is expected to be
             a Boolean, 'random', or None.""")

    if not (isinstance(rotational_symmetry_order, str) and rotational_symmetry_order.lower() == "random" or
            isinstance(rotational_symmetry_order, int) and rotational_symmetry_order > 0 or
            rotational_symmetry_order is None or
            isinstance(rotational_symmetry_order, list)):
        raise TypeError("""The argument 'rotational_symmetry_order' is expected to be
             a positive integer, 'random', or None.""")

    local_connecting_function = connecting_function
    if connecting_function is None:
        local_connecting_function = "fill"

    if isinstance(n_rows, int) and n_rows > 0 and isinstance(n_columns, int) and n_columns > 0:
        return _random_mandalas_figure(n_rows=n_rows,
                                       n_columns=n_columns,
                                       radius=radius,
                                       rotational_symmetry_order=rotational_symmetry_order,
                                       connecting_function=local_connecting_function,
                                       number_of_elements=number_of_elements,
                                       symmetric_seed=symmetric_seed,
                                       face_color=face_color,
                                       edge_color=edge_color,
                                       **kwargs)
    elif isinstance(size, int) and size == 1:
        if (isinstance(radius, float) or isinstance(radius, int)) and radius > 0:
            return _random_mandala_single(figure=None,
                                          axes=None,
                                          location=None,
                                          radius=radius,
                                          rotational_symmetry_order=rotational_symmetry_order,
                                          connecting_function=local_connecting_function,
                                          number_of_elements=number_of_elements,
                                          symmetric_seed=symmetric_seed,
                                          face_color=face_color,
                                          edge_color=edge_color,
                                          **kwargs)
        else:
            return _random_mandala_multi(figure=None,
                                         location=None,
                                         radius=radius,
                                         rotational_symmetry_order=rotational_symmetry_order,
                                         connecting_function=local_connecting_function,
                                         number_of_elements=number_of_elements,
                                         symmetric_seed=symmetric_seed,
                                         face_color=face_color,
                                         edge_color=edge_color,
                                         **kwargs)


# ===========================================================
# Random mandala figure
# ===========================================================
def _random_mandalas_figure(n_rows=None,
                            n_columns=None,
                            radius=1,
                            rotational_symmetry_order=6,
                            connecting_function: str = "fill",
                            number_of_elements=6,
                            symmetric_seed=True,
                            face_color="0.2",
                            edge_color="0.2",
                            **kwargs):
    """Makes a figure with random mandalas."""

    fig: matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)

    for i in range(n_rows):
        for j in range(n_columns):
            locationSpec = (n_rows, n_columns, i * n_columns + j + 1)

            if isinstance(radius, list):
                rm_func = _random_mandala_multi
            else:
                rm_func = _random_mandala_single

            rm_func(figure=fig,
                    axes=None,
                    location=locationSpec,
                    radius=radius,
                    rotational_symmetry_order=rotational_symmetry_order,
                    connecting_function=connecting_function,
                    number_of_elements=number_of_elements,
                    symmetric_seed=symmetric_seed,
                    face_color=face_color,
                    edge_color=edge_color)

    return fig


# ===========================================================
# Random mandala (multi)
# ===========================================================
def _random_mandala_multi(figure=None,
                          axes=None,
                          location=None,
                          radius=[6, 4, 2],
                          rotational_symmetry_order=6,
                          connecting_function: str = "fill",
                          number_of_elements=6,
                          symmetric_seed=True,
                          face_color="0.2",
                          edge_color="0.2",
                          **kwargs):
    """Makes a random multi-mandala."""

    # Figure
    fig = figure
    if figure is None:
        fig = matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)

    # Location spec
    locationSpec = location
    if location is None:
        locationSpec = (1, 1, 1)

    ax = fig.add_subplot(*locationSpec)

    faceColors = numpy.resize(face_color, len(radius))
    edgeColors = numpy.resize(edge_color, len(radius))
    rotSymOrders = numpy.resize(rotational_symmetry_order, len(radius))

    for i in range(len(radius)):
        r = radius[i]
        fc = faceColors[i]
        ec = edgeColors[i]
        rso = rotSymOrders[i]
        _random_mandala_single(figure=fig,
                               axes=ax,
                               location=locationSpec,
                               radius=r,
                               rotational_symmetry_order=rso,
                               connecting_function=connecting_function,
                               number_of_elements=number_of_elements,
                               symmetric_seed=symmetric_seed,
                               face_color=fc,
                               edge_color=ec)

    return fig


# ===========================================================
# Random mandala (single)
# ===========================================================
def _random_mandala_single(figure=None,
                           axes=None,
                           location=None,
                           radius=1,
                           rotational_symmetry_order=6,
                           connecting_function: str = "fill",
                           number_of_elements=6,
                           symmetric_seed=True,
                           face_color="0.2",
                           edge_color="0.2",
                           **kwargs):
    """Makes a random mandala."""

    # Figure
    fig = figure
    if figure is None:
        fig = matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)

    # Axes
    ax = axes

    # Location spec
    locationSpec = location
    if location is None:
        locationSpec = 111

    # Rotational symmetry order
    if isinstance(rotational_symmetry_order, str) and rotational_symmetry_order.lower() == "random" or \
            rotational_symmetry_order is None:
        rso = random.sample([3, 4, 5, 6, 7, 12], 1)[0]
    else:
        rso = rotational_symmetry_order

    # Symmetric seed
    if isinstance(symmetric_seed, str) and symmetric_seed.lower() == "random" or symmetric_seed is None:
        ssb = random.random() > 0.3
    else:
        ssb = symmetric_seed

    # Generate seed
    rMandala = (RandomMandala(figure=fig, axes=ax)
                .make_seed_segment(radius=radius,
                                   angle=numpy.pi / rso,
                                   number_of_elements=6)
                .make_seed_symmetric(ssb))

    # Connect, rotate, place
    conFunc = connecting_function.lower()
    if conFunc == 'random':
        conFunc = random.sample(['line', 'bezier', 'fill', 'bezier_fill'], 1)[0]

    if conFunc in {"fill", "polygon"}:

        rMandala.rotate_and_fill(face_color=face_color,
                                 edge_color=edge_color,
                                 location=locationSpec,
                                 ax=ax)

    elif conFunc == "line":

        rMandala.rotate_and_fill(face_color=None,
                                 edge_color=edge_color,
                                 location=locationSpec,
                                 ax=ax)

    elif conFunc == "bezier":

        rMandala.rotate_and_bezier(face_color=face_color,
                                   edge_color=edge_color,
                                   location=locationSpec,
                                   ax=ax)

    elif conFunc in {"bezier_fill", "bezier fill", "bezierfill"}:

        rMandala.rotate_and_bezier_fill(face_color=face_color,
                                        edge_color=edge_color,
                                        location=locationSpec,
                                        ax=ax)

    else:
        raise TypeError("""The argument 'connecting_function' is expected to be one of 
        'fill', 'line', 'bezier', 'bezier_fill', 'random', or None.""")

    return fig
