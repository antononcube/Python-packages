from JavaScriptD3.CodeSnippets import CodeSnippets
from JavaScriptD3.CodeSnippets import process_margins
from JavaScriptD3.CodeSnippets import process_grid_lines
from JavaScriptD3.Plots import is_list_of_dicts

import json
import numpy
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
        jsPlotMiddle = cs.get_plot_data_and_scales_code(n_x_ticks=gridLinesLocal[0],
                                                        n_y_ticks=gridLinesLocal[1],
                                                        code_fragment=cs.get_multi_bar_chart_part())
    else:
        jsPlotMiddle = cs.get_plot_data_and_scales_code(n_x_ticks=gridLinesLocal[0],
                                                        n_y_ticks=gridLinesLocal[1],
                                                        code_fragment=cs.get_bar_chart_part())

    # Chose to add legend code fragment or not
    maxGroupChars = len("all")
    if hasGroups:
        maxGroupChars = max([len(x) for x in [r["group"] for r in data]])

    if isinstance(legends, bool) and legends or legends is None and hasGroups:
        marginsLocal["right"] = max(marginsLocal["right"], (maxGroupChars + 4) * 12)
        jsPlotMiddle = jsPlotMiddle + "\n" + cs.get_legend_code().replace('return o.group;', "return o.variable;")

    # Stencil
    jsChart = cs.get_plot_starting_code(fmt) + "\n" + cs.get_plot_margins_and_labels_code(fmt) + "\n" + \
              jsPlotMiddle + "\n" + cs.get_plot_ending_code(fmt)

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

    if fmt.lower() == "html":
        res = res.replace('element.get(0)', '"#my_dataviz"')
    elif fmt.lower() == "jupyter":
        res = display(Javascript(res))

    return res
