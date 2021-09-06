const URL = "https://oec.world/olap-proxy/data?cube=trade_i_baci_a_92&Exporter+Country=nacri&drilldowns=HS4&measures=Trade+Value&parents=true&Year=2019&sparse=false&locale=en&q=Trade Value"

let CHART_DATA;

function formatData( data ) {

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

async function getData() {
     return new Promise ((resolve,reject) => {
        fetch(URL)
            .then( (repsonse) => {
                return repsonse.json();
            })
            .then( (data) => {
                //data = formatData(data.data.slice(0,100));
                
                data =  formatData(data.data);
                resolve( data);
            })
            .catch((error) => {
                console.log(error)
            });  
     })
}




