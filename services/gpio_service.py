import RPi.GPIO as GPIO

class GPIOService:
    def __init__(self, pin=18):
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def lock(self):
        GPIO.output(self.pin, GPIO.LOW)

    def unlock(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def cleanup(self):
        GPIO.cleanup()