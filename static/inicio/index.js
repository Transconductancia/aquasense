Chart.defaults.global.responsive = true;
Chart.defaults.global.legend.display = false;

$(document).ready(function () {
    const config = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "Numero 1",
                backgroundColor: "rgb(132,186,91,0.2)",
                borderColor: "rgb(62,150,81,1)",
                data: [],
                fill: false,
            }],
        },
        options: {
            responsive: true,
            title: {
                display: true,
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Fecha de adquisición'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Unidad'
                    }
                }]
            }
        }
    };

    const context = document.getElementById('numero1').getContext('2d');

    const lineChart = new Chart(context, config);

    const source = new EventSource("/datos_monitoreo");

    source.onmessage = function (event) {
        const data = JSON.parse(event.data);

        if (config.data.labels.length == 20) {
            config.data.labels.shift();
            config.data.datasets[0].data.shift();
        }

        config.data.labels.push(data.fecha);
        config.data.datasets[0].data.push(data.numero1);
        lineChart.update();
    }
});