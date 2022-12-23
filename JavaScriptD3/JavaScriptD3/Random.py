from JavaScriptD3.CodeSnippets import CodeSnippets
from JavaScriptD3.CodeSnippets import wrap_it
from JavaScriptD3.Plots import js_d3_list_line_plot
from JavaScriptD3.Plots import is_list_of_dicts

import json
import numpy
import math
import random
from IPython.display import clear_output, display, HTML, Javascript


# ===========================================================
# Random seed segment
# ===========================================================
def _make_seed_segment(
        radius: float = 10.,
        angle=numpy.pi / 6,
        number_of_seed_elements: int = 10,
        symmetric_seed=True):
    ang = angle
    if symmetric_seed:
        ang = ang / 2

    t1 = [radius * r * math.cos(ang) for r in numpy.arange(0, 1, 1 / number_of_seed_elements)]
    t2 = [radius * r * math.sin(ang) for r in numpy.arange(0, 1, 1 / number_of_seed_elements)]

    b = [(radius * r, 0) for r in numpy.arange(0, 1, 1 / number_of_seed_elements)]

    t = list(zip(t1, t2)) + b
    seed_points = random.sample(t, len(t))

    if symmetric_seed:
        sym_seed_points = [(x[0], -x[1]) for x in seed_points]
        seed_points = seed_points + sym_seed_points

    return seed_points


# ============================================================
# Mandala
# ============================================================
def mandala(radius=1,
            rotational_symmetry_order=6,
            number_of_seed_elements=None,
            symmetric_seed=True):
    ang = 2 * numpy.pi / rotational_symmetry_order

    # Make seed segment
    nodes = _make_seed_segment(radius=radius,
                               angle=ang,
                               number_of_seed_elements=number_of_seed_elements,
                               symmetric_seed=symmetric_seed)

    nodes = numpy.array(nodes).transpose()

    # Rotation matrix
    rotMat = [[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]]

    # First segment
    randomMandala = [{"group": str(0), "x": nodes[0, i], "y": nodes[1, i]} for i in range(nodes.shape[1])]

    # Incremental rotation and plotting
    for i in range(1, math.floor(2 * numpy.pi / ang)):
        nodes = numpy.dot(rotMat, nodes)
        nodeDicts = [{"group": str(i), "x": nodes[0, j], "y": nodes[1, j]} for j in range(nodes.shape[1])]
        if rotational_symmetry_order % 2 == 0 and i % 2 == 1:
             nodeDicts.reverse()
        randomMandala = randomMandala + nodeDicts

    return randomMandala


# ============================================================
# RandomMandala
# ============================================================

def js_d3_random_mandala(radius=1,
                         rotational_symmetry_order=6,
                         number_of_seed_elements=None,
                         connecting_function="curveBasis",
                         symmetric_seed=True,
                         color="steelblue",
                         stroke_width=None,
                         fill=None,
                         background="white",
                         width=300,
                         height=300,
                         title='',
                         x_axis_label='',
                         y_axis_label='',
                         grid_lines=False,
                         margins=10,
                         legends=False,
                         axes=False,
                         count=1,
                         fmt="jupyter"):
    """
    Random mandala
    ----------------------------------
    :param radius: Radius.
    :param rotational_symmetry_order: Rotational symmetry order.
    :param number_of_seed_elements: Number of seed elements.
    :param connecting_function: Connecting function.
    :param symmetric_seed: Should the seed be symmetric or not?
    :param background: Background color.
    :param color:Color of the curves drawn.
    :param stroke_width: Stroke width (for curves drawn.)
    :param fill: Color to do curve filling with.
    :param width: Width of the plot.
    :param height: Height of the plot.
    :param title: Plot title.
    :param x_axis_label: X-axis label.
    :param y_axis_label: Y-axis label.
    :param grid_lines: Grid lines spec. If True automatic grid lines spec made.
    :param margins: Margins spec: an integer or dictionary with keys "top", "bottom", "left", "right".
    :param legends: Should legends be placed or not?
    :param axes: Should axes be drawn or not?
    :param count: Number of mandalas to be plotted.
    :param fmt: Format, one of "html", "jupyter", or "script".
    :return: JavaScript code or HTML code.
    """

    # --------------------------------------------------------
    # Process options
    # --------------------------------------------------------

    # Number of seed elements
    numberOfSeedElements = number_of_seed_elements
    if numberOfSeedElements is None:
        numberOfSeedElements = random.sample(range(4, 10), 1)[0]

    # Stroke
    strokeLocal = color
    if strokeLocal is None:
        strokeLocal = "gray"

    # Stroke width
    if stroke_width is None:
        strokeWidth = 1.5

    # Fill
    fillLocal = fill
    if fillLocal is None:
        fillLocal = "rgb(100,100,100)"

    # --------------------------------------------------------
    # Random mandala
    # --------------------------------------------------------
    jsCode = ""
    for i in range(count):
        randomMandala = mandala(radius=radius,
                                rotational_symmetry_order=rotational_symmetry_order,
                                number_of_seed_elements=numberOfSeedElements,
                                symmetric_seed=symmetric_seed)

        jsCode = jsCode + js_d3_list_line_plot(
            data=randomMandala,
            background=background,
            color=color,
            width=width,
            height=height,
            title=title,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            grid_lines=grid_lines,
            margins=margins,
            legends=False,
            axes=axes,
            fmt="asis"
        )

    # --------------------------------------------------------
    # Finishing
    # --------------------------------------------------------
    jsCode = (jsCode
              .replace('.attr("stroke-width", 1.5)',
                       '.attr("stroke-width", ' + str(strokeWidth) + ').attr("fill", "' + fillLocal + '")')
              .replace('.attr("stroke", function(d){ return myColor(d[0]) })', '.attr("stroke", "' + strokeLocal + '")')
              .replace('.y(function(d) { return y(+d.y); })',
                       '.y(function(d) { return y(+d.y); }).curve(d3.' + connecting_function + ')'))

    return wrap_it(code=jsCode, fmt=fmt)
