from JavaScriptD3.CodeSnippets import CodeSnippets
from JavaScriptD3.CodeSnippets import process_margins
from JavaScriptD3.CodeSnippets import process_grid_lines
from JavaScriptD3.CodeSnippets import wrap_it
from JavaScriptD3.Plots import is_list_of_dicts
from JavaScriptD3.Plots import is_list_of_numeric_arrays

import json
import numpy
import pandas
from IPython.display import clear_output, display, HTML, Javascript


# ============================================================
# BarChart
# ============================================================

def js_d3_bar_chart(data,
                    background="white",
                    color="steelblue",
                    width=600,
                    height=400,
                    title='',
                    x_axis_label='',
                    y_axis_label='',
                    grid_lines=False,
                    margins=None,
                    legends=None,
                    fmt="jupyter"):
    """
    Bar chart
    -------------------------------
    :param data: Data to charted.
    :param background: Background color.
    :param color: Color of the points.
    :param width: Width of the plot.
    :param height: Height of the plot.
    :param title: Plot title.
    :param x_axis_label: X-axis label.
    :param y_axis_label: Y-axis label.
    :param grid_lines: Grid lines spec. If True automatic grid lines spec made.
    :param margins: Margins spec: an integer or dictionary with keys "top", "bottom", "left", "right".
    :param legends: Should legends be placed or not?
    :param fmt: Format, one of "html", "jupyter", or "script".
    :return: JavaScript code or HTML code.
    """
    # Type checking and coercion
    dataLocal = data
    if isinstance(dataLocal, numpy.ndarray):
        if len(dataLocal.shape) == 1:
            dataLocal = [{"variable": k, "value": dataLocal[k]} for k in range(0, dataLocal.shape[0])]
        elif len(dataLocal.shape) == 2:
            dataLocal = [{"variable": dataLocal[k, 0], "value": dataLocal[k, 1]} for k in range(0, dataLocal.shape[0])]

    if not is_list_of_dicts(dataLocal):
        raise TypeError("The first argument is expected to be coercible to numpy.ndarray or a list of dictionaries.")

    # Convert to JSON data
    jsData = json.dumps(dataLocal, default=str)

    # Grid lines
    gridLinesLocal = process_grid_lines(grid_lines)

    # Process margins
    marginsLocal = process_margins(margins)

    # Groups
    hasGroups = True
    for d in dataLocal:
        if "group" not in d.keys():
            hasGroups = False
            break

    # Code snippets object
    cs = CodeSnippets()

    # Select code fragment to splice in
    if hasGroups:
        jsChartMiddle = cs.get_plot_data_scales_and_axes_code(n_x_ticks=gridLinesLocal[0],
                                                              n_y_ticks=gridLinesLocal[1],
                                                              code_fragment=cs.get_multi_bar_chart_part())
    else:
        jsChartMiddle = cs.get_plot_data_scales_and_axes_code(n_x_ticks=gridLinesLocal[0],
                                                              n_y_ticks=gridLinesLocal[1],
                                                              code_fragment=cs.get_bar_chart_part())

    # Chose to add legend code fragment or not
    maxGroupChars = len("all")
    if hasGroups:
        maxGroupChars = max([len(x) for x in [r["group"] for r in dataLocal]])

    if isinstance(legends, bool) and legends or legends is None and hasGroups:
        marginsLocal["right"] = max(marginsLocal["right"], (maxGroupChars + 4) * 12)
        jsChartMiddle = jsChartMiddle + "\n" + cs.get_legend_code().replace('return o.group;', "return o.variable;")

    # Stencil
    jsChart = cs.get_plot_margins_and_labels_code(fmt) + "\n" + jsChartMiddle

    # Concrete parameters
    res = (jsChart
           .replace('$DATA', jsData)
           .replace('$BACKGROUND_COLOR', '"' + background + '"')
           .replace('$FILL_COLOR', '"' + color + '"')
           .replace('$WIDTH', str(width))
           .replace('$HEIGHT', str(height))
           .replace('$TITLE', '"' + title + '"')
           .replace('$X_AXIS_LABEL', '"' + x_axis_label + '"')
           .replace('$Y_AXIS_LABEL', '"' + y_axis_label + '"')
           .replace('$MARGINS', json.dumps(marginsLocal))
           .replace('$LEGEND_X_POS', 'width + 3*12')
           .replace('$LEGEND_Y_POS', '0')
           .replace('$LEGEND_Y_GAP', '25'))

    return wrap_it(code=res, fmt=fmt)


# ============================================================
# Histogram
# ============================================================
# The Histogram and BarChart codes have to be refactored.
# (After Histogram for multi-datasets is implemented.)
def js_d3_histogram(data,
                    background="white",
                    color="steelblue",
                    width=600,
                    height=400,
                    title='',
                    x_axis_label='',
                    y_axis_label='',
                    grid_lines=False,
                    margins=None,
                    legends=None,
                    fmt="jupyter"):
    """
    Histogram
    -------------------------------
    :param data: Data to charted.
    :param background: Background color.
    :param color: Color of the points.
    :param width: Width of the plot.
    :param height: Height of the plot.
    :param title: Plot title.
    :param x_axis_label: X-axis label.
    :param y_axis_label: Y-axis label.
    :param grid_lines: Grid lines spec. If True automatic grid lines spec made.
    :param margins: Margins spec: an integer or dictionary with keys "top", "bottom", "left", "right".
    :param legends: Should legends be placed or not?
    :param fmt: Format, one of "html", "jupyter", or "script".
    :return: JavaScript code or HTML code.
    """
    # Type checking and coercion
    dataLocal = data
    if isinstance(dataLocal, numpy.ndarray):
        if len(dataLocal.shape) == 1:
            dataLocal = list(dataLocal.data)
        elif len(dataLocal.shape) > 1:
            dataLocal = None

    if not isinstance(dataLocal, list):
        raise TypeError("The first argument is expected to be coercible to 1D numpy.ndarray.")

    # Convert to JSON data
    jsData = json.dumps(dataLocal, default=str)

    # Grid lines
    gridLinesLocal = process_grid_lines(grid_lines)

    # Process margins
    marginsLocal = process_margins(margins)

    # Groups
    hasGroups = False

    # Code snippets object
    cs = CodeSnippets()

    # Select code fragment to splice in
    if hasGroups:
        jsChartMiddle = cs.get_plot_data_scales_and_axes_code(n_x_ticks=gridLinesLocal[0],
                                                              n_y_ticks=gridLinesLocal[1],
                                                              code_fragment=cs.get_histogram_part())
    else:
        jsChartMiddle = cs.get_plot_data_scales_and_axes_code(n_x_ticks=gridLinesLocal[0],
                                                              n_y_ticks=gridLinesLocal[1],
                                                              code_fragment=cs.get_histogram_part())

    # Chose to add legend code fragment or not
    maxGroupChars = len("all")
    if hasGroups:
        maxGroupChars = max([len(x) for x in [r["group"] for r in dataLocal]])

    if isinstance(legends, bool) and legends or legends is None and hasGroups:
        marginsLocal["right"] = max(marginsLocal["right"], (maxGroupChars + 4) * 12)
        jsChartMiddle = jsChartMiddle + "\n" + cs.get_legend_code().replace('return o.group;', "return o.variable;")

    # Stencil
    jsChart = cs.get_plot_margins_and_labels_code(fmt) + "\n" + jsChartMiddle

    # Concrete parameters
    res = (jsChart
           .replace('$DATA', jsData)
           .replace('$BACKGROUND_COLOR', '"' + background + '"')
           .replace('$FILL_COLOR', '"' + color + '"')
           .replace('$WIDTH', str(width))
           .replace('$HEIGHT', str(height))
           .replace('$TITLE', '"' + title + '"')
           .replace('$X_AXIS_LABEL', '"' + x_axis_label + '"')
           .replace('$Y_AXIS_LABEL', '"' + y_axis_label + '"')
           .replace('$MARGINS', json.dumps(marginsLocal))
           .replace('$LEGEND_X_POS', 'width + 3*12')
           .replace('$LEGEND_Y_POS', '0')
           .replace('$LEGEND_Y_GAP', '25'))

    return wrap_it(code=res, fmt=fmt)


# ============================================================
# BubbleChart
# ============================================================

def js_d3_bubble_chart(data,
                       background="white",
                       color="steelblue",
                       opacity=0.7,
                       width=600,
                       height=400,
                       title='',
                       x_axis_label='',
                       y_axis_label='',
                       grid_lines=False,
                       margins=None,
                       legends=None,
                       tooltip=None,
                       fmt="jupyter"):
    """
    Bubble chart
    -------------------------------
    :param data: Data to charted.
    :param background: Background color.
    :param color: Color of the bubbles. (Single dataset.)
    :param opacity: Opacity of the bubbles.
    :param width: Width of the plot.
    :param height: Height of the plot.
    :param title: Plot title.
    :param x_axis_label: X-axis label.
    :param y_axis_label: Y-axis label.
    :param grid_lines: Grid lines spec. If True automatic grid lines spec made.
    :param margins: Margins spec: an integer or dictionary with keys "top", "bottom", "left", "right".
    :param legends: Should legends be placed or not?
    :param tooltip: Should tooltips be placed or not?
    :param fmt: Format, one of "html", "jupyter", or "script".
    :return: JavaScript code or HTML code.
    """
    # Type checking and coercion
    dataLocal = data
    if is_list_of_numeric_arrays(obj=dataLocal, length=3) or is_list_of_numeric_arrays(obj=dataLocal, length=2):
        dataLocal = numpy.asarray(dataLocal)

    if isinstance(dataLocal, pandas.core.frame.DataFrame):
        dataLocal = list(dataLocal.transpose().to_dict().values())

    if isinstance(dataLocal, numpy.ndarray):
        if len(dataLocal.shape) == 1:
            dataLocal = [{"x": k, "y": dataLocal[k], "z": 1} for k in range(0, dataLocal.shape[0])]
        elif len(dataLocal.shape) == 2 and dataLocal.shape[1] == 2:
            dataLocal = [{"x": dataLocal[k, 0], "y": dataLocal[k, 1], "z": 1} for k in range(0, dataLocal.shape[0])]
        elif len(dataLocal.shape) == 2 and dataLocal.shape[1] == 3:
            dataLocal = [{"x": dataLocal[k, 0], "y": dataLocal[k, 1], "z": dataLocal[k, 2]} for k in
                         range(0, dataLocal.shape[0])]

    if not is_list_of_dicts(dataLocal):
        raise TypeError("The first argument is expected to be coercible to numpy.ndarray or a list of dictionaries.")

    # Convert to JSON data
    jsData = json.dumps(dataLocal, default=str)

    # Grid lines
    gridLinesLocal = process_grid_lines(grid_lines)

    # Process margins
    marginsLocal = process_margins(margins)

    # Groups
    hasGroups = True
    for d in dataLocal:
        if "group" not in d.keys():
            hasGroups = False
            break

    # Code snippets object
    cs = CodeSnippets()

    # Tooltip
    tooltipLocal = hasGroups and tooltip is None or isinstance(tooltip, bool) and tooltip

    # Select code fragment to splice in
    if hasGroups and not tooltipLocal:
        jsChartMiddle = cs.get_plot_data_scales_and_axes_code(n_x_ticks=gridLinesLocal[0],
                                                              n_y_ticks=gridLinesLocal[1],
                                                              code_fragment=cs.get_multi_bubble_chart_part())
    elif tooltipLocal:
        jsChartMiddle = cs.get_plot_data_scales_and_axes_code(n_x_ticks=gridLinesLocal[0],
                                                              n_y_ticks=gridLinesLocal[1],
                                                              code_fragment=cs.get_tooltip_multi_bubble_chart_part())
    else:
        jsChartMiddle = cs.get_plot_data_scales_and_axes_code(n_x_ticks=gridLinesLocal[0],
                                                              n_y_ticks=gridLinesLocal[1],
                                                              code_fragment=cs.get_bubble_chart_part())

    # Chose to add legend code fragment or not
    maxGroupChars = len("all")
    if hasGroups:
        maxGroupChars = max([len(str(x)) for x in [r["group"] for r in dataLocal]])

    if isinstance(legends, bool) and legends or legends is None and hasGroups:
        marginsLocal["right"] = max(marginsLocal["right"], (maxGroupChars + 4) * 12)
        jsChartMiddle = jsChartMiddle + "\n" + cs.get_legend_code()

    # Stencil
    jsChart = cs.get_plot_preparation_code(fmt, gridLinesLocal[0], gridLinesLocal[1]) + "\n" + jsChartMiddle

    # Concrete parameters
    res = (jsChart
           .replace('$DATA', jsData)
           .replace('$BACKGROUND_COLOR', '"' + background + '"')
           .replace('$FILL_COLOR', '"' + color + '"')
           .replace('$OPACITY', '"' + str(opacity) + '"')
           .replace('$WIDTH', str(width))
           .replace('$HEIGHT', str(height))
           .replace('$TITLE', '"' + title + '"')
           .replace('$X_AXIS_LABEL', '"' + x_axis_label + '"')
           .replace('$Y_AXIS_LABEL', '"' + y_axis_label + '"')
           .replace('$MARGINS', json.dumps(marginsLocal))
           .replace('$LEGEND_X_POS', 'width + 3*12')
           .replace('$LEGEND_Y_POS', '0')
           .replace('$LEGEND_Y_GAP', '25'))

    return wrap_it(code=res, fmt=fmt)
