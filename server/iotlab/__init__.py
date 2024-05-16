import os


from flask import Flask
from flask_mqtt import Mqtt

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config['MQTTBROKER_URL'] = '192.168.146.131'
    app.config['MQTT_BROKER_PORT'] = '1883'
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 5
    app.config['MQTT_TLS_ENABLED'] = False
    mqtt = Mqtt()

    return app

import iotlab.views