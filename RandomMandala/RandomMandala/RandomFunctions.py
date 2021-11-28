import numpy
import random
import matplotlib
import matplotlib.figure
from RandomMandala.RandomMandala import RandomMandala
from typing import Optional, Union


# ===========================================================
# Utilities
# ===========================================================
def _is_radius_number(obj):
    return isinstance(obj, float) or isinstance(obj, int) and obj > 0


def _is_radius_list(obj):
    return isinstance(obj, list) and all([_is_radius_number(x) for x in obj])


# ===========================================================
# Random mandala
# ===========================================================
def random_mandala(n_rows=None,
                   n_columns=None,
                   radius=1,
                   rotational_symmetry_order=6,
                   connecting_function="fill",
                   number_of_elements=6,
                   symmetric_seed=True,
                   face_color="0.2",
                   edge_color="0.2",
                   **kwargs):
    """Generates random mandalas.

    If 'n_rows' and 'n_columns' are None a figure object with one axes object is returned.

    If the argument 'radius' is a list of positive floats, then a "multi-mandala" is created
    with the mandalas corresponding to each number in the radius list being overlain.

    :type n_rows: int|None
    :param n_rows: Number of rows in the result figure.

    :type n_columns: int|None
    :param n_columns: Number of columns in the result figure.

    :type radius: int|list
    :param radius: Radius for the mandalas, a flot or a list of floats. If a list of floats the mandalas are overlain.

    :type rotational_symmetry_order: int|str|list|None
    :param rotational_symmetry_order: Number of copies of the seed segment that comprise the mandala.

    :type connecting_function: str|None
    :param connecting_function: Connecting function, one of "line", "fill", "bezier", "bezier_fill", "random", or None.
    If 'random' or None a random choice of the rest of values is made.

    :type number_of_elements: int
    :param number_of_elements: Controls how may graphics elements are in the seed segment.

    :type symmetric_seed: bool|str|None
    :param symmetric_seed: Specifies should the seed segment be symmetric or not.
    If 'random' of None random choice between True and False is made.

    :type face_color: str|list
    :param face_color: Face (fill) color.

    :type edge_color: str|list
    :param edge_color: Edge (line) color.

    :type kwargs: **dict
    :param kwargs: Arguments for matplotlib.pyplot.figure .

    :rtype fig: matplotlib.figure.Figure
    :return fig: A figure (object of the class matplotlib.figure.Figure .)
    """

    # Check symmetric_seed
    if not (isinstance(symmetric_seed, str) and symmetric_seed.lower() == "random" or
            isinstance(symmetric_seed, bool) or symmetric_seed is None):
        raise TypeError("""The argument 'symmetric_seed' is expected to be
             a Boolean, 'random', or None.""")

    # Check rotational_symmetry_order
    if not (isinstance(rotational_symmetry_order, str) and rotational_symmetry_order.lower() == "random" or
            isinstance(rotational_symmetry_order, int) and rotational_symmetry_order > 0 or
            rotational_symmetry_order is None or
            isinstance(rotational_symmetry_order, list)):
        raise TypeError("""The argument 'rotational_symmetry_order' is expected to be
             a positive integer, 'random', or None.""")

    local_connecting_function = connecting_function
    if connecting_function is None:
        local_connecting_function = "fill"

    # Check radius
    if not (_is_radius_number(radius) or _is_radius_list(radius)):
        raise TypeError("The argument 'radius' is expected to be a positive number or a list of positive numbers.")

    # Check number_of_elements
    if not isinstance(number_of_elements, int) and number_of_elements > 0:
        raise TypeError("The argument 'number_of_elements' is expected to be a positive integer.")

    # Delegate
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
    else:
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
                            rotational_symmetry_order: Union[int, list, str, None] = 6,
                            connecting_function: Optional[str] = "fill",
                            number_of_elements: int = 6,
                            symmetric_seed: Union[bool, str, None] = True,
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
                          rotational_symmetry_order: Union[int, list, str, None] = 6,
                          connecting_function: Optional[str] = "fill",
                          number_of_elements: int = 6,
                          symmetric_seed: Union[bool, str, None] = True,
                          face_color="0.2",
                          edge_color="0.2",
                          **kwargs):
    """Makes a random multi-mandala."""

    # Figure
    fig = figure
    if figure is None:
        # fig: matplotlib.pyplot.Figure = matplotlib.figure.Figure(**kwargs)
        fig: matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)

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
                           rotational_symmetry_order: Union[int, list, str, None] = 6,
                           connecting_function: Optional[str] = "fill",
                           number_of_elements: int = 6,
                           symmetric_seed: Union[bool, str, None] = True,
                           face_color="0.2",
                           edge_color="0.2",
                           **kwargs):
    """Makes a random mandala."""

    # Figure
    fig = figure
    if figure is None:
        # fig: matplotlib.pyplot.Figure = matplotlib.figure.Figure(**kwargs)
        fig: matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)

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
                                   number_of_elements=number_of_elements)
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
