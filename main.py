# main.py
import time
from services.mqtt_service import MQTTService
from services.gpio_service import GPIOService
from view.lcd_view import LCDView
from services.vision_service import VisionService
from services.voice_service import VoiceService
from controller.app_controller import AppController

BROKER = "localhost"
PORT = 1883

TOPIC_DI1 = "WSA2025/DI1"
TOPIC_RELAY = "WSA2025/RELAY01"

# Init components
mqtt_service = MQTTService(BROKER, PORT)
gpio = GPIOService(18)
lcd = LCDView()

vision = VisionService("/home/lorenz/iothings/models/manny.pkl")

voice = VoiceService(
    "/home/lorenz/iothings/models/vosk-model-small-en-us-0.15",
    mic_index=0
)

controller = AppController(
    mqtt_service.client,
    gpio,
    lcd,
    vision,
    voice
)

client = mqtt_service.connect(
    on_connect=lambda c,u,f,rc: c.subscribe([(TOPIC_DI1,0),(TOPIC_RELAY,0)]),
    on_message=controller.on_message,
    on_disconnect=lambda c,u,rc: print("Disconnected")
)

print("System running...")
client.loop_forever()