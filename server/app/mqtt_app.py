import json
from datetime import datetime

latest_sensor_y = None

def register_mqtt_handlers(mqtt):
    global actuator

    #handle the event when the broker responds to a connection request
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        mqtt.subscribe('home/sensor')
        print('Subscribed to home/sensor')

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        global actuator
        print('MQTT Message received')
        data_received = dict (
            topic = message.topic,
            payload = message.payload.decode()
        )
        print(data_received)
        from app import mqtt
        match data_received.topic:
            case 'home/sensor':
                #get u from controller, to string, to byte array
                #actuator = 0#str(controller(y, r)).encode() 
                latest_sensor_y = data_received["payload"]
                #send u to actuator
                send_u(actuator)
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
            case _:
                return

def control_mode(control_mode):
    from app import mqtt
    mqtt.publish('home/control_mode',control_mode, qos=1)

def send_u(actuator):
    from app import mqtt
    mqtt.publish('home/actuator',int(actuator).to_bytes(1,'big'))

def get_latest_sensor_y():
    return latest_sensor_y
