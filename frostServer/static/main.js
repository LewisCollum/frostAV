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

function updateStats() {
    let cpuCelsiusText = document.getElementById("cpuCelsiusText")
    handleUrlResponse("/cpuCelsius", (responseText) => {
        cpuCelsiusText.innerHTML = `${parseFloat(responseText)}&degC CPU` 
    })

    let gpuCelsiusText = document.getElementById("gpuCelsiusText")    
    handleUrlResponse("/gpuCelsius", (responseText) => {
        gpuCelsiusText.innerHTML = `${parseFloat(responseText)}&degC GPU` 
    })

    urlResponseToChartSeries("/cpuLoad", chartL.series[0])
    urlResponseToChartSeries("/memoryUsed", chartM.series[1])
    urlResponseToChartSeries("/memoryFree", chartM.series[0])
    urlResponseToChartSeries("/power", chartT.series[0])
    urlResponseToChartSeries("/voltage", chartH.series[0])
    urlResponseToChartSeries("/current", chartP.series[0])    
}

updateStats()
setInterval(updateStats, 5000)
