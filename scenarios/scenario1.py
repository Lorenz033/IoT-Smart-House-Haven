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
        self.lcd.show("Scanning Owner...")

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
        self.state.voice_detected = True
        self.lcd.show("WELCOME HOME", ":)")
        self.gpio.unlock()
        self.gpio.set_motor_speed(50)
        self.mqtt.publish("WSA2025/RELAY01", "ON")
        self.mqtt.publish("WSA2025/DO1", "ON")
        self.mqtt.publish("WSA2025/DO2", "ON")
        self.mqtt.publish("WSA2025/DO3", "ON")
        self.mqtt.publish("WSA2025/DO4", "ON")
        self.mqtt.publish("WSA2025/MOTOR01", "50")

    def leave(self):
        self.state.welcomed = False
        self.state.running = True
        self.lcd.show("GOODBYE")
        self.gpio.lock()
        self.gpio.stop_motor()
        self.mqtt.publish("WSA2025/RELAY01", "OFF")
        self.mqtt.publish("WSA2025/DO1", "OFF")
        self.mqtt.publish("WSA2025/DO2", "OFF")
        self.mqtt.publish("WSA2025/DO3", "OFF")
        self.mqtt.publish("WSA2025/DO4", "OFF")
        self.mqtt.publish("WSA2025/MOTOR01", "OFF")
        self.state.running = False

