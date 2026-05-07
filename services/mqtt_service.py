import paho.mqtt.client as mqtt

class MQTTService:
    def __init__(self, broker="localhost", port=1883):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port

    def connect(self, on_connect, on_message, on_disconnect):
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect

        self.client.connect(self.broker, self.port, 60)
        return self.client