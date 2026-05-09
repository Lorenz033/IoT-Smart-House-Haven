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
            voice_ok = self.voice.detect_command()
            
            if voice_ok:
                self.welcome()
            else:
                self.lcd.show("Voice Not Detected", "Access Denied")
        else:
            self.lcd.show("Face Not Detected", "Access Denied")

        self.state.running = False


    def welcome(self):
        self.state.welcomed = True
        self.lcd.show("WELCOME HOME", ":)")
        self.gpio.unlock()
        self.mqtt.publish("WSA2025/RELAY01", "ON")

    def leave(self):
        self.state.welcomed = False
        self.state.running = True

        self.lcd.show("GOODBYE")
        self.gpio.lock()
        self.mqtt.publish("WSA2025/RELAY01", "OFF")

        self.state.running = False