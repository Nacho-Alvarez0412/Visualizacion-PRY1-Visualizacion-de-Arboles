

// LOAD DATA SEGMENT

/*
    JSON FORMAT:
    {Section ID,Section,HS2 ID, HS2, HS4 ID, HS4}
*/

const URL = "https://oec.world/olap-proxy/data?cube=trade_i_baci_a_92&Exporter+Country=nacri&drilldowns=HS4&measures=Trade+Value&parents=true&Year=2019&sparse=false&locale=en&q=Trade Value"

let CHART_DATA;

function formatData(data){

    formattedData = {"name":'Exportaciones en Costa Rica', "children":[]};
    sections = {"Section ID": 0, "Section": '', "children": []}
    leaves = {"HS2 ID": 0 , "HS2": '', "children": []}

    data.forEach(element => 
        {
            leaf = { "HS4 ID": element["HS4 ID"],"HS4": element.HS4,"Trade Value": element["Trade Value"] }

            if(sections["Section ID"] == 0){
                sections["Section ID"] = element["Section ID"];
                sections["Section"] = element["Section"];
            }

            if(sections["Section ID"] != element["Section ID"]){
                formattedData["children"].push(JSON.parse(JSON.stringify(sections)));
                sections["Section ID"] = element["Section ID"];
                sections["Section"] = element["Section"];
            }
            
            if(leaves["HS2 ID"] == 0){

                leaves["HS2 ID"] = element["HS2 ID"];
                leaves["HS2"] = element["HS2"];
            }

            if (leaves["HS2 ID"] != element["HS2 ID"]){

                sections["children"].push(JSON.parse(JSON.stringify(leaves)));
                leaves["HS2 ID"] = element["HS2 ID"];
                leaves["HS2"] = element["HS2"];
                leaves["children"] = [];
            }

            leaves["children"].push(leaf);
        }
        )
    sections["children"].push(leaves);
    formattedData["children"].push(sections);
    return formattedData;
}

fetch(URL)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
         CHART_DATA = formatData(data.data);
    })
    .catch((error) => 
    {console.log(error)
    });




// CHART GENERATION SEGMENT

const CHART_WIDTH = 975;
const CHART_HEIGHT = 1200;
const format = d3.format(",d")
const color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, CHART_DATA.children.length + 1))