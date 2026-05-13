import RPi.GPIO as GPIO

class GPIOService:

    def __init__(self, pin=18):

  
        self.pin = pin

  
        self.leds = {
            "DO1": 17,
            "DO2": 27,
            "DO3": 22,
            "DO4": 23
        }

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Relay
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

        # LEDs
        for led_pin in self.leds.values():
            GPIO.setup(led_pin, GPIO.OUT)
            GPIO.output(led_pin, GPIO.LOW)

  
    def lock(self):
        GPIO.output(self.pin, GPIO.LOW)

    def unlock(self):
        GPIO.output(self.pin, GPIO.HIGH)

  
    def set_led(self, led, state):

        pin = self.leds.get(led)

        if pin is None:
            return
        GPIO.output(pin, GPIO.HIGH if state == "ON" else GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()