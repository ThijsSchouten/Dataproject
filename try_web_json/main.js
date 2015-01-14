"use strict";

window.onload = function() {

     // 
     function parse_json(id) {
          var selected = document.getElementById(id).value
          return JSON.parse(selected)
     }
     
     var parsed_data = parse_json("method_one")
     // console.log(parsed_data)



     console.log


     // for (var field in parsed_data.Fields) {
     //     console.log(parsed_data.Fields)
     //}
}