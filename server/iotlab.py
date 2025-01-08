import os
import time
import webbrowser
import random
from datetime import datetime

import eventlet
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_mqtt import Mqtt
import paho.mqtt.client as mqtt_client #imports constants from paho
from flask_socketio import SocketIO, emit
import json

#eventlet.monkey_patch()

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'secret'

app.config['MQTT_BROKER_URL'] = '192.168.1.74'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
try:
    mqtt = Mqtt(app)
    mqtt.subscribe('home/sensor')
    print('Subscribed to home/sensor')
except:
    print("No connection to MQTT broker")
    mqtt = Mqtt()
socketio = SocketIO(app)
#socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)

actuator = 0

@app.route("/")  
def index():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    user_email = request.cookies.get('email')
    is_logged_in = user_email is not None
    return render_template("index.html", is_logged_in=is_logged_in)

@app.route('/graph')
def graph():
    return render_template("graph.html")

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        response = make_response(redirect(url_for('home')))
        if "fct.unl.pt" in email:
            response.set_cookie('email', email, max_age=60*60*24*2)
        return response
    #return render_template("login.html")

@app.route("/upload", methods=['POST'])
def upload():
    return render_template("upload.html")

@app.route('/data', methods = ['GET'])
def data():
    return jsonify(result=random.randint(0,10)) 

@app.route('/button_test_page')
def button_test_page():
    return render_template("button_test.html")

@app.route('/mqtt_test', methods=['POST'])
def mqtt_test():
    global actuator
    actuator = request.form['message']
    (result, mid) = mqtt.publish('home/actuator', int(actuator).to_bytes(1,'big'))
    if(result == mqtt_client.MQTT_ERR_SUCCESS):
        print("MQTT message success - " + actuator)
    else:
        print("MQTT message failed. Error: " + result)
    return redirect(url_for('graph'))

@app.route('/socket_test', methods=['POST'])
def socket_test():
    message = request.form['ping']
    socketio.send('ping')
    return redirect(url_for('graph'))

#handle the event when the broker responds to a connection request
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('home/sensor')
    print('Subscribed to home/sensor')

#the only message received is sensor data
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global actuator
    print('MQTT Message received')
    data_received = dict (
        topic = message.topic,
        payload = message.payload.decode()
    )
    print(data_received)
    #get u from controller, to string, to byte array
    #actuator = 0#str(controller(y, r)).encode() 
    #send u to actuator
    mqtt.publish('home/actuator',int(actuator).to_bytes(1,'big'))
    print(actuator)
    #sends to the websocket
    data_to_send = {
        "topic":data_received["topic"],
        "sensor": data_received["payload"],
        "actuator": actuator,
        "timestamp": datetime.now().isoformat()
    }
    socketio.send(json.dumps(data_to_send))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)