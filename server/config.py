import os

class Config:
    secret_key = 'secret'
    MQTT_BROKER_URL = '192.168.1.74'
    MQTT_BROKER_PORT = 1883
    MQTT_USERNAME = ''
    MQTT_PASSWORD = ''
    MQTT_KEEPALIVE = 5
    MQTT_TLS_ENABLED = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(),'instance','uploads')
    MAX_CONTENT_LENGTH = 10*1024*1024 #file size limit 10MB