# controller/app_controller.py

import threading
import time
import json

from model.state import ScenarioState
from scenarios.scenario1 import Scenario1

class AppController:

    def __init__(self, mqtt, gpio, lcd, vision, voice, sensor, environment):

        self.mqtt = mqtt
        self.gpio = gpio
        self.lcd = lcd
        self.vision = vision
        self.voice = voice

        self.state = ScenarioState()

        self.scenario1 = Scenario1(
            lcd, vision, voice, gpio, mqtt, self.state
        )

        # =========================
        # 🌡️ DHT22 INTEGRATION
        # =========================
        self.sensor = sensor
        self.env = environment

        # start sensor loop automatically
        self.start_dht_loop()
        self.start_alarm_loop()

    # =========================
    # 🌡️ DHT22 LOOP
    # =========================
    def start_dht_loop(self):

        def loop():

            while True:

                data = self.sensor.read()

                if data:

                    temp = data["temp"]
                    humi = data["humi"]

                    # store in model
                    self.env.update(temp, humi)

                    # send to Node-RED
                    self.mqtt.publish(
                        "WSA2025/DHT22",
                        json.dumps({
                            "temp": temp,
                            "humi": humi
                        })
                    )

                    print(f"🌡 Temp: {temp} | 💧 Humi: {humi}")

                time.sleep(2)

        threading.Thread(target=loop, daemon=True).start()

    # =========================
    # ALARM SENSOR LOOP
    # =========================
    def start_alarm_loop(self):

        def loop():

            while True:

                if self.gpio.is_flame_detected():
                    self.scenario1.fire_detected()

                if self.gpio.is_smoke_detected():
                    self.scenario1.smoke_detected()

                time.sleep(0.2)

        threading.Thread(target=loop, daemon=True).start()

    # =========================
    # MQTT CALLBACK
    # =========================
    def turn_all_modules_off(self):
        self.gpio.all_off()

        for led in ("DO1", "DO2", "DO3", "DO4", "DO5", "DO6", "DO7", "DO8"):
            self.mqtt.publish(f"WSA2025/{led}", "OFF")

        self.mqtt.publish("WSA2025/MOTOR01", "OFF")
        self.mqtt.publish("WSA2025/BUZZER01", "OFF")

    def on_message(self, client, userdata, msg):

        topic = msg.topic
        payload = msg.payload.decode().strip()

        if topic == "WSA2025/DI1":

            if self.state.running:
                return

            command = payload.upper()

            if command in ("OFF", "LEAVE", "GOODBYE", "0"):
                threading.Thread(
                    target=self.scenario1.leave,
                    daemon=True
                ).start()
            elif not self.state.welcomed:
                threading.Thread(
                    target=self.scenario1.run,
                    daemon=True
                ).start()
            else:
                threading.Thread(
                    target=self.scenario1.leave,
                    daemon=True
                ).start()

        elif topic == "WSA2025/RELAY01":

            if payload.upper() == "ON":
                if not self.state.welcomed or not self.state.voice_detected:
                    return

                self.gpio.unlock()
            else:
                self.state.welcomed = False
                self.state.voice_detected = False
                self.turn_all_modules_off()

        elif topic.startswith("WSA2025/DO"):
                
                if not self.state.welcomed or not self.state.voice_detected:
                    return

                led = topic.split("/")[-1]

                if payload == "ON":
                    self.gpio.set_led(led, "ON")
                else:
                    self.gpio.set_led(led, "OFF")

        elif topic == "WSA2025/MOTOR01":

            if not self.state.welcomed or not self.state.voice_detected:
                return

            if payload.upper() == "OFF":
                self.gpio.stop_motor()
            else:
                self.gpio.set_motor_speed(payload)

        elif topic == "WSA2025/BUZZER01":

            if not self.state.welcomed or not self.state.voice_detected:
                return

            if payload.upper() == "ON":
                self.gpio.buzzer_on()
            else:
                self.gpio.buzzer_off()
