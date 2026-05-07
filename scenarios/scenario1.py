# scenarios/scenario1.py
import time

class Scenario1:
    def __init__(self, lcd, vision, voice, gpio, mqtt, state):
        self.lcd = lcd
        self.vision = vision
        self.voice = voice
        self.gpio = gpio
        self.mqtt = mqtt
        self.state = state

    def run(self):
        self.lcd.show("Booting...")

        face_ok = self.vision.detect_owner()

        if face_ok:
            self.lcd.show("Face Detected", "Checking Voice...")
            self.voice.detect_command()
            self.welcome()


        if not self.vision.detect_owner():
            self.lcd.show("Access Denied")
            return

        if not self.voice.detect_command():
            self.lcd.show("No Voice")
            return


    def welcome(self):
        self.state.welcomed = True
        self.state.running = True

        self.lcd.show("WELCOME HOME", ":)")
        self.gpio.unlock()
        self.mqtt.publish("WSA2025/RELAY01", "ON")

    def leave(self):
        self.state.welcomed = False
        self.state.running = True

        self.lcd.show("GOODBYE")
        self.gpio.lock()
        self.mqtt.publish("WSA2025/RELAY01", "OFF")