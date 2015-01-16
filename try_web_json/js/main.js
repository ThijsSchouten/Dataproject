"use strict";

window.onload = function() {

    function make_heat_graph(json_file_loc, element, veld, iter) {

        // Set up size of the graph (c) mbostock
        var margin = {top: 20, right: 35, bottom: 30, left: 45},
            width = 200 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

        // var format_time = d3.time.format("%M:%S,%L").parse;

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
            .ticks(10, "M")

        // Select the element to place svg in, add svg to it
        var svg = d3.select(element)
                    .append("svg")
                        .attr("width", width + margin.left + margin.right)
                        .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        d3.json(json_file_loc, function(error, json) {
            if (error) return console.warn("error loading json");
            
            var dataset = []

            for (var crew in json.fields.B_acht.heats[iter].participants) {
                var crew_code = (json.fields.B_acht.heats[iter].participants[crew].crew_code)
                var crew_time = (json.fields.B_acht.heats[iter].participants[crew].twenty_time)
                var crew_lane = (json.fields.B_acht.heats[iter].participants[crew].lane)
                dataset.push({crew: crew_code, times: crew_time, lane: crew_lane})
            }   

            // 
            x.domain(dataset.map(function(d,i) {return dataset[i].crew} ));
            y.domain([350, 400])
            /*y.domain([d3.min(dataset, function(d,i) { return dataset[i].times}) - 15,
                      d3.max(dataset, function(d,i) { return dataset[i].times}) + 15])*/

            // x axis text
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis)
              .append("text")
                .attr("x", width)
                .attr("dy", "-0.71em")
                .style("text-anchor", "end")
                //.text("CREW"); 

            // y axis text
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
              .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 10)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("FINISH TIME");

            // title text
            svg.append("text")
                .attr("class", "g_title")
                .attr("x", (width / 2))             
                .attr("y", 0 - (margin.top / 3))
                .attr("text-anchor", "middle")
                .text(veld)

            svg.selectAll(".bar")
                .data(dataset)
              .enter().append("rect")
                .attr("class", "bar")
                .attr("x", function(d,i) {return x(dataset[i].crew); })
                .attr("width", (x.rangeBand()))
                .attr("y", function(d,i) {return y(dataset[i].times); })
                .attr("height", function(d,i) {return height - y(dataset[i].times); }) 
                
        });

    }

    make_heat_graph("json/NSRF 2014.json", "#heat_stat", "B8+ A-Finale", 2)
    make_heat_graph("json/NSRF 2014.json", "#heat_stat", "B8+ Heat 2", 1)
    make_heat_graph("json/NSRF 2014.json", "#heat_stat", "B8+ Heat 1", 0)

}

/*
                .attr("x", function(d,i) {return x(d.letter); })
                .attr("width", x.rangeBand())
                .attr("y", function(d) {return y(d.frequency); })
                .attr("height", function(d) {return height - y(d.frequency); })
*/
