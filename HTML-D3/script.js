

// LOAD DATA SEGMENT

/*
    JSON FORMAT:
    {Section ID,Section,HS2 ID, HS2, HS4 ID, HS4}
*/

const URL = "https://oec.world/olap-proxy/data?cube=trade_i_baci_a_92&Exporter+Country=nacri&drilldowns=HS4&measures=Trade+Value&parents=true&Year=2019&sparse=false&locale=en&q=Trade Value"

let CHART_DATA;

function formatData(data){

    formattedData = {"name":'Exportaciones en Costa Rica', "children":[]};
    sections = {"Section ID": 0, "name": '', "children": []}
    leaves = {"HS2 ID": 0 , "name": '', "children": []}

    data.forEach(element => 
        {
            leaf = { "HS4 ID": element["HS4 ID"],"name": element.HS4,"Trade Value": element["Trade Value"] }

            if(sections["Section ID"] == 0){
                sections["Section ID"] = element["Section ID"];
                sections["name"] = element["Section"];
            }

            if(sections["Section ID"] != element["Section ID"]){
                formattedData["children"].push(JSON.parse(JSON.stringify(sections)));
                sections["Section ID"] = element["Section ID"];
                sections["name"] = element["Section"];
            }
            
            if(leaves["HS2 ID"] == 0){

                leaves["HS2 ID"] = element["HS2 ID"];
                leaves["name"] = element["HS2"];
            }

            if (leaves["HS2 ID"] != element["HS2 ID"]){

                sections["children"].push(JSON.parse(JSON.stringify(leaves)));
                leaves["HS2 ID"] = element["HS2 ID"];
                leaves["name"] = element["HS2"];
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
         chart();

    })
    .catch((error) => 
    {console.log(error)
    });



const CHART_WIDTH = 975;
const CHART_HEIGHT = 1000;
const format = d3.format(",d");

function chart()  {
    
    const color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, CHART_DATA.children.length + 1));

    const root = partition(CHART_DATA);
    let focus = root;
    console.log(root.descendants())
    const svg = 
        d3.select("#Chart")
        .append("svg")
        .attr("viewBox", [0, 0, CHART_WIDTH, CHART_HEIGHT])
        .style("font", "10px sans-serif");
    
    const cell = svg
        .selectAll("g")
        .data(root.descendants())
        .join("g")
        .attr("transform", d => `translate(${d.y0},${d.x0})`);
    
    const rect = cell.append("rect")
        .attr("width", d => d.y1 - d.y0 - 1)
        .attr("height", d => rectHeight(d))
        .attr("fill-opacity", 0.6)
        .attr("fill", d => {
            if (!d.depth) return "#ccc";
            while (d.depth > 1) d = d.parent;
            return color(d.data.name);
        })
        .style("cursor", "pointer")
        .on("click", clicked);
    
    const text = cell.append("text")
        .style("user-select", "none")
        .attr("pointer-events", "none")
        .attr("x", 4)
        .attr("y", 13)
        .attr("fill-opacity", d => +labelVisible(d));
    
    text.append("tspan")
        .text(d => d.data.name);
    
    const tspan = text.append("tspan")
        .attr("fill-opacity", d => labelVisible(d) * 0.7)
        .text(d => ` ${format(d.value)}`);
    
    cell.append("title")
        .text(d => `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${format(d.value)}`);
    
    function clicked(event, p) {
        focus = focus === p ? p = p.parent : p;
    
        root.each(d => d.target = {
        x0: (d.x0 - p.x0) / (p.x1 - p.x0) * CHART_HEIGHT,
        x1: (d.x1 - p.x0) / (p.x1 - p.x0) * CHART_HEIGHT,
        y0: d.y0 - p.y0,
        y1: d.y1 - p.y0
        });
    
        const t = cell.transition().duration(750)
            .attr("transform", d => `translate(${d.target.y0},${d.target.x0})`);
    
        rect.transition(t).attr("height", d => rectHeight(d.target));
        text.transition(t).attr("fill-opacity", d => +labelVisible(d.target));
        tspan.transition(t).attr("fill-opacity", d => labelVisible(d.target) * 0.7);
    }
    
    function rectHeight(d) {
        return d.x1 - d.x0 - Math.min(1, (d.x1 - d.x0) / 2);
    }
    
    function labelVisible(d) {
        return d.y1 <= CHART_WIDTH && d.y0 >= 0 && d.x1 - d.x0 > 16;
    }
    
    return svg.node();
}

partition = data => {
        const root = d3.hierarchy(data)
            .sum(d => d["Trade Value"])
            .sort((a, b) => b.height - a.height || b["Trade Value"] - a["Trade Value"]);  
        return d3.partition()
            .size([CHART_HEIGHT, (root.height + 1) * CHART_WIDTH / 3])
          (root);
}