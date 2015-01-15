"use strict";

window.onload = function() {

    // 
    function parse_json(json_id) {
        var selected = document.getElementById(json_id).value
        var parsed = JSON.parse(selected)
        console.log("----------  JSON data parsed")
        return parsed
    }
     
    var regatta = parse_json("method_one")

    //var 


    console.log(regatta.fields.HTal_acht.heats)
    //console.log("json.name >>>>", regatta.name)
    //console.log("json.date >>>>", regatta.date)
    //console.log("json.fields >>>>", regatta.fields)
    //console.log("json.fields.heatname >>>>", regatta.fields.B1x)
    //console.log("json.fields.heatname.heats >>>>", regatta.fields.'B1x'.heats)
    //console.log("json.fields.heatname.heats[2] >>>>", regatta.fields.'B1x'.heats[2])
    //console.log("json.fields.heatname.heats[2].participants >>>>", regatta.fields.'B1x'.heats[2].participants)

    // get all teams and times in final of LO4-

    // console.log(regatta.fields."LO4-")]

    function make_heat_graph(dataset, legend, element) {

        // Set up size of the graph (c) mbostock
        var margin = {top: 20, right: 35, bottom: 30, left: 45},
            width = 640 - margin.left - margin.right,
            height = 350 - margin.top - margin.bottom;
        var barpadding = 1;

        var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1);

        var y = d3.scale.linear()
            .range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(10, "%");

        // Select the element to place svg in, add svg to it
        var svg = d3.select(element)
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height)

        svg.selectAll("rect")
            .data(dataset)
                .enter().append("rect")
                    .attr("x", function(d,i) {
                        return i*(width / dataset.length);
                    })
                    .attr("y", function(d) {
                        return height - d;
                    })
                    .attr("width", function(d,i) {
                        return width / dataset.length - barpadding
                    })
                    .attr("height", function(d,i) {
                        return d
                    })
                    .attr("fill", "steelblue")

     }

     var dataset = [ 5, 10, 13, 19, 21, 25, 22, 18, 15, 13,
                11, 12, 15, 20, 18, 17, 16, 18, 23, 25 ];
     make_heat_graph(dataset, "ok", "#heat_stat")


}


/*
     json.name [regatta name]
     json.date [regatta date]
     json.fields [list of fields]
*/