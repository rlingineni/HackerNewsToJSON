let hnJSON = require("./outputs.json");
const hnApiClient = require('hn-api-client')
const fs = require('fs');

let listOfUpvoted = hnJSON["saved_stories"];

a();

async function a(startFromId) {
    fs.openSync("hn-sites.txt", 'a')
    let hasStarted = false;
    for (let item of listOfUpvoted) {

        if (!hasStarted) {
            if (startFromId) {
                if (item.id != startFromId) {
                    continue;
                }else{
                    hasStarted = true;
                    console.log("Starting from Id............ " + startFromId)
                }
            }
        }
    

    if (item.id) {
        let resp = await hnApiClient.getItem(item.id);
        console.log(resp.url);
        if (resp.url) {
            fs.appendFileSync('hn-sites.txt', `${resp.url}\n`);
        } else {
            console.log("missing url for item " + item.id)
        }

    }
}
}


