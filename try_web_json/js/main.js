"use strict";

window.onload = function() {

    heat_graphs("json/NSRF_2014.json", "#heat_stat", "B_acht", 2, "B8+ Finale")
    heat_graphs("json/NSRF_2014.json", "#heat_stat", "B_acht", 1, "B8+ Heat 1")
    heat_graphs("json/NSRF_2014.json", "#heat_stat", "B_acht", 0, "B8+ Heat 2")

    regatta_overview_graph("json/NSRF_2014.json", "#regatta_overview")
    lane_advantage_scatterplot("json/NSRF_2014.json", "#lane_advantage")

    function heat_graphs(json_file_loc, element, asked_field, iter, name) {

        // Credits jshanley on stackoverflow.
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
                    //console.log(json.fields[index])

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

    function regatta_overview_graph(json_file_loc, element) {

        // Set up size of the graph 
        var margin = {top: 20, right: 10, bottom: 60, left: 35},
            width = 700 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

        var dotwidth = 5

        // Ordinal scale on x-axis, linear on y-axis
        var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1);

        var y = d3.scale.linear()
            .range([height, 0]);

        // x- axis will but put at the bottom, y at top. Y ticks in percentages
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .tickFormat(d3.format(".0%"));

        // select the tooltip div
        var tooltip = d3.select(".tooltip")          
            .style("opacity", 0);

        // call the JSON file
        d3.json(json_file_loc, function(error, json) {
            if (error) return console.warn("error loading json");
            
            // variables to store the saturday and sunday heats
            var dataset_sat = [],
                dataset_sun = []

            // for every field in the json
            for (var i in json.fields) {

                // find heat containing the finale data
                if (json.fields[i].heattype === "Final A") 
                {
                    // find the day of the race. 
                    var day = (json.fields[i].heat_day_time.substring(0,3))

                    // for every team in the race
                    for (var team in json.fields[i].participants) {

                        // save the stats
                        var heat_id = json.fields[i].id,
                            crew_code = json.fields[i].participants[team].crew_code,
                            crew_time = json.fields[i].participants[team].twenty_time,
                            crew_names = json.fields[i].participants[team].names;

                        var heat_dict = {final_id: heat_id, code: crew_code,
                                         finish_time: crew_time, names: crew_names}

                        // push to the matching day
                        if (day.indexOf("zo ") != -1) {
                            dataset_sun.push(heat_dict)
                        } else {
                            dataset_sat.push(heat_dict)
                        }
                    }              
                }
            }   
            
            r_overview(dataset_sat)
            r_overview(dataset_sun)

            function r_overview(dataset) {

                // Select the element to place svg in, add svg to it
                var svg = d3.select(element)
                  .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                  .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                x.domain(dataset.map(function(d,i) {return dataset[i].final_id} ))
                y.domain([0.8, 1]);
     
                // x axis text
                svg.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis)
                    .selectAll("text")  
                    .style("text-anchor", "end")
                    .attr("dx", "-.6em")
                    .attr("dy", ".10em")
                    // credits: http://www.d3noob.org/2013/01/how-to-rotate-text-labels-for-x-axis-of.html
                    .attr("transform", function(d) { return "rotate(-60)" })
                    .append("text")
                        .attr("x", width)
                        .attr("dy", "-0.71em")
                        .style("text-anchor", "end")
                        .text("HEAT ID"); 

                // y axis text
                svg.append("g")
                    .attr("class", "y axis")
                    .call(yAxis)
                  .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 10)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("SPEED");

                // make circles

                svg.selectAll("dot")
                    .data(dataset)
                  .enter().append("circle")
                    .attr("class", "dot")
                    .attr("cx", function(d,i) { return (x(dataset[i].final_id) )} )
                    .attr("cy", function(d,i) { return y(speed_percentage(dataset[i].finish_time,
                                                                          dataset[i].final_id)) } )
                    .attr("r", dotwidth)
                    .on("mouseover", function(d,i) { 

                        var id = dataset[i].final_id,
                            code = dataset[i].code,
                            names = dataset[i].names.join("<br>");

                        tooltip.transition()        
                            .duration(250)      
                            .style("opacity", .7);      
                        tooltip.html("<strong>" + id + "&nbsp&nbsp|&nbsp&nbsp" +
                                     code + "</strong><hr>" + names)
                        .style("left", _x + "px")     
                        .style("top", _y + "px"); 

                        })                  
                    .on("mouseout", function(d) {       
                        tooltip.transition()        
                            .duration(700)      
                            .style("opacity", 0);   
                    });


            }
                
        });
    }

    function speed_percentage(time, field_id) {

        var best = 1 / QUICKEST_TIMES[field_id],
            current = 1 / time,
            percentage = (current / best)

        if (isNaN(percentage) === true) {
            console.log("error, no time or no best_time found")
            return 0.5
        }

        return percentage
    }


    // Run this to find fastest times for every heat, save in QUICKEST_TIMES
    // Running this every time the sites loads would make it very slow --> 
    // Save the list, copy/paste from FF with the .toSource() function

    
    // get_quickest_times("json/NSRF_2014.json")
    //console.log(QUICKEST_TIMES["SA1x"])

    

    function get_quickest_times(json_file_loc) {

        var records = {}

        d3.json(json_file_loc, function(error, json) {
            if (error) return console.warn("error loading json");

            // for every field
            for (var i in json.fields) {
                // save the heattype
                var heattype = json.fields[i].id

                for (var j in json.fields[i].participants) {
                    //console.log(json.fields[i].participants[j])
                    var time = json.fields[i].participants[j].twenty_time
                    if (records[heattype] === undefined) {
                        records[heattype] = time
                    } else if (time < records[heattype]) {
                        records[heattype] = time
                    } else {
                        //console.log("no new record")
                    }
                }
            } 

            console.log(records.toSource())
        
            // return records
        });
    }

}

var QUICKEST_TIMES = ({SA1x:[421.48], 'SA2+':[438.49], 'SA2-':[387.67], SA2x:[394.23], 'SA4-':[359.74], SA4x:[352.94], 'SA8+':[342.15], O1x:[430.38], 'O2-':[408.48], 'O4+':[401.3], 'O4-':[378.06], N1x:[442.79], 'N2+':[457.37], 'N2-':[411.07], N2x:[421.58], 'N4+':[399.55], 'N4-':[386.48], B1x:[434.36], 'B4+':[403.83], 'B8+':[354.85], LSA1x:[422.78], 'LSA2+':[455.9], 'LSA2-':[417.35], 'LSA4-':[365.97], 'LSA8+':[360.06], LO1x:[436.57], 'LO2-':[408.01], 'LO4+':[420.12], 'LO4-':[369.35], LN1x:[447.51], 'LN2+':[466.16], 'LN2-':[426.34], LN2x:[414.08], 'LN4+':[422], 'LN4-':[393.98], LB1x:[453.77], 'LB8+':[371.99], DSA1x:[458.46], 'DSA2+':[511.52], 'DSA2-':[437.64], DSA2x:[442.34], 'DSA4-':[411.91], DSA4x:[379.12], 'DSA8+':[407.32], DO1x:[479.86], 'DO2-':[450.59], 'DO4+':[442.69], DN1x:[489.78], 'DN2-':[466.95], DN2x:[464], 'DN4+':[450.32], 'DN4-':[434.23], DB1x:[493.39], 'DB4+':[464.6], 'DB8+':[400.7], LDSA1x:[463.29], LDO1x:[498.32], LDN1x:[492.68], LDN2x:[474.33], LDB1x:[524.39], 'Ej8+':[350.81], 'Dev4-':[373.21], 'LEj8+':[361.28], 'LDev4-':[378.37], 'DEj8+':[397.61], 'DDev4-':[412.43], 'LDEj4*':[443.73], LDDev2x:[451.36], J181x:[436.66], J182x:[407.25], J184x:[365.37], 'J188+':[361.13], J161x:[457.86], J162x:[430.13], 'J164*':[431.29], J164x:[398.19], 'J168+':[387.05], M181x:[496.36], 'M182-':[492.41], M182x:[462.01], M184x:[436.5], Meisjesacht:"no_data", M161x:[519.58], M162x:[477.96], 'M164*':[481.1], M164x:[447.86], 'M168+':[436.77], 'HTal8+':[388.78], 'DTal8+':[441.55]})


