$(document).ready(function() {

    // Global variable to store actice devices
    var currentDevices = [];
    var currentChartConfigs = {};
    var currentCharts = {};

    function createDeviceCharts(event) {

        // Parse event data
        const data = JSON.parse(event.data);

        // Iterate over each device id and create a chart
        Object.keys(data).forEach(function(id, index) {

            // Update charts if they exist
            if (currentDevices.includes(id)) {

                currentChartConfigs[id].data.labels = data[id].time;
                currentChartConfigs[id].data.datasets[0].data = data[id].x;
                currentChartConfigs[id].data.datasets[1].data = data[id].y;
                currentChartConfigs[id].data.datasets[2].data = data[id].z;
                currentCharts[id].update();

                return

            }

            let canvas = document.createElement('canvas');
            canvas.setAttribute('id', id);
            canvas.setAttribute('width', '100');
            canvas.setAttribute('height', '50');
            let canvasContainer = document.createElement('div');
            canvasContainer.appendChild(canvas);
            document.getElementById("main-container").appendChild(canvasContainer);

            currentDevices.push(id);

            var ctx = document.getElementById(id).getContext("2d");

            currentChartConfigs[id] = {
                type: 'line',
                data: {
                    labels: data[id].time,
                    datasets: [{
                        label: "X",
                        backgroundColor: 'blue',
                        borderColor: 'blue',
                        data: data[id].x,
                        fill: false,
                    }, {
                        label: "Y",
                        backgroundColor: 'orange',
                        borderColor: 'orange',
                        data: data[id].y,
                        fill: false,
                    }, {
                        label: "Z",
                        backgroundColor: 'green',
                        borderColor: 'green',
                        data: data[id].z,
                        fill: false,
                    }],
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Accelerometer signal for ' + id
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
                                labelString: 'Time'
                            }
                        }],
                        yAxes: [{
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Value'
                            }
                        }]
                    }
                }
            };

            currentCharts[id] = new Chart(ctx, currentChartConfigs[id]);

        });


    }

    const source = new EventSource("http://127.0.0.1:8080/chart-data");

    source.addEventListener("new_message", function(event) {

        createDeviceCharts(event);

    });

});