Chart.defaults.global.responsive = true;
Chart.defaults.global.legend.display = false;

$(document).ready(function () {
    const plugin = {
        id: 'custom_canvas_background_color',
        beforeDraw: (chart) => {
          const ctx = chart.canvas.getContext('2d');
          ctx.save();
          ctx.globalCompositeOperation = 'destination-over';
          ctx.fillStyle = 'rgb(239,239,239)';
          ctx.fillRect(0, 0, chart.width, chart.height);
          ctx.restore();  }
      };

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
        plugins: [plugin],
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
                        labelString: 'Fecha y Hora'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Flujo de agua'
                    }
                }]
            }
        }
    };

    const context = document.getElementById('numero1').getContext('2d');

    const lineChart = new Chart(context, config);

    const source = new EventSource("/flujo_tiempo_real");

    source.onmessage = function (event) {
        const data = JSON.parse(event.data);

        if (config.data.labels.length == 5) {
            config.data.labels.shift();
            config.data.datasets[0].data.shift();
        }

        config.data.labels.push(data.fecha);
        config.data.datasets[0].data.push(data.numero1);
        document.getElementById("flujo").innerHTML=data.numero1 + " L/m";
        lineChart.update();
    }
});