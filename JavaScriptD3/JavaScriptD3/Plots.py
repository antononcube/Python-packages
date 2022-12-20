from JavaScriptD3.CodeSnippets import CodeSnippets
from JavaScriptD3.CodeSnippets import process_margins
from JavaScriptD3.CodeSnippets import process_grid_lines

import json
import numpy
from IPython.display import clear_output, display, HTML, Javascript


# ============================================================
# Predicates
# ============================================================

def is_list_of_dicts(obj):
    if not isinstance(obj, list):
        return False
    for a in obj:
        if not isinstance(a, dict):
            return False
    return True


def is_list_of_date_value_pairs(obj):
    if not isinstance(obj, list):
        return False
    for a in obj:
        if not isinstance(a, list) and len(a) == 2:
            return False
        if not isinstance(a[0], str) and isinstance(a[1], int | float):
            return False
    return True


# ============================================================
# ListPlot
# ============================================================

def _js_d3_list_plot(data,
                     background="white",
                     color="steelblue",
                     width=600,
                     height=400,
                     title='',
                     x_axis_label='',
                     y_axis_label='',
                     grid_lines=False,
                     margins=None,
                     legends=False,
                     single_dataset_code='',
                     multi_dataset_code='',
                     data_scales_and_axes_code='',
                     fmt="jupyter"):
    """
    Generic list plot
    ----------------------------------
    :param data: Data to plotted.
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
    :param single_dataset_code: Code for single dataset.
    :param multi_dataset_code: Code for multiple datasets.
    :param data_scales_and_axes_code: Code for the data, scales, and axes.
    :param fmt: Format, one of "html", "jupyter", or "script".
    :return: JavaScript code or HTML code.
    """
    # Type checking and coercion
    dataLocal = data
    if isinstance(dataLocal, numpy.ndarray):
        if len(dataLocal.shape) == 1:
            dataLocal = [{"x": k, "y": dataLocal[k]} for k in range(0, dataLocal.shape[0])]
        elif len(dataLocal.shape) == 2:
            dataLocal = [{"x": dataLocal[k, 0], "y": dataLocal[k, 1]} for k in range(0, dataLocal.shape[0])]

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
        jsPlotMiddle = multi_dataset_code
    else:
        jsPlotMiddle = single_dataset_code

    # Chose to add legend code fragment or not
    maxGroupChars = len("all")
    if hasGroups:
        maxGroupChars = max([len(x) for x in [r["group"] for r in data]])

    if isinstance(legends, bool) and legends or legends is None and hasGroups:
        marginsLocal["right"] = max(marginsLocal["right"], (maxGroupChars + 4) * 12)
        jsPlotMiddle = jsPlotMiddle + "\n" + cs.get_legend_code()

    # Stencil
    jsScatterPlot = cs.get_plot_starting_code(fmt=fmt) + "\n" + \
                    cs.get_plot_margins_and_labels_code(fmt=fmt) + "\n" + \
                    cs.get_plot_data_scales_and_axes_code(n_x_ticks=gridLinesLocal[0],
                                                          n_y_ticks=gridLinesLocal[1],
                                                          code_fragment=data_scales_and_axes_code) + "\n" + \
                    jsPlotMiddle + "\n" + \
                    cs.get_plot_ending_code(fmt=fmt)

    # Concrete parameters
    res = (jsScatterPlot
           .replace('$DATA', jsData)
           .replace('$BACKGROUND_COLOR', '"' + background + '"')
           .replace('$POINT_COLOR', '"' + color + '"')
           .replace('$LINE_COLOR', '"' + color + '"')
           .replace('$WIDTH', str(width))
           .replace('$HEIGHT', str(height))
           .replace('$TITLE', '"' + title + '"')
           .replace('$X_AXIS_LABEL', '"' + x_axis_label + '"')
           .replace('$Y_AXIS_LABEL', '"' + y_axis_label + '"')
           .replace('$MARGINS', json.dumps(marginsLocal))
           .replace('$LEGEND_X_POS', 'width + 3*12')
           .replace('$LEGEND_Y_POS', '0')
           .replace('$LEGEND_Y_GAP', '25'))

    if fmt.lower() == "html":
        res = res.replace('element.get(0)', '"#my_dataviz"')
    elif fmt.lower() == "jupyter":
        res = display(Javascript(res))

    return res


# ============================================================
# ListPlot
# ============================================================

def js_d3_list_plot(data,
                    background="white",
                    color="steelblue",
                    width=600,
                    height=400,
                    title='',
                    x_axis_label='',
                    y_axis_label='',
                    grid_lines=False,
                    margins=None,
                    legends=False,
                    fmt="jupyter"):
    """
    List plot (or scatter plot)
    --------------------------------
    :param data: Data to plotted.
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
    cs = CodeSnippets()

    return _js_d3_list_plot(
        data=data,
        background=background,
        color=color,
        width=width,
        height=height,
        title=title,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        grid_lines=grid_lines,
        margins=margins,
        legends=legends,
        single_dataset_code=cs.get_scatter_plot_part(),
        multi_dataset_code=cs.get_multi_scatter_plot_part(),
        data_scales_and_axes_code=cs.get_plot_data_scales_and_axes_code(),
        fmt=fmt
    )


# ============================================================
# ListLinePlot
# ============================================================
def js_d3_list_line_plot(data,
                         background="white",
                         color="steelblue",
                         width=600,
                         height=400,
                         title='',
                         x_axis_label='',
                         y_axis_label='',
                         grid_lines=False,
                         margins=None,
                         legends=False,
                         fmt="jupyter"):
    """
    List line plot
    ------------------------------------
    :param data: Data to plotted.
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
    cs = CodeSnippets()

    return _js_d3_list_plot(
        data=data,
        background=background,
        color=color,
        width=width,
        height=height,
        title=title,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        grid_lines=grid_lines,
        margins=margins,
        legends=legends,
        single_dataset_code=cs.get_path_plot_part(),
        multi_dataset_code=cs.get_multi_path_plot_part(),
        data_scales_and_axes_code=cs.get_plot_data_scales_and_axes_code(),
        fmt=fmt
    )


# ============================================================
# DateListPlot
# ============================================================


def js_d3_date_list_plot(data,
                         background="white",
                         color="steelblue",
                         width=600,
                         height=400,
                         title='',
                         date_axis_label='',
                         value_axis_label='',
                         time_parse_spec='%Y-%m-%d',
                         grid_lines=False,
                         margins=None,
                         legends=False,
                         fmt="jupyter"):
    """
    Generic list plot
    ----------------------------------
    :param data: Data to plotted.
    :param background: Background color.
    :param color: Color of the points.
    :param width: Width of the plot.
    :param height: Height of the plot.
    :param title: Plot title.
    :param date_axis_label: Date-axis label.
    :param value_axis_label: Value-axis label.
    :param time_parse_spec: Time parse spec (for D3.js.)
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
            dataLocal = [{"date": k, "value": dataLocal[k]} for k in range(0, dataLocal.shape[0])]
        elif len(dataLocal.shape) == 2:
            dataLocal = [{"date": dataLocal[k, 0], "value": dataLocal[k, 1]} for k in range(0, dataLocal.shape[0])]
    elif is_list_of_date_value_pairs(dataLocal):
        dataLocal = [{"date": dataLocal[k][0], "value": dataLocal[k][1]} for k in range(0, len(dataLocal))]

    if not is_list_of_dicts(dataLocal):
        raise TypeError("The first argument is expected to be coercible to numpy.ndarray or a list of dictionaries.")

    cs = CodeSnippets()

    res = _js_d3_list_plot(
        data=dataLocal,
        background=background,
        color=color,
        width=width,
        height=height,
        title=title,
        x_axis_label=date_axis_label,
        y_axis_label=value_axis_label,
        grid_lines=grid_lines,
        margins=margins,
        legends=legends,
        single_dataset_code=cs.get_path_plot_part(),
        multi_dataset_code=cs.get_multi_path_plot_part(),
        data_scales_and_axes_code=cs.get_plot_date_data_and_scales(),
        fmt="script"
    )

    res = res.replace('$TIME_PARSE_SPEC', '"' + time_parse_spec + '"')

    if fmt.lower() == "html":
        res = res.replace('element.get(0)', '"#my_dataviz"')
    elif fmt.lower() == "jupyter":
        res = display(Javascript(res))

    return res
