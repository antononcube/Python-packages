import math
from typing import Optional

import PIL
import matplotlib
import matplotlib.cm
import matplotlib.figure
import matplotlib.pyplot
import numpy
from ChernoffFace.ChernoffFace import single_chernoff_face


# ===========================================================
# Utilities
# ===========================================================
def _is_face_part_number(obj):
    return isinstance(obj, (float, int))


def _is_face_part_list(obj):
    return isinstance(obj, (list, tuple)) and all([_is_face_part_number(x) for x in obj])


def _is_face_part_dict(obj):
    return isinstance(obj, dict) and all([_is_face_part_number(x) for x in list(obj.values())])


def _is_face_part_dict_list(obj):
    return isinstance(obj, list) and all([_is_face_part_dict(x) for x in obj])


def _is_face_part_list_list(obj):
    return isinstance(obj, list) and all([_is_face_part_list(x) for x in obj])


# ===========================================================
# Chernoff face
# ===========================================================
def chernoff_face(data,
                  n_rows: Optional[int] = None,
                  n_columns: Optional[int] = None,
                  make_symmetric: bool = True,
                  color_mapper: Optional[matplotlib.colors.LinearSegmentedColormap]=None,
                  **kwargs):
    """Makes Chernoff face diagrams.

    :type data: Any
    :param data: Data to be plotted.

    :type n_rows: int|None
    :param n_rows: Number of rows.

    :type n_columns: int|None
    :param n_columns: Number of columns.

    :type make_symmetric: bool
    :param make_symmetric: The faces can be made symmetric for shorter faces.

    :type color_mapper: matplotlib.colors.LinearSegmentedColormap|None
    :param color_mapper: Color mapping object.

    :type kwargs: **dict
    :param kwargs: Arguments for matplotlib.pyplot.figure .

    :rtype fig: matplotlib.figure.Figure
    :return fig: A figure (object of the class matplotlib.figure.Figure .)
    """

    # If numpy array
    if isinstance(data, numpy.ndarray) and data.ndim == 2:
        return chernoff_face(data.tolist(),
                             n_rows=n_rows,
                             n_columns=n_columns,
                             make_symmetric=make_symmetric,
                             color_mapper=color_mapper,
                             **kwargs)

    # Check make_symmetric
    if not isinstance(make_symmetric, bool):
        raise TypeError("""The argument 'make_symmetric' is expected to be a Boolean""")

    if _is_face_part_dict_list(data) or _is_face_part_list_list(data):

        myNRows = n_rows
        myNCols = n_columns

        if myNRows is None and myNCols is None:

            myNRows = math.ceil(math.sqrt(len(data)))
            myNCols = math.ceil(len(data) / myNRows)

        elif myNRows is None and isinstance(myNCols, int) and myNCols > 0:

            myNRows = math.ceil(len(data) / myNCols)

        elif myNCols is None and isinstance(myNRows, int) and myNRows > 0:

            myNCols = math.ceil(len(data) / myNRows)

        if isinstance(myNRows, int) and myNRows > 0 and isinstance(myNCols, int) and myNCols > 0:

            resFig = _chernoff_faces_figure(data=data,
                                            n_rows=myNRows,
                                            n_columns=myNCols,
                                            make_symmetric=make_symmetric,
                                            color_mapper=color_mapper,
                                            **kwargs)

        else:
            raise TypeError("The arguments n_rows and n_columns are expected to be positive integers or None.")

    elif _is_face_part_dict(data):

        resFig = single_chernoff_face(data=data,
                                      make_symmetric=make_symmetric,
                                      color_mapper=color_mapper,
                                      figure=None, axes=None, location=None,
                                      **kwargs)

    else:
        raise TypeError("Unknown type for first argument, 'data'.")

    return resFig


# ===========================================================
# Chernoff faces figure
# ===========================================================
def _chernoff_faces_figure(data,
                           n_rows=None,
                           n_columns=None,
                           make_symmetric: bool = True,
                           color_mapper=None,
                           **kwargs):
    """Makes a figure with random mandalas."""

    fig: matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)

    k = 0
    for i in range(n_rows):
        for j in range(n_columns):
            locationSpec = (n_rows, n_columns, i * n_columns + j + 1)

            if k >= len(data):
                break

            single_chernoff_face(
                data=data[k],
                rescale_values=False,
                make_symmetric=make_symmetric,
                color_mapper=color_mapper,
                figure=fig,
                axes=None,
                location=locationSpec
            )
            k += 1

    return fig


# ===========================================================
# Figure to data
# ===========================================================
# Following documentation here:
#    https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
def figure_to_image(figure):
    """Convert a Matplotlib figure into a PIL image.

    :param figure: A figure (object of the class matplotlib.figure.Figure .)
    :return res: A Python Imaging Library (PIL) image.
    """
    canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(figure)

    canvas.draw()
    rgba = numpy.asarray(canvas.buffer_rgba())
    res = PIL.Image.fromarray(rgba)
    res = res.convert('RGB')

    return res
