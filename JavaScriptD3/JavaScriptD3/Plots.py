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
                     fmt="jupyter"):
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
    jsData = json.dumps(dataLocal)

    # Grid lines
    gridLinesLocal = process_grid_lines(grid_lines)

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
    if isinstance(legends, bool) and legends or legends is None and hasGroups:
        jsPlotMiddle = jsPlotMiddle + "\n" + cs.get_legend_code()

    # Stencil
    jsScatterPlot = cs.get_plot_preparation_code(fmt, gridLinesLocal[0], gridLinesLocal[1]) + "\n" + \
                    jsPlotMiddle + "\n" + cs.get_plot_ending_code(fmt)

    # Concrete parameters
    marginsLocal = process_margins(margins)

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
    cs = CodeSnippets()

    return _js_d3_list_plot(
        data=data,
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
    cs = CodeSnippets()

    return _js_d3_list_plot(
        data=data,
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
        fmt=fmt
    )
