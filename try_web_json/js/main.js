"use strict";

window.onload = function() {



    function make_heat_graph(json_file_loc, element, asked_field, iter, name) {

        var formatMinutes = function(d) { 
            var hours = Math.floor(d / 3600),
                minutes = Math.floor((d - (hours * 3600)) / 60),
                seconds = d - (minutes * 60);
            var output = seconds + '"';
            if (minutes) {
                output = minutes + "m " + output;
            }
            if (hours) {
                output = hours + 'h ' + output;
            }
            return output;
        };

        // Set up size of the graph (c) mbostock
        var margin = {top: 20, right: 10, bottom: 30, left: 45},
            width = 240 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

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
            .ticks(10)
            .tickFormat(formatMinutes);

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

            // for every field
            for (var index in json.fields) {

                //find the right field
                if (json.fields[index].field === asked_field) {

                    index = (parseInt(index) + parseInt(iter))
                    console.log(json.fields[index])

                    // save every teams data
                    for (var team in json.fields[index].participants) {
                        var crew_code = (json.fields[index].participants[team].crew_code)
                        var crew_time = (json.fields[index].participants[team].twenty_time)
                        var crew_lane = (json.fields[index].participants[team].lane)
                        dataset.push({crew: crew_code, times: crew_time, lane: crew_lane})
                    }
                    break
                }  
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
                .text(name)

            svg.selectAll(".bar")
                .data(dataset)
              .enter().append("rect")
                .attr("class", "bar")
                .attr("x", function(d,i) {return x(dataset[i].crew); })
                .attr("width", (x.rangeBand()))
                .attr("y", function(d,i) {return y(dataset[i].times); })
                .attr("height", function(d,i) {return height - y(dataset[i].times); }) 
                
            svg.selectAll("text")
        });
    }

    function lane_advantage_scatterplot(json_file_loc, element) {

        // Set up size of the graph (c) mbostock
        var margin = {top: 20, right: 10, bottom: 30, left: 45},
            width = 480 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

        var x = d3.scale.linear()
            .range([0, width]);

        var y = d3.scale.linear()
            .range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
        

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")


            //.ticks(7)
            //.tickValues(600);

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

            for (var i in json.fields) {

                for (var j in json.fields[i].participants) {
                    if (json.fields[i].heattype === "Heat") {
                        var pos = parseInt(j) + 1
                        var lane = json.fields[i].participants[j].lane
                        dataset.push({lanes: lane, positions: pos})
                    }
                }
            }   
            

            //x.domain([d3.min(dataset.lanes), d3.max(dataset.lanes)]),

            x.domain([d3.min(dataset, function(d,i) { return dataset[i].lanes}),
                      d3.max(dataset, function(d,i) { return dataset[i].lanes})])

            y.domain([d3.max(dataset, function(d,i) { return dataset[i].positions}),
                      d3.min(dataset, function(d,i) { return dataset[i].positions})])
 
            // x axis text
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis)
              .append("text")
                .attr("x", width)
                .attr("dy", "-0.71em")
                .style("text-anchor", "end")
                .text("LANE"); 

            // y axis text
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
              .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 10)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("FINISH POSITION");

            /* title text
            svg.append("text")
                .attr("class", "g_title")
                .attr("x", (width / 2))             
                .attr("y", 0 - (margin.top / 3))
                .attr("text-anchor", "middle")
                .text("Lane") */

            /*svg.selectAll("dot")
                .data(dataset)
              .enter().append("circle")
                .attr("class", "dot")
                .attr("fill-opacity", "0.04")
                .attr("cx", function(d,i) { return x(dataset[i].lanes) } )
                .attr("cy", function(d,i) { return y(dataset[i].positions) } )
                .attr("r", 10);*/


            svg.selectAll(".pos_bar")
                .data(dataset)
              .enter().append("rect")
                .attr("fill-opacity", "0.04")
                .attr("x", function(d,i) {return x(dataset[i].lanes) } )
                .attr("y", function(d,i) {return y(dataset[i].positions) } )
                .attr("width", (width/7))
                .attr("height", (height/7));
                
        });
    }

    make_heat_graph("json/NSRF_2014.json", "#heat_stat", "B_acht", 2, "B8+ Finale")
    make_heat_graph("json/NSRF_2014.json", "#heat_stat", "B_acht", 1, "B8+ Heat 1")
    make_heat_graph("json/NSRF_2014.json", "#heat_stat", "B_acht", 0, "B8+ Heat 2")
    //make_heat_graph("json/NSRF_2014.json", "#heat_stat", "B8+ Heat 1", 0)
    //make_heat_graph("json/NSRF_2014.json", "#heat_stat", "B8+ Heat 2", 1)

    lane_advantage_scatterplot("json/NSRF_2014.json", "#lane_advantage")

}



/*
                .attr("x", function(d,i) {return x(d.letter); })
                .attr("width", x.rangeBand())
                .attr("y", function(d) {return y(d.frequency); })
                .attr("height", function(d) {return height - y(d.frequency); })
*/
