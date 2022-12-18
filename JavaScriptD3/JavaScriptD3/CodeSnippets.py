# ============================================================
# JavaScript plot template parts
# ============================================================

def process_margins(margins):
    marginsLocal = margins
    defaultMargins = {"top": 40, "bottom": 40, "left": 40, "right": 40}
    if marginsLocal is None:
        marginsLocal = defaultMargins
    if not isinstance(marginsLocal, dict):
        raise TypeError("The argument margins is expected to be a dict or None.")
    marginsLocal = defaultMargins | marginsLocal
    return marginsLocal


def process_grid_lines(grid_lines):
    defaultGridLines = (5, 5)

    gridLinesLocal = defaultGridLines
    if isinstance(grid_lines, bool) and not grid_lines:
        gridLinesLocal = (0, 0)
    elif isinstance(grid_lines, bool) and grid_lines:
        gridLinesLocal = defaultGridLines
    elif grid_lines is None:
        gridLinesLocal = defaultGridLines
    elif isinstance(grid_lines, list) and len(grid_lines) == 2:
        gridLinesLocal = grid_lines
    elif isinstance(grid_lines, list) and len(grid_lines) == 1:
        gridLinesLocal = (grid_lines[0], grid_lines[0])
    elif isinstance(grid_lines, int):
        gridLinesLocal = (grid_lines, grid_lines)
    elif isinstance(grid_lines, float):
        gridLinesLocal = (grid_lines.round(), grid_lines.round())

    # More processing is needed to turn, say, (5, None) into (5, 0)

    if gridLinesLocal is not list:
        TypeError(
            "The argument grid-lines is expected to be a non-negative integer," +
            "None, or a two element list of those type of values.")

    return gridLinesLocal


class CodeSnippets:
    # --------------------------------------------------------
    # Plot code snippets
    # --------------------------------------------------------
    _jsPlotStartingHTML = """
    <!DOCTYPE html>
    <head>
        <script src="https://d3js.org/d3.v7.js"></script>
    </head>
    <body>
    
    <div id="my_dataviz"></div>
    
    <script>
    """

    _jsPlotStarting = """
    (function(element) { require(['d3'], function(d3) {
    """

    _jsPlotMarginsAndLabels = """
    // set the dimensions and margins of the graph
    var margin = $MARGINS,
        width = $WIDTH - margin.left - margin.right,
        height = $HEIGHT - margin.top - margin.bottom;
    
    // append the svg object to the body of the page
    var svg = d3
       .select(element.get(0))
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("background", $BACKGROUND_COLOR)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")")
    
    // Obtain title
    var title = $TITLE
    
    if ( title.length > 0 ) {
        svg.append("text")
            .attr("x", (width / 2))
            .attr("y", 0 - (margin.top / 2))
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            //.style("text-decoration", "underline")
            .text(title);
    }
    
    // Obtain x-axis label
    var xAxisLabel = $X_AXIS_LABEL
    var xAxisLabelFontSize = 12
    
    if ( xAxisLabel.length > 0 ) {
        svg.append("text")
            .attr("x", (width / 2))
            .attr("y", height + margin.bottom - xAxisLabelFontSize/2)
            .attr("text-anchor", "middle")
            .style("font-size", xAxisLabelFontSize.toString() + "px")
            .text(xAxisLabel);
    }
    
    // Obtain y-axis label
    var yAxisLabel = $Y_AXIS_LABEL
    var yAxisLabelFontSize = 12
    
    if ( yAxisLabel.length > 0 ) {
        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("x", - (height / 2))
            .attr("y", 0 - margin.left + yAxisLabelFontSize)
            .attr("text-anchor", "middle")
            .style("font-size", yAxisLabelFontSize.toString() + "px")
            .text(yAxisLabel);
    }
    """

    _jsPlotDataAndScales = """
    // Obtain data
    var data = $DATA
    
    var xMin = Math.min.apply(Math, data.map(function(o) { return o.x; }))
    var xMax = Math.max.apply(Math, data.map(function(o) { return o.x; }))
    
    var yMin = Math.min.apply(Math, data.map(function(o) { return o.y; }))
    var yMax = Math.max.apply(Math, data.map(function(o) { return o.y; }))
    
    // X scale and Axis
    var x = d3.scaleLinear()
        .domain([xMin, xMax])         // This is the min and the max of the data: 0 to 100 if percentages
        .range([0, width]);           // This is the corresponding value I want in Pixel
    
    svg
      .append('g')
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
    
    // X scale and Axis
    var y = d3.scaleLinear()
        .domain([yMin, yMax])         // This is the min and the max of the data: 0 to 100 if percentages
        .range([height, 0]);          // This is the corresponding value I want in Pixel
    
    svg
      .append('g')
      .call(d3.axisLeft(y));
    """

    # See https://d3-graph-gallery.com/graph/custom_legend.html
    _jsGroupsLegend = """
    // create a list of keys
    var keys = data.map(function(o) { return o.group; })
    keys = [...new Set(keys)];
    
    // Add one dot in the legend for each name.
    svg.selectAll("mydots")
      .data(keys)
      .enter()
      .append("circle")
        .attr("cx", $LEGEND_X_POS)
        .attr("cy", function(d,i){ return $LEGEND_Y_POS + i*$LEGEND_Y_GAP}) // 100 is where the first dot appears. 25 is the distance between dots
        .attr("r", 6)
        .style("fill", function(d){ return myColor(d)})
    
    // Add one dot in the legend for each name.
    svg.selectAll("mylabels")
      .data(keys)
      .enter()
      .append("text")
        .attr("x", $LEGEND_X_POS + 12)
        .attr("y", function(d,i){ return $LEGEND_Y_POS + i*$LEGEND_Y_GAP}) // 100 is where the first dot appears. 25 is the distance between dots
        .style("fill", function(d){ return myColor(d)})
        .text(function(d){ return d})
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle")
        .style("font-size", "12px")
        .attr("font-family", "Courier")
    """

    _jsPlotEndingHTML = """
    </script>
    </body>
    </html>
    """

    _jsPlotEnding = """
    }) })(element);
    """

    _jsPlotPreparation = _jsPlotStarting + "\n" + _jsPlotMarginsAndLabels + "\n" + _jsPlotDataAndScales

    # --------------------------------------------------------
    # Accessors
    # --------------------------------------------------------

    def get_plot_starting_code(self, fmt='jupyter'):
        if fmt.lower() == 'jupyter':
            return self._jsPlotStarting
        else:
            return self._jsPlotStartingHTML

    def get_plot_ending_code(self, fmt='jupyter'):
        if fmt.lower() == 'jupyter':
            return self._jsPlotEnding
        else:
            return self._jsPlotEndingHTML

    def get_plot_margins_and_labels_code(self, fmt='jupyter'):
        if fmt.lower() == 'jupyter':
            return self._jsPlotMarginsAndLabels
        else:
            return self._jsPlotMarginsAndLabels.replace('element.get(0)', '"#my_dataviz"')

    def get_plot_data_and_scales_code(self, n_x_ticks=0, n_y_ticks=0, code_fragment=None):
        if code_fragment is str:
            res = code_fragment
        else:
            res = self._jsPlotDataAndScales

        if n_x_ticks > 0:
            res = res.replace('.call(d3.axisBottom(x))',
                              ".call(d3.axisBottom(x).ticks(" + str(n_x_ticks) + ").tickSizeInner(-height))")

        if n_y_ticks > 0:
            res = res.replace('.call(d3.axisLeft(y))',
                              ".call(d3.axisLeft(y).ticks(" + str(n_y_ticks) + ").tickSizeInner(-width))")

        return res

    def get_plot_preparation_code(self, fmt='jupyter', n_x_ticks=0, n_y_ticks=0):
        return self.get_plot_starting_code(fmt) + "\n" + \
               self.get_plot_margins_and_labels_code(fmt) + "\n" + \
               self.get_plot_data_and_scales_code(n_x_ticks, n_y_ticks)

    def get_legend_code(self):
        return self._jsGroupsLegend

    # --------------------------------------------------------
    # ListPlot
    # --------------------------------------------------------

    _jsScatterPlotPart = """
    // Add dots
    svg
      .selectAll("whatever")
      .data(data)
      .enter()
      .append("circle")
        .attr("cx", function(d){ return x(d.x) })
        .attr("cy", function(d){ return y(d.y) })
        .attr("r", 3)
        .attr("color", "blue")
        .attr("fill", $POINT_COLOR)
    """

    _jsMultiScatterPlotPart = """
    // Add a scale for dot color
    var myColor = d3.scaleOrdinal()
        .domain(data.map(function(o) { return o.group; }))
        .range(d3.schemeSet2);

    // Add dots
    svg
      .selectAll("whatever")
      .data(data)
      .enter()
      .append("circle")
        .attr("cx", function(d){ return x(d.x) })
        .attr("cy", function(d){ return y(d.y) })
        .attr("r", 3)
        .attr("color", "blue")
        .attr("fill", function (d) { return myColor(d.group) } )
    """

    # --------------------------------------------------------
    # ListPlot Accessors
    # --------------------------------------------------------
    def get_scatter_plot_part(self):
        return self._jsScatterPlotPart

    def get_multi_scatter_plot_part(self):
        return self._jsMultiScatterPlotPart

    # --------------------------------------------------------
    # ListLinePlot
    # --------------------------------------------------------
    _jsPathPlotPart = """
    // prepare a helper function
    var lineFunc = d3.line()
      .x(function(d) { return x(d.x) })
      .y(function(d) { return y(d.y) })

    // Add the path using this helper function
    svg.append('path')
      .attr('d', lineFunc(data))
      .attr('stroke', $LINE_COLOR)
      .attr('fill', 'none');
    """

    # See https://d3-graph-gallery.com/graph/line_several_group.html
    _jsMultiPathPlotPart = """
    // group the data: I want to draw one line per group
    const sumstat = d3.group(data, d => d.group); // nest function allows to group the calculation per level of a factor

    // Add a scale for line color
    var myColor = d3.scaleOrdinal()
        .domain(data.map(function(o) { return o.group; }))
        .range(d3.schemeSet2);

    // Draw the line
    svg.selectAll(".line")
          .data(sumstat)
          .join("path")
            .attr("fill", "none")
            .attr("stroke", function(d){ return myColor(d[0]) })
            .attr("stroke-width", 1.5)
            .attr("d", function(d){
              return d3.line()
                .x(function(d) { return x(d.x); })
                .y(function(d) { return y(+d.y); })
                (d[1])
            })

    """

    # --------------------------------------------------------
    # ListLinePlot Accessors
    # --------------------------------------------------------
    def get_path_plot_part(self):
        return self._jsPathPlotPart

    def get_multi_path_plot_part(self):
        return self._jsMultiPathPlotPart

    # --------------------------------------------------------
    # DateListPlot code snippets
    # --------------------------------------------------------
    _jsPlotDateDataAndScales = """
    // Obtain data
    var data = $DATA

    data = data.map(function(d){
        var d2 = d;
        d2["x"] = d3.timeParse("%Y-%m-%d")(d.date);
        if ( "value" in d ) { d2["y"] = d.value; }
        return d2
    })

    var yMin = Math.min.apply(Math, data.map(function(o) { return o.y; }))
    var yMax = Math.max.apply(Math, data.map(function(o) { return o.y; }))

    // Add X axis --> it is a date format
    var x = d3.scaleTime()
      .domain(d3.extent(data, function(d) { return d.x; }))
      .range([ 0, width ]);

    svg
        .append('g')
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))

    // Y scale and Axis
    var y = d3.scaleLinear()
        .domain([yMin, yMax])
        .range([height, 0]);

    svg
        .append('g')
        .call(d3.axisLeft(y));
    """

    # --------------------------------------------------------
    # DateListPlot code snippets accessors
    # --------------------------------------------------------
    def get_plot_date_data_and_scales(self):
        return self._jsPlotDateDataAndScales

    # --------------------------------------------------------
    # BarChart code snippets
    # --------------------------------------------------------
    _jsBarChartPart = """
// Obtain data
var data = $DATA

var valueMin = Math.min.apply(Math, data.map(function(o) { return o.Value; }))
var valueMax = Math.max.apply(Math, data.map(function(o) { return o.Value; }))

// X axis
var x = d3.scaleBand()
  .range([ 0, width ])
  .domain(data.map(function(d) { return d.Label; }))
  .padding(0.2);
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x))
  .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");

// Add Y axis
var y = d3.scaleLinear()
  .domain([0, valueMax])
  .range([ height, 0]);
svg.append("g")
  .call(d3.axisLeft(y));

// Bars
svg.selectAll("mybar")
  .data(data)
  .enter()
  .append("rect")
    .attr("x", function(d) { return x(d.Label); })
    .attr("y", function(d) { return y(d.Value); })
    .attr("width", x.bandwidth())
    .attr("height", function(d) { return height - y(d.Value); })
    .attr("fill", $FILL_COLOR)    
    """

    # --------------------------------------------------------
    # BarChart code snippets accessors
    # --------------------------------------------------------
    def get_bar_chart_part(self):
        return self._jsBarChartPart
