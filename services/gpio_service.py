import RPi.GPIO as GPIO

class GPIOService:

    def __init__(self, pin=18):

  
        self.pin = pin
        self.motor_speed = 0

  
        self.leds = {
            "DO1": 17,
            "DO2": 27,
            "DO3": 22,
            "DO4": 23
        }

        self.motor = {
            "ENA": 13,
            "IN1": 5,
            "IN2": 6
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

        # DC Motor with L298N
        GPIO.setup(self.motor["ENA"], GPIO.OUT)
        GPIO.setup(self.motor["IN1"], GPIO.OUT)
        GPIO.setup(self.motor["IN2"], GPIO.OUT)

        GPIO.output(self.motor["IN1"], GPIO.LOW)
        GPIO.output(self.motor["IN2"], GPIO.LOW)

        self.motor_pwm = GPIO.PWM(self.motor["ENA"], 1000)
        self.motor_pwm.start(0)

  
    def lock(self):
        GPIO.output(self.pin, GPIO.LOW)

    def unlock(self):
        GPIO.output(self.pin, GPIO.HIGH)

  
    def set_led(self, led, state):

        pin = self.leds.get(led)

        if pin is None:
            return
        GPIO.output(pin, GPIO.HIGH if state == "ON" else GPIO.LOW)

    def set_motor_speed(self, speed):

        try:
            speed = int(speed)
        except (TypeError, ValueError):
            return

        if speed not in (50, 75, 100):
            return

        self.motor_speed = speed
        GPIO.output(self.motor["IN1"], GPIO.HIGH)
        GPIO.output(self.motor["IN2"], GPIO.LOW)
        self.motor_pwm.ChangeDutyCycle(speed)

    def stop_motor(self):
        self.motor_speed = 0
        self.motor_pwm.ChangeDutyCycle(0)
        GPIO.output(self.motor["IN1"], GPIO.LOW)
        GPIO.output(self.motor["IN2"], GPIO.LOW)

    def cleanup(self):
        self.stop_motor()
        self.motor_pwm.stop()
        GPIO.cleanup()
