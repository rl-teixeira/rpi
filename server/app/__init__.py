from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

from app.routes import register_routes
from config import Config

import os

mqtt = Mqtt()
socketio = SocketIO()

def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    try:
        mqtt.init_app(app)
        from app.mqtt_app import register_mqtt_handlers
        register_mqtt_handlers(mqtt)
    except:
        print("No connection to MQTT broker")
    register_routes(app)
    socketio.init_app(app)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    return app