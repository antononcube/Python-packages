import math
from typing import Optional

import PIL
import matplotlib
import matplotlib.cm
import matplotlib.figure
import matplotlib.pyplot
import numpy
import pandas.core.frame
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


def _is_title_list(obj, expected_len: int):
    return isinstance(obj, (list, tuple)) and len(obj) == expected_len and all([isinstance(x, str) for x in obj])


# ===========================================================
# Chernoff face
# ===========================================================
def chernoff_face(data,
                  n_rows: Optional[int] = None,
                  n_columns: Optional[int] = None,
                  make_symmetric: bool = True,
                  color_mapper: Optional[matplotlib.colors.LinearSegmentedColormap] = None,
                  long_face: bool = False,
                  titles=None,
                  figure: Optional[matplotlib.figure.Figure] = None,
                  location=None,
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

    :type long_face: bool
    :param long_face: Should the face be longer of wider.

    :type titles: list|tuple
    :param titles: Titles for the each of the face in face collection.

    :type figure: matplotlib.figure.Figure|None
    :param figure: Figure to draw the Chernoff faces diagrams into.

    :type location: tuple|None
    :param location: Location spec to add the Chernoff face to.

    :type kwargs: **dict
    :param kwargs: Arguments for matplotlib.pyplot.figure .

    :rtype resFig: matplotlib.figure.Figure
    :return resFig: A figure (object of the class matplotlib.figure.Figure .)
    """

    # If numpy array
    if isinstance(data, numpy.ndarray) and data.ndim == 2:
        return chernoff_face(data.tolist(),
                             n_rows=n_rows,
                             n_columns=n_columns,
                             make_symmetric=make_symmetric,
                             color_mapper=color_mapper,
                             long_face=long_face,
                             titles=titles,
                             figure=figure,
                             **kwargs)

    # If a data frame
    if isinstance(data, pandas.core.frame.DataFrame):
        num_cols = list(data.select_dtypes('number'))

        data2 = data[[*num_cols]].to_numpy()
        # data2 = variables_rescale(data2)

        titles2 = titles
        if titles2 is None:
            cat_cols = list(data.select_dtypes(exclude=["number"]))
            if len(cat_cols) > 0:
                titles2 = data[cat_cols[0]].to_list()
                if not all([isinstance(x, str) for x in titles2]):
                    titles2 = None

        return chernoff_face(data2,
                             n_rows=n_rows,
                             n_columns=n_columns,
                             make_symmetric=make_symmetric,
                             color_mapper=color_mapper,
                             long_face=long_face,
                             titles=titles2,
                             figure=figure,
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
                                            long_face=long_face,
                                            titles=titles,
                                            figure=figure,
                                            **kwargs)

        else:
            raise TypeError("The arguments n_rows and n_columns are expected to be positive integers or None.")

    elif _is_face_part_dict(data) or _is_face_part_list(data):

        resFig = single_chernoff_face(data=data,
                                      make_symmetric=make_symmetric,
                                      color_mapper=color_mapper,
                                      long_face=long_face,
                                      figure=figure,
                                      axes=None,
                                      location=location,
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
                           long_face=True,
                           titles=None,
                           figure=None,
                           **kwargs):
    """Makes a figure with Chernoff faces."""

    # Titles argument processing
    myTitles = titles
    if myTitles is not None:
        expected_len = None
        if _is_face_part_list_list(data) or _is_face_part_dict_list(data):
            expected_len = len(data)
        if isinstance(myTitles, pandas.core.frame.DataFrame):
            myTitles = myTitles.to_list()

        if myTitles is not None and not _is_title_list(myTitles, expected_len):
            raise TypeError(
                "The argument 'titles' is expected to be list of strings with length " + str(expected_len) + ".")

    fig = figure
    if fig is None:
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
                long_face=long_face,
                figure=fig,
                axes=None,
                location=locationSpec
            )

            if myTitles is not None:
                ax = fig.gca()
                ax.set_title(myTitles[k])

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
