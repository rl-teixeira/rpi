console.log('simulations.js')
const context = document.getElementById('graph');

const data = {
    labels: [],
    datasets:[
        {
            label: 'Sensor',
            backgroundColor: 'rgba(75,192,192,0.2)',
            borderColor: 'rgba(75,192,192,1)',
            borderWidth: 1,
            hoverBackgroundColor: 'rgba(75,192,192,0.4)',
            hoverBorderColor: 'rgba(75,192,192,1)',
            data: []
        },
        {
            label: 'Actuator',
            backgroundColor: 'rgba(192,75,192,0.2)',
            borderColor: 'rgba(192,75,192,1)',
            borderWidth: 1,
            hoverBackgroundColor: 'rgba(192,75,192,0.4)',
            hoverBorderColor: 'rgba(192,75,192,1)',
            data: [] 
        },
        {
            label: 'Reference',
            backgroundColor: 'rgba(255,99,132,0.2)',
            borderColor: 'rgba(255,99,132,1)',
            borderWidth: 1,
            hoverBackgroundColor: 'rgba(255,99,132,0.4)',
            hoverBorderColor: 'rgba(255,99,132,1)',
            data: []
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

document.getElementById('start-sim-btn').addEventListener('click', async function () {
    const authResponse = await fetch('/get_auth_state');
    const authData = await authResponse.json();
    if(authData.is_logged_in){
        const stuNumber = document.cookie.split(';').find((row) => row.startsWith('stu_number'))?.split('=')[1];
        const btn = document.getElementById('start-sim-btn');
        btn.disabled = true;
        document.getElementById("graph-container").removeAttribute('hidden');
        try{
            const response = await fetch(`/start_experiment/${stuNumber}`);
            const result = await response.json();
            if(!result.success){
                console.error('Error',result.message);
                btn.disabled = false;
            }
        } catch (e){
            console.error('Error: ',e)
            btn.disabled = false;
        }
    } else {
        alert('Please log in!')
    }
})

async function checkAuthState() {
    try {
        const response = await fetch('/get_auth_state');
        const data = await response.json();
        if(data.is_logged_in){
            document.getElementById('sims-table-container').classList.remove('hidden');
            fetchSimulations();
            location.reload;
        } else {
            document.getElementById('start-sim-btn').disabled = true;
        }
    } catch(e){
        console.error('Error checking logged status: ', e);
    }
}

async function fetchSimulations() {
    const stuNumber = parseInt(document.cookie.split(';').find(cookie => cookie.includes('stu_number')).split('=')[1]);
    const response = await fetch(`/get_sims/${stuNumber}`)
    const data = await response.json();

    if(data.success){
        const table = document.querySelector('#sims-table tbody')
        table.innerHTML = '';
        data.files.forEach((entry) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.timestamp}</td>
                <td>${entry.file}</td>
            `
            table.appendChild(row);
            row.addEventListener('click', () => {
                document.getElementById("graph-container").classList.remove('hidden');
                plotSimulation(stuNumber, entry.file);
            })
        })
    }
}

async function plotSimulation(stuNumber, filename) {
    try {
        const response = await fetch(`/download_sim/${stuNumber}/${filename}`)
        const text = await response.text();
        const rows = text.split('\n').slice(1); //remove csv header
        //clear labels and data
        data.labels = []; 
        data.datasets[0].data = [];
        data.datasets[1].data = [];
        data.datasets[2].data = [];
        rows.forEach((row) => {
            const [t, r, u, y] = row.split(',');
            data.labels.push(t);
            data.datasets[0].data.push(y);
            data.datasets[1].data.push(u);
            data.datasets[2].data.push(r);
        })
        chart.update();
    } catch (e){
        console.error("Error ", e)
    }
}

const socket = io.connect('http://127.0.0.1:5000')

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

socket.on('sim_end', (msg)=> {
    document.getElementById('start-sim-btn').disabled = false;
    fetchSimulations();
})

/*window.onload = function(){
    checkAuthState();
    fetchSimulations();
}*/
document.addEventListener("DOMContentLoaded", () => {
    checkAuthState();
})