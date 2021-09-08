var width = 960,
    height = 500;


function icicleChartTB (chartData) {

    const format = d3.format(",d");
    const color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, chartData.children.length + 1));

    var x = d3.scaleLinear()
    .range([0, width]);

    var y = d3.scaleLinear()
        .range([0, height]);

    var partition = d3.partition()
        .size([width, height])
        .padding(0)
        .round(true);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    var rect = svg.selectAll("rect");

    let root = d3.hierarchy (Object.entries(chartData)[0], function(d) {
        return Object.entries(d.value)
        })
        .sum(function(d) { return d.value })
        .sort(function(a, b) { return b.value - a.value; });

    partition(root);

    rect = rect
        .data(root.descendants())
        .enter().append("rect")
        .attr("x", function(d) { return d.x0; })
        .attr("y", function(d) { return d.y0; })
        .attr("width", function(d) { return d.x1 - d.x0; })
        .attr("height", function(d) { return d.y1 - d.y0; })
        .attr("fill", function(d) { return color((d.children ? d : d.parent).data.key); })
        .on("click", clicked);
    

    function clicked(d) {
    x.domain([d.x0, d.x1]);
    y.domain([d.y0, height]).range([d.depth ? 20 : 0, height]);

    rect.transition()
        .duration(750)
        .attr("x", function(d) { return x(d.x0); })
        .attr("y", function(d) { return y(d.y0); })
        .attr("width", function(d) { return x(d.x1) - x(d.x0); })
        .attr("height", function(d) { return y(d.y1) - y(d.y0); });
    }
}



