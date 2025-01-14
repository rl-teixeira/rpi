from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import os

mqtt = Mqtt()
socketio = SocketIO()


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    try:
        mqtt.init_app(app)
        from app.mqtt_handlers import register_mqtt_handlers
        register_mqtt_handlers(mqtt)
    except:
        print("No connection to MQTT broker")
    socketio.init_app(app)
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app