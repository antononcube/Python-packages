import re
from typing import Any, Union, Optional

import matplotlib
import matplotlib.backends.backend_agg
import matplotlib.colors
import matplotlib.patches as mpatches
import matplotlib.pyplot
import numpy
# ===========================================================
# Utilities
# ===========================================================
import pandas.core.frame


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


def _is_float(element: Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


# ===========================================================
# Rescaling
# ===========================================================
def rescale(arr, xmin=None, xmax=None, vmin: float = 0, vmax: float = 1):
    mxmin = xmin
    mxmax = xmax
    if xmin is None and xmax is None:
        if isinstance(arr, (list, tuple, numpy.ndarray)):
            mxmin = min(arr)
            mxmax = max(arr)
        else:
            raise TypeError(
                """If the second and third arguments are None the first argument is expected to be a list or array""")

    if mxmax - mxmin == 0:
        return arr

    if isinstance(arr, (list, tuple, numpy.ndarray)):
        res = [(x - mxmin) / (mxmax - mxmin) * (vmax - vmin) + vmin for x in arr]
    else:
        res = (arr - mxmin) / (mxmax - mxmin) * (vmax - vmin) + vmin
    return res


def variables_rescale(data):
    """Variables rescaling.

    :type data: list|numpy.ndarray|pandas.core.frame.DataFrame
    :param data: Data that can be coerced into a two dimensional array the columns of which are rescaled.
    """
    if isinstance(data, list):

        return variables_rescale(numpy.asarray(data))

    elif isinstance(data, pandas.core.frame.DataFrame):

        numCols = data.select_dtypes("number")
        data2 = data[[*numCols]].apply(lambda x: rescale(list(x)), axis=0)

        catCols = data.select_dtypes(exclude="number")

        if len(catCols) == 0:
            return data2
        else:
            return pandas.concat([data[[*catCols]].reset_index(drop=True), data2], axis=1)

    elif isinstance(data, numpy.ndarray) or data.ndim != 2:

        arr2 = data.transpose()
        arr2 = [rescale(x) for x in arr2]
        arr2 = numpy.asarray(arr2).transpose()

        return arr2

    else:
        raise TypeError("The first argument is expected to be coercible into a two dimensional array.")


# ===========================================================
# Default parameters
# ===========================================================
def default_chernoff_face_parameters():
    return {"FaceSize": 0.5,
            "ForeheadShape": 0.5, "EyesVerticalPosition": 0.5,
            "EyeSize": 0.5, "EyeSlant": 0.5, "LeftEyebrowSlant": 0.5,
            "LeftIris": 0.5, "NoseLength": 0.5, "MouthSmile": 0.5,
            "LeftEyebrowTrim": 0.5, "LeftEyebrowRaising": 0.5,
            "MouthTwist": 0.5, "MouthWidth": 0.5,
            "RightEyebrowTrim": 0.5, "RightEyebrowRaising": 0.5,
            "RightEyebrowSlant": 0.5, "RightIris": 0.5,
            "FaceColor": None, "IrisColor": None,
            "NoseColor": None, "MouthColor": None,
            "EyeBallColor": None, "MakeSymmetric": True}


def chernoff_face_parts_parameters():
    res = {k: v for (k, v) in default_chernoff_face_parameters().items()
           if not (bool(re.search("Color", k)) or bool(re.search("Symmetric", k)))}
    return res


# ===========================================================
# Make symmetric Chernoff face parts
# ===========================================================

def make_symmetric_chernoff_face_parameters(params: dict, defaultParams: dict):
    symPairs = [["LeftEyebrowTrim", "RightEyebrowTrim", lambda x: x],
                ["LeftEyebrowRaising", "RightEyebrowRaising", lambda x: x],
                ["LeftEyebrowSlant", "RightEyebrowSlant", lambda x: x],
                ["LeftIris", "RightIris", lambda x: 1 - x]]
    res = {}
    for (p1, p2, f) in symPairs:
        if p1 in params and p2 not in params:
            res = {**res, p2: f(params[p1])}
        elif p1 not in params and p2 in params:
            res = {**res, p1: f(params[p2])}

    res = {**defaultParams, **params, **res}

    return res


# ===========================================================
# Chernoff face parts
# ===========================================================

def mouth_curve(mouthWidth, mouthColor, faceColor, a, b, c, axes=None):
    # Build the polygon and add it to the axes
    xCoords = rescale(list(range(0, 21)), 0, 20, - mouthWidth / 2, mouthWidth / 2)
    points = [[x, a * x ** 2 + b * x + c] for x in xCoords]
    points = numpy.asarray(points)
    # poly = mpatches.Polygon(points, closed=True, **kwargs2)
    # axes.add_patch(poly)
    # # Plot border lines
    axes.plot(points.T[0], points.T[1], color=mouthColor)
    return axes


def nose_patch(noseLength, noseColor, faceColor, edgecolor="0.2", axes=None):
    # Build the polygon and add it to the axes
    points = [[0.012, 0], [-0.012, 0], [-0.1, -noseLength], [0.1, -noseLength]]
    points = numpy.asarray(points)
    if noseColor != faceColor:
        poly = mpatches.Polygon(points, closed=True, color=noseColor)
        axes.add_patch(poly)
        # Plot border lines
        axes.plot(points.T[0], points.T[1], color=edgecolor)
    else:
        axes.plot(points.T[0], points.T[1], color=edgecolor)

    return axes


def left_eyebrow(eyebrLeftTrim, eyebrRaiseLeft, eyebrSlantLeft, edgecolor="0.2", axes=None):
    # build the polygon and add it to the axes
    th1 = numpy.pi / 2 - (eyebrLeftTrim * numpy.pi) / 6
    th1 = th1 / (2 * numpy.pi) * 360

    th2 = numpy.pi / 2 + (eyebrLeftTrim * numpy.pi) / 6
    th2 = th2 / (2 * numpy.pi) * 360

    eyebrow = mpatches.Arc(xy=(-0.5, -0.2),
                           height=2 * 0.7, width=2 * eyebrRaiseLeft,
                           theta1=th1, theta2=th2,
                           angle=eyebrSlantLeft / (2 * numpy.pi) * 360,
                           fill=False,
                           edgecolor=edgecolor)
    axes.add_patch(eyebrow)

    return axes


def right_eyebrow(eyebrRightTrim, eyebrRaiseRight, eyebrSlantRight, edgecolor="0.2", axes=None):
    # build the polygon and add it to the axes
    th1 = numpy.pi / 2 - (eyebrRightTrim * numpy.pi) / 6
    th1 = th1 / (2 * numpy.pi) * 360

    th2 = numpy.pi / 2 + (eyebrRightTrim * numpy.pi) / 6
    th2 = th2 / (2 * numpy.pi) * 360

    eyebrow = mpatches.Arc(xy=(0.5, -0.2),
                           height=2 * 0.7, width=2 * eyebrRaiseRight,
                           theta1=th1, theta2=th2,
                           angle=eyebrSlantRight / (2 * numpy.pi) * 360,
                           fill=False,
                           edgecolor=edgecolor)
    axes.add_patch(eyebrow)

    return axes


def left_eye(eyeSize, eyeBallsColor, irisColor, leftIrisOffset, angle, edgecolor="0.2", axes=None):
    # build the polygon and add it to the axes
    eyeball = mpatches.Ellipse(xy=(-0.5, 0),
                               height=2 * 0.2 * eyeSize, width=2 * 0.4 * eyeSize,
                               angle=angle,
                               facecolor=eyeBallsColor, edgecolor=edgecolor)
    axes.add_patch(eyeball)

    iris = mpatches.Circle(xy=(leftIrisOffset, 0.02),
                           radius=0.15 * eyeSize,
                           facecolor=irisColor, edgecolor=None)
    axes.add_patch(iris)

    iris2 = mpatches.Circle(xy=(leftIrisOffset, 0.02),
                            radius=0.05 * eyeSize,
                            facecolor="black", edgecolor=None)
    axes.add_patch(iris2)

    return axes


def right_eye(eyeSize, eyeBallsColor, irisColor, rightIrisOffset, angle, edgecolor="0.2", axes=None):
    # build the polygon and add it to the axes
    eyeball = mpatches.Ellipse(xy=(0.5, 0),
                               height=2 * 0.2 * eyeSize, width=2 * 0.4 * eyeSize,
                               angle=angle,
                               facecolor=eyeBallsColor, edgecolor=edgecolor)
    axes.add_patch(eyeball)

    iris = mpatches.Circle(xy=(rightIrisOffset, 0.02),
                           radius=0.15 * eyeSize,
                           facecolor=irisColor, edgecolor=None)
    axes.add_patch(iris)

    iris2 = mpatches.Circle(xy=(rightIrisOffset, 0.02),
                            radius=0.05 * eyeSize,
                            facecolor="black", edgecolor=None)
    axes.add_patch(iris2)
    return axes


def forehead_patch(points, axes=None, resolution=50, **kwargs):
    # Build the polygon and add it to the axes
    kwargs2 = {k: v for (k, v) in kwargs.items() if k != "edgecolor"}
    poly = mpatches.Polygon(points, closed=True, **kwargs2)
    axes.add_patch(poly)
    # Plot border lines
    axes.plot(points.T[0], points.T[1], color=kwargs["edgecolor"])
    return axes


def bottom_face_patch(center, height, width, theta1, theta2, axes=None, resolution=50, **kwargs):
    # Generate the points of the bottom of the face
    theta = numpy.linspace(numpy.radians(theta1), numpy.radians(theta2), resolution)
    points = numpy.vstack((width * numpy.cos(theta) + center[0],
                           height * numpy.sin(theta) + center[1]))

    # Build the polygon and add it to the axes
    kwargs2 = {k: v for (k, v) in kwargs.items() if k != "edgecolor"}
    poly = mpatches.Polygon(points.T, closed=True, **kwargs2)
    axes.add_patch(poly)

    # Plot face border
    axes.plot(points[0], points[1], color=kwargs["edgecolor"])
    return axes


# ===========================================================
# Chernoff face
# ===========================================================
def single_chernoff_face(data: dict,
                         rescale_values: bool = True,
                         make_symmetric: bool = True,
                         color_mapper: Optional[matplotlib.colors.LinearSegmentedColormap] = None,
                         long_face=True,
                         figure=None,
                         axes=None,
                         location=None,
                         **kwargs):
    """Make a single Chernoff face diagram."""

    # Make vectors dictionaries and delegate
    if _is_face_part_list(data):
        pars = data

        if len(pars) > len(chernoff_face_parts_parameters()):
            pars = pars[0:len(chernoff_face_parts_parameters())]

        if min(pars) < 0 or max(pars) > 1:
            pars = rescale(pars)

        pars = dict(zip(list(chernoff_face_parts_parameters().keys())[0:len(pars)], pars))

        return single_chernoff_face(pars,
                                    rescale_values=False,
                                    make_symmetric=make_symmetric,
                                    color_mapper=color_mapper,
                                    long_face=long_face,
                                    figure=figure, axes=axes, location=location)

    # Figure
    fig = figure
    if figure is None:
        fig: matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)

    # Location spec
    locationSpec = location
    if location is None:
        locationSpec = (1, 1, 1)

    # Axes spec
    ax = axes
    if axes is None:
        ax = fig.add_subplot(*locationSpec)

    # Process parameters
    pars = data

    # Make symmetric
    if make_symmetric:
        pars = make_symmetric_chernoff_face_parameters(pars, chernoff_face_parts_parameters())

    # Merge with all parameters
    pars = {**default_chernoff_face_parameters(), **pars}

    # Rescaling
    if rescale_values:
        scaledPars = {k: v for (k, v) in pars.items() if k in chernoff_face_parts_parameters()}
        scaledPars = dict(zip(scaledPars.keys(), rescale(list(scaledPars.values()))))
        pars = {**pars, **scaledPars}

    # Colors
    colorParts = {k: v for (k, v) in pars.items()
                  if k in {"FaceColor", "IrisColor", "NoseColor", "MouthColor", "EyeBallColor"} and v is not None}

    if color_mapper is None:
        pars = {**pars, "FaceColor": "white", "IrisColor": "0.85",
                "NoseColor": None, "MouthColor": "black",
                "EyeBallColor": "white"}
        pars = {**pars, **colorParts}
    else:
        pars = chernoff_face_auto_colors(data=pars, color_mapper=color_mapper)

    foreheadTh = 2 * round(rescale(pars["ForeheadShape"], 0, 1, 2, 15))
    # For "historical" purpose 'faceLength' is used.
    # It refers to the original interpretation of "FaceSize" -- that parameter was named "FaceLength".
    faceLength = rescale(pars["FaceSize"], 0, 1, 2, 3)
    eyesVerticalPos = rescale(pars["EyesVerticalPosition"], 0, 1, 0.2, 0.6)

    eyebrLeftTrim = rescale(pars["LeftEyebrowTrim"], 0, 1, 0, 1)
    eyebrRightTrim = rescale(pars["RightEyebrowTrim"], 0, 1, 0, 1)
    eyebrRaiseLeft = rescale(pars["LeftEyebrowRaising"], 0, 1, 0.5, 0.8)
    eyebrRaiseRight = rescale(pars["RightEyebrowRaising"], 0, 1, 0.5, 0.8)
    eyebrSlantLeft = rescale(pars["LeftEyebrowSlant"], 0, 1, -numpy.pi / 6, numpy.pi / 6)
    eyebrSlantRight = rescale(pars["RightEyebrowSlant"], 0, 1, numpy.pi / 6, -numpy.pi / 6)
    eyeSize = rescale(pars["EyeSize"], 0, 1, 0.4, 1)
    eyesSlant = rescale(pars["EyeSlant"], 0, 1, -numpy.pi / 6, numpy.pi / 6)
    leftIrisOffset = rescale(pars["LeftIris"], 0, 1, -0.63, -0.37)
    rightIrisOffset = rescale(pars["RightIris"], 0, 1, 0.37, 0.63)
    noseLength = rescale(pars["NoseLength"], 0, 1, 0.2, 0.65)
    a = rescale(pars["MouthSmile"], 0, 1, -2, 2)
    b = rescale(pars["MouthTwist"], 0, 1, -0.25, 0.25)
    c = -0.8
    mouthWidth = rescale(pars["MouthWidth"], 0, 1, 0.1, 0.7)

    irisColor = pars["IrisColor"]
    eyeBallsColor = pars["EyeBallColor"]
    faceColor = pars["FaceColor"]
    mouthColor = pars["MouthColor"]
    noseColor = pars["NoseColor"]

    if noseColor is None:
        if faceColor == "white":
            noseColor = "white"
        elif _is_float(faceColor):
            noseColor = float(faceColor) - 0.15
            noseColor = 0 if noseColor < 0 else noseColor
            noseColor = str(noseColor)

    # Bottom face part
    if long_face:
        face_width = 1
        face_height = faceLength * (1 - eyesVerticalPos)
    else:
        face_width = faceLength * (1 - eyesVerticalPos)
        face_height = 1

    bottom_face_patch(center=(0., 0),
                      width=face_width,
                      height=face_height,
                      theta1=180, theta2=360,
                      axes=ax, fill=True,
                      color=faceColor, edgecolor='0.3')

    # Forehead
    xCoords = rescale(list(range(0, 21)), 0, 20, -1, 1)
    foreheadPts = [[x * face_width, (1 - x ** foreheadTh) * faceLength * eyesVerticalPos] for x in xCoords]

    forehead_patch(numpy.asarray(foreheadPts), axes=ax, color=faceColor, edgecolor="0.3")

    # Eyes
    left_eye(eyeSize=eyeSize, eyeBallsColor=eyeBallsColor,
             irisColor=irisColor, leftIrisOffset=leftIrisOffset,
             angle=eyesSlant / (2 * numpy.pi) * 360,
             edgecolor="0.3", axes=ax)

    right_eye(eyeSize=eyeSize, eyeBallsColor=eyeBallsColor,
              irisColor=irisColor, rightIrisOffset=rightIrisOffset,
              angle=-eyesSlant / (2 * numpy.pi) * 360,
              edgecolor="0.3", axes=ax)

    # Eyebrows
    left_eyebrow(eyebrLeftTrim=eyebrLeftTrim,
                 eyebrRaiseLeft=eyebrRaiseLeft,
                 eyebrSlantLeft=eyebrSlantLeft,
                 edgecolor="0.3", axes=ax)

    right_eyebrow(eyebrRightTrim=eyebrRightTrim,
                  eyebrRaiseRight=eyebrRaiseRight,
                  eyebrSlantRight=eyebrSlantRight,
                  edgecolor="0.3", axes=ax)

    # Nose
    nose_patch(noseLength=noseLength, noseColor=noseColor, faceColor=faceColor,
               edgecolor="0.3", axes=ax)

    # Mouth
    mouth_curve(mouthWidth=mouthWidth, mouthColor=mouthColor, faceColor=faceColor,
                a=a, b=b, c=c,
                axes=ax)

    # Axes tuning
    ax.set_xlim(-2.1, 2.1)
    # ax.set_ylim(-3, 3)
    ax.set_aspect(aspect=1, adjustable="datalim", anchor="C")
    ax.axis('off')

    # Result
    return fig


# ===========================================================
# Automatic coloring
# ===========================================================

def chernoff_face_auto_colors(data: Union[dict, list],
                              color_mapper: matplotlib.colors.LinearSegmentedColormap):
    """Chernoff face auto colors

    :type data: dict|list
    :param data: Data dictionary.

    :param color_mapper: Color mapping object.
    :return:
    """
    if isinstance(data, dict):
        priorityKeys = ["FaceSize", "ForeheadShape", "EyesVerticalPosition",
                        "EyeSize", "EyeSlant", "LeftEyebrowSlant", "LeftIris"]
        vec = [data[k] for k in priorityKeys]
        res = chernoff_face_auto_colors(vec, color_mapper=color_mapper)
        return {**data, **res}

    if len(data) == 1:
        asc = {"FaceColor": color_mapper(data[0])}
    elif len(data) <= 2:
        asc = {"FaceColor": color_mapper(data[0]),
               "IrisColor": color_mapper(data[1])}
    elif len(data) <= 6:
        asc = {"FaceColor": color_mapper(numpy.mean(data[0:2])),
               "IrisColor": color_mapper(numpy.mean(data[2:len(data)]))}
    else:
        asc = {"FaceColor": color_mapper(numpy.mean(data[0:2])),
               "MouthColor": color_mapper(numpy.mean(data[0:3])),
               "IrisColor": color_mapper(numpy.mean(data[3:6])),
               "NoseColor": color_mapper(numpy.mean(data[6:len(data)]))}

    asc = {**asc, "EyeBallColor": (1, 1, 1, 1)}
    return asc
