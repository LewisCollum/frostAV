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

setInterval(function() {
    let cpuCelsiusText = document.getElementById("cpuCelsiusText")
    handleUrlResponse("/cpuCelsius", (responseText) => {
        cpuCelsiusText.innerHTML = `CPU: ${parseFloat(responseText)}&degC` 
    })

    let gpuCelsiusText = document.getElementById("gpuCelsiusText")    
    handleUrlResponse("/gpuCelsius", (responseText) => {
        gpuCelsiusText.innerHTML = `GPU: ${parseFloat(responseText)}&degC` 
    })
}, 5000)

setInterval(function() {
    urlResponseToChartSeries("/cpuLoad", chartL.series[0])
    urlResponseToChartSeries("/memoryUsed", chartM.series[1])
    urlResponseToChartSeries("/memoryFree", chartM.series[0])
    urlResponseToChartSeries("/power", chartT.series[0])
    urlResponseToChartSeries("/voltage", chartH.series[0])
    urlResponseToChartSeries("/current", chartP.series[0])
}, 5000)
