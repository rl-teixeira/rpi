import os
import time
import webbrowser
import random

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'secret'
print("made app")

app.config['MQTTBROKER_URL'] = '192.168.146.131'
app.config['MQTT_BROKER_PORT'] = '1883'
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt()
print("made mqtt")


@app.route("/")
def index():
    # TODO: verify if logged in, if yes rediret to index, else redirect to login
    # return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/graph')
def graph():
    return render_template("graph.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            return redirect(url_for('home'))
        else: 
            flash('Invalid login', 'error')
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/data', methods = ['GET'])
def data():

    return jsonify(result=random.randint(0,10)) 


