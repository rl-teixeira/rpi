import os

from flask import Flask
from flask_mqtt import Mqtt

def create_app():

    app = Flask(__name__, instance_relative_config=True)
    print("made app")

    app.config['MQTTBROKER_URL'] = '192.168.146.131'
    app.config['MQTT_BROKER_PORT'] = '1883'
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 5
    app.config['MQTT_TLS_ENABLED'] = False
    mqtt = Mqtt()
    print("made mqtt")

    return app

app = create_app()

@app.route("/home")
def home():
    return render_template("home.html")
    