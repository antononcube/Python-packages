from typing import Optional

import matplotlib
import matplotlib.figure
import matplotlib.pyplot

from ChernoffFace.ChernoffFace import chernoff_face_for_axes


# ===========================================================
# Utilities
# ===========================================================
def _is_face_part_number(obj):
    return isinstance(obj, float) or isinstance(obj, int) and obj > 0


def _is_face_part_list(obj):
    return isinstance(obj, (list, tuple)) and all([_is_face_part_number(x) for x in obj])


def _is_face_part_dict(obj):
    return isinstance(obj, dict) and all([_is_face_part_number(x) for x in list(obj.values())])


# ===========================================================
# Chernoff face
# ===========================================================
def chernoff_face(data,
                  make_symmetric: bool = True,
                  rescale_range_function=None,
                  figure: Optional[matplotlib.figure.Figure] = None,
                  location=None,
                  **kwargs):
    """Makes Chernoff face diagrams.

    :type data: list|tuple|dict
    :param data: Data to be plotted.

    :type make_symmetric: bool
    :param make_symmetric: The faces can be made symmetric for shorter faces.

    :param rescale_range_function: A function to rescale the data with.

    :type figure: matplotlib.pyplot.Figure|None
    :param figure: Figure to add the random mandala to.

    :type location: tuple|None
    :param location: Location spec to add the random mandala to.

    :type kwargs: **dict
    :param kwargs: Arguments for matplotlib.pyplot.figure .

    :rtype fig: matplotlib.figure.Figure
    :return fig: A figure (object of the class matplotlib.figure.Figure .)
    """

    if _is_face_part_list(data):
        return None

    # Check make_symmetric
    if not isinstance(make_symmetric, bool):
        raise TypeError("""The argument 'make_symmetric' is expected to be a Boolean""")

    fig, ax = matplotlib.pyplot.subplots()

    chernoff_face_for_axes(data=data, axes=ax)
    ax.set_aspect('equal')

    return fig
