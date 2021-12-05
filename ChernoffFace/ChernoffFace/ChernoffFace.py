import re

import PIL
import matplotlib
import matplotlib.backends.backend_agg
import matplotlib.patches as mpatches
import numpy


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
    if isinstance(arr, (list, tuple, numpy.ndarray)):
        res = [(x - mxmin) / (mxmax - mxmin) * (vmax - vmin) + vmin for x in arr]
    else:
        res = (arr - mxmin) / (mxmax - mxmin) * (vmax - vmin) + vmin
    return res


# ===========================================================
# Default parameters
# ===========================================================
def default_chernoff_face_parameters():
    return {"FaceLength": 0.5,
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
    points = numpy.vstack((height * numpy.cos(theta) + center[0],
                           width * numpy.sin(theta) + center[1]))

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
def chernoff_face_for_axes(data: dict, axes):
    pars = data
    pars = default_chernoff_face_parameters() | pars
    scaledPars = {k: v for (k, v) in pars.items() if k in chernoff_face_parts_parameters()}
    scaledPars = dict(zip(scaledPars.keys(), rescale(list(scaledPars.values()))))
    pars = pars | scaledPars

    forheadTh = 2 * round(rescale(pars["ForeheadShape"], 0, 1, 2, 15))
    faceLength = rescale(pars["FaceLength"], 0, 1, 2, 3)
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

    irisColor = "lightblue"
    eyeBallsColor = "white"
    faceColor = "0.9"
    noseColor = "blue"
    mouthColor = "red"

    xCoords = rescale(list(range(0, 21)), 0, 20, -1, 1)
    foreheadPts = [[x, (1 - x ** forheadTh) * faceLength * eyesVerticalPos] for x in xCoords]

    forehead_patch(numpy.asarray(foreheadPts), axes=axes, color=faceColor, edgecolor="0.3")

    bottom_face_patch((0., 0), 1, faceLength * (1 - eyesVerticalPos),
                      theta1=180, theta2=360,
                      axes=axes, fill=True,
                      color=faceColor, edgecolor='0.3')

    left_eye(eyeSize=eyeSize, eyeBallsColor=eyeBallsColor,
             irisColor=irisColor, leftIrisOffset=leftIrisOffset,
             angle=eyesSlant / (2 * numpy.pi) * 360,
             edgecolor="0.3", axes=axes)

    right_eye(eyeSize=eyeSize, eyeBallsColor=eyeBallsColor,
              irisColor=irisColor, rightIrisOffset=rightIrisOffset,
              angle=-eyesSlant / (2 * numpy.pi) * 360,
              edgecolor="0.3", axes=axes)

    nose_patch(noseLength=noseLength, noseColor=noseColor, faceColor=faceColor,
               edgecolor="0.3", axes=axes)

    mouth_curve(mouthWidth=mouthWidth, mouthColor=mouthColor, faceColor=faceColor, a=a, b=b, c=c, axes=axes)
    return pars
