import json
from datetime import datetime

def register_mqtt_handlers(mqtt):
    global actuator

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
        from app import socketio
        socketio.send(json.dumps(data_to_send))