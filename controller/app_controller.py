# controller/app_controller.py
import threading
from model.state import ScenarioState
from scenarios.scenario1 import Scenario1

class AppController:
    def __init__(self, mqtt, gpio, lcd, vision, voice):
        self.state = ScenarioState()

        self.scenario1 = Scenario1(
            lcd, vision, voice, gpio, mqtt, self.state
        )

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        if topic == "WSA2025/DI1":

            if self.state.running:
                return

            if not self.state.welcomed:
                threading.Thread(target=self.scenario1.run, daemon=True).start()
            else:
                threading.Thread(target=self.scenario1.leave, daemon=True).start()

        elif topic == "WSA2025/RELAY01":

            if payload == "ON":
                self.scenario1.gpio.lock()
            else:
                self.scenario1.gpio.unlock()