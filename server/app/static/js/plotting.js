//import { scales } from "/node_modules/chart.js";
//import {Chart} from "https://cdn.jsdelivr.net/npm/chart.js";
//import { Chart } from "/static/js/chart.js";
//const {Chart} = await import('chart.js');

console.log("ploting.js")

//Chart.register(...Chart.registerables); //idk why this is needed but it is

const context = document.getElementById('graph');

const data = {
    labels: [],
    datasets:[
        {
            label: 'Sensor Data',
            backgroundColor: 'rgba(75,192,192,0.2)',
            borderColor: 'rgba(75,192,192,1)',
            borderWidth: 1,
            hoverBackgroundColor: 'rgba(75,192,192,0.4)',
            hoverBorderColor: 'rgba(75,192,192,1)',
            data: []  // Sensor data readings
        },
        {
            label: 'Actuator Data',
            backgroundColor: 'rgba(192,75,192,0.2)',
            borderColor: 'rgba(192,75,192,1)',
            borderWidth: 1,
            hoverBackgroundColor: 'rgba(192,75,192,0.4)',
            hoverBorderColor: 'rgba(192,75,192,1)',
            data: []  // Actuator data readings
        }
    ]
}

const options = {
    responsive:true,
    scales: {
        y: {
            beginAtZero: true
        }
    }
}

const chart = new Chart(context, {
    type: 'line',
    data: data,
    options: options
});

const socket = io.connect('http://127.0.0.1:5000')
console.log(socket);

socket.on('connect', ()=>{
    console.log('Connected to server')
})

/*socket.on('message', (msg)=>{
    console.log("MQTT message received");
    const msg_json = JSON.parse(msg);
    const sensorData = msg_json.sensor;
    const actuatorData = msg_json.actuator;
    const timestamp = msg_json.timestamp;

    // push new data to both datasets with timestamp as label
    data.labels.push(timestamp);
    data.datasets[0].data.push(sensorData);
    data.datasets[1].data.push(actuatorData);

    // update chart
    chart.update();
})*/

socket.on('sim_update', (msg)=>{
    const msg_json = JSON.parse(msg);
    const referenceData = msg_json.reference;
    const sensorData = msg_json.sensor;
    const actuatorData = msg_json.actuator;
    const timestamp = msg_json.timestamp;

    data.labels.push(timestamp);
    data.datasets[0].data.push(sensorData);
    data.datasets[1].data.push(actuatorData);
    data.datasets[2].data.push(referenceData);

    chart.update();
})
socket.on('sim-end', (msg)=>{

})