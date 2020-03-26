var chartL = new Highcharts.Chart({
    chart: {renderTo : 'chart-load'},
    title: {text: 'System Load'},
    series: [{showInLegend: false, data: []}],
    plotOptions: {
        line: {
            animation: false,
            dataLabels: { enabled: true }},
        series: { color: '#059e8a' }
    },
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }},
    yAxis: {},
    credits: {enabled: false}
})

var chartM = new Highcharts.Chart({
    chart:{ renderTo : 'chart-mem' },
    title: { text: 'Memory' },
    series: [{
        name: 'Used Memory',
        color: '#00FF00',
        showInLegend: true,
        data: []
    }, {
        name: 'Free Memory',
        color: '#FF00FF',
        showInLegend: true,
        data: []
    }],
    plotOptions: {
        line: {
            animation: false,
            dataLabels: { enabled: true }},
        series: { color: '#059e8a' }
    },
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }},
    yAxis: {
        title: {text: "Memory (Mb)" }
    },
    credits: { enabled: false }
});

var chartT = new Highcharts.Chart({
    chart:{ renderTo : 'chart-power' },
    title: { text: 'Power' },
    series: [{
        showInLegend: false,
        data: []
    }],
    plotOptions: {
        line: { animation: false,
                dataLabels: { enabled: true }
              },
        series: { color: '#059e8a' }
    },
    xAxis: { type: 'datetime',
             dateTimeLabelFormats: { second: '%H:%M:%S' }
           },
    yAxis: {
        title: { text: 'Power (W)' }
    },
    credits: { enabled: false }
});

var chartH = new Highcharts.Chart({
    chart:{ renderTo:'chart-voltage' },
    title: { text: 'Battery Voltage' },
    series: [{
        showInLegend: false,
        data: []
    }],
    plotOptions: {
        line: { animation: false,
                dataLabels: { enabled: true }
              }
    },
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }
    },
    yAxis: {
        title: { text: 'Voltage (V)' }
    },
    credits: { enabled: false }
});

var chartP = new Highcharts.Chart({
    chart:{ renderTo:'chart-current' },
    title: { text: 'Battery Current' },
    series: [{
        showInLegend: false,
        data: []
    }],
    plotOptions: {
        line: { animation: false,
                dataLabels: { enabled: true }
              },
        series: { color: '#18009c' }
    },
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }
    },
    yAxis: {
        title: { text: 'Current (mA)' }
    },
    credits: { enabled: false }
});
