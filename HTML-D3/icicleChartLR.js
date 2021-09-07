const CHART_WIDTH = 975;
const CHART_HEIGHT = 1000;

function icicleChartLR () {
    
    const format = d3.format(",d");
    const color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, CHART_DATA.children.length + 1));
    const root = partition(CHART_DATA);
    
    const svg = d3.select("#IcicleLR")
        .append("svg")
        .attr("viewBox", [0, 0, CHART_WIDTH, CHART_HEIGHT])
        .style("font", "10px sans-serif");

    const cell = svg.selectAll("g")
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
    
    cell.append("title")
        .text(d =>"Product: "+ `${d.ancestors().map(d => d.data.name).reverse().join(" -> ")}\n Trade Value: ₡${format(d.value)}`)


    const sectionItems = 
        d3.select('#SectionSelect')
        .on('change',onchangeSection)

    sectionItems
        .selectAll('#SectionOption')
            .data(root.children)
            .enter()
            .append("option")
            .text((data) => data.data.name)
            .attr("value", (data) => data.data["Section ID"])
            .attr("class","SectionOption");

    
    function setHS2(data){
        const hs2Items = d3.select('#HS2Select')
            .on('change',onchangeHS2)

        hs2Items
            .selectAll('#HS2Option')
                .data(data)
                .enter()
                .append("option")
                .text((data) => data.data.name)
                .attr("value", (data) => data.data["HS2 ID"])
                .attr("class","HS2Option");
    }
    
        

    function onchangeSection() {
        let selectValue = d3.select('#SectionSelect').property('value')
        let selectedSection;
        let HS2Options;

        root.children.forEach(element => {
            
            if(element.data["Section ID"] == selectValue){
                selectedSection = element;
                HS2Options = element.children;
            }
                
        });
        clicked(null,selectedSection);
        setHS2(HS2Options);
    };

    function onchangeHS2() {
        
        let selectValue1 = d3.select('#HS2Select').property('value');
        let selectValue2 = d3.select('#SectionSelect').property('value');
        let selectedSection;
        let selectedHS2;

        root.children.forEach(element => {
            
            if(element.data["Section ID"] == selectValue2){
                selectedSection = element;
            }
                
        });

        selectedSection.children.forEach(element => {

            if(element.data["HS2 ID"] == selectValue1 ){
                selectedHS2 = element;
            }
        })
        clicked(null,selectedHS2);
    };

    function clicked(event, p) {
        focus = focus === p ? p = p.parent : p;
    
        root.each(d => d.target = {
        x0: (d.x0 - p.x0) / (p.x1 - p.x0) * CHART_HEIGHT,
        x1: (d.x1 - p.x0) / (p.x1 - p.x0) * CHART_HEIGHT,
        y0: d.y0 - p.y0,
        y1: d.y1 - p.y0
        });
    
        const t = cell.transition()
            .duration(750)
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



