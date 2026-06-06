# scenarios/scenario1.py
import time

FIRE_STATUS_TOPIC = "WSA2025/FIRE_STATUS"
FIRE_STATUS_MESSAGE = "Fire Detected"
SMOKE_STATUS_TOPIC = "WSA2025/SMOKE_STATUS"
SMOKE_STATUS_MESSAGE = "Smoke Detected"

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
            self.gpio.buzzer_on()
            time.sleep(0.2)
            self.gpio.buzzer_off()
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
        self.lcd.show("GOODBYE: Locked")
        self.gpio.lock()
        self.gpio.stop_motor()
        self.gpio.buzzer_off()

        for led in ("DO1", "DO2", "DO3", "DO4"):
            self.gpio.set_led(led, "OFF")

        self.mqtt.publish("WSA2025/RELAY01", "OFF")
        self.mqtt.publish("WSA2025/DO1", "OFF")
        self.mqtt.publish("WSA2025/DO2", "OFF")
        self.mqtt.publish("WSA2025/DO3", "OFF")
        self.mqtt.publish("WSA2025/DO4", "OFF")
        self.mqtt.publish("WSA2025/MOTOR01", "OFF")
        self.mqtt.publish("WSA2025/BUZZER01", "OFF")
        self.state.voice_detected = False
        self.state.running = False

    def fire_detected(self):
        if self.state.fire_detected:
            return

        self.state.fire_detected = True
        self.gpio.buzzer_on()
        self.lcd.show("FIRE DETECTED", "Buzzer ON")
        self.mqtt.publish(FIRE_STATUS_TOPIC, FIRE_STATUS_MESSAGE)

    def smoke_detected(self):
        if self.state.smoke_detected:
            return


        self.state.smoke_detected = True
        self.gpio.buzzer_on()
        self.lcd.show("SMOKE DETECTED", "Buzzer ON")
        self.mqtt.publish(SMOKE_STATUS_TOPIC, SMOKE_STATUS_MESSAGE)
