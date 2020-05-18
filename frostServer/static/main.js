function addTimestampedPointToSeries(series, value) {
    var x = (new Date()).getTime()
    var y = value
    
    if(series.data.length > 40)
        series.addPoint([x, y], true, true, true)
    else
        series.addPoint([x, y], true, false, true)
}

function handleUrlResponse(url, onUrlResponseText) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4)
            onUrlResponseText(this.responseText)
    }
    xhttp.open("GET", url, true);
    xhttp.send();
}

function urlResponseToChartSeries(url, series) {
    handleUrlResponse(url, (responseText) => {
        addTimestampedPointToSeries(series, parseFloat(responseText))
    })
}


let panel = new cpanel.ButtonPanel("panel")
panel.buttonStyle = "PanelButton"
panel.panelStyle = "Panel"
panel.appendToParent(document.getElementById("cameraContainer"))

panel.addButtonChangeListener((change) => {
    var request = new XMLHttpRequest();
    request.open("POST", "/updateImageStream")
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    request.send(JSON.stringify(change))              
})

const categoryNameToClass = {
    'toggle': cpanel.ToggleButtonCategory,
    'radio': cpanel.RadioButtonCategory
}

handleUrlResponse('/imageStreamChoices', (response) => {
    categorySetups = JSON.parse(response)
    for (let [key, categorySetup] of Object.entries(categorySetups)) {
        let category = new categoryNameToClass[categorySetup.type](key)
        categorySetup.names.forEach((name) => {
            category.addButton(name)
        })
        categorySetup.defaults.forEach((name) => {
            category.turnOnButton(name)
        })
        panel.addCategory(category)
    }
})
