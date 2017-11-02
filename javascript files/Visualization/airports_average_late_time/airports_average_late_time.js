/**
 * This File represents the logic behind the visualization.
 * In this logic, we are presenting bubble char, that represents the the amount of average late_time of
 * the incoming flights for each airport.*/

var diameter = 1000,
    format = d3.format(",d"),
    color = d3.scaleOrdinal(d3.schemeCategory20c);

var bubble = d3.pack()
    .size([diameter, diameter])
    .padding(1.5);

var svg = d3.select("body").append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .attr("class", "bubble");

d3.json("airports_average_late_time.json", function(error, jsonData) {
    var data = {"name": "airports", children:[]};

    for (var key in jsonData){
        if(1 <= jsonData[key].average_late)
            data.children.push({name:jsonData[key].name, size: Math.round(jsonData[key].average_late)})
    }
    console.log(data)
    if (error) throw error;

    var root = d3.hierarchy(classes(data))
        .sum(function(d) { return d.value; })
        .sort(function(a, b) { return b.value - a.value; });

    bubble(root);
    var node = svg.selectAll(".node")
        .data(root.children)
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

    node.append("title")
        .text(function(d) { return d.data.className + ": " + format(d.value); });

    node.append("circle")
        .attr("r", function(d) { return d.r; })
        .style("fill", function(d, i) { return color(i); });

    node.append("text")
        .attr("dy", ".3em")
        .style("text-anchor", "middle")
        .text(function(d) {
            if(5 < d.value)
                return d.data.className.substring(0, d.r / 4) + "\n" + numberWithCommas(d.value.toString().substring(0,d.r /6));
            return d.data.className.substring(0, d.r /3);
        });
});
function classes(root) {
    var classes = [];

    function recurse(name, node) {
        if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
        else classes.push({packageName: name, className: node.name, value: node.size});
    }

    recurse(null, root);
    return {children: classes};
}

d3.select(self.frameElement).style("height", diameter + "px");

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}