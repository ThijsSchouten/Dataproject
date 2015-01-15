/*
name: Thijs Schouten
student number: 10887679
*/

window.onload = function() {

    // set margins 
    var margin = {top: 30, right: 30, bottom: 30, left: 60},
        width = 700 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

    // set function to format the data to Date
    var format_date = d3.time.format("%d-%m-%Y").parse;

    // set a variable to scale the data to the axes
    var x = d3.time.scale()
        .range([0,width]);

    var y = d3.scale.linear()
        .range([height,0]);

    // functions to create the x/y axes 
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(d3.time.weeks, 1)
        .tickFormat(d3.time.format('%W'));

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    /* Passing json data like this only works in FireFox 
       or on a (local) server. */
    d3.json("data.json", function(error, json) {
        if (error) return console.warn("error");

        var dataset = json.trainingen,
            datum_array = [],
            score_array = [];

        dataset.forEach(function(d) {
            d.datum = format_date(d.datum),
            datum_array.push(d.datum),
            d.score = +d.score,
            score_array.push(d.score);
        });

        x.domain(d3.extent(datum_array));
        y.domain(d3.extent(score_array));

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
          .append("text")
            .attr("x", width)
            .attr("dy", "-0.71em")
            .style("text-anchor", "end")
            .text("Week number");

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 5)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Seconds / 500m");

        svg.append("text")
            .attr("class", "g_title")
            .attr("x", (width / 2))             
            .attr("y", 0 - (margin.top / 3))
            .attr("text-anchor", "middle")
            .text("Ergometer Scores Autumn'14 (2x 45min - T20)");

        svg.selectAll("dot")
            .data(dataset)
          .enter().append("circle")
            .attr("class", "dot")
            .attr("cx", function(d) { return x(d.datum) } )
            .attr("cy", function(d) { return y(d.score) } )
            .attr("r", 2);



        });
}