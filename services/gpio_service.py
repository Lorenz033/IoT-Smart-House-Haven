import RPi.GPIO as GPIO

class GPIOService:

    def __init__(
        self,
        pin=18,
        flame_pin=24,
        smoke_pin=26,
        buzzer_pin=25,
        flame_active_low=True,
        smoke_active_low=True
    ):

  
        self.pin = pin
        self.flame_pin = flame_pin
        self.smoke_pin = smoke_pin
        self.buzzer_pin = buzzer_pin
        self.flame_active_low = flame_active_low
        self.smoke_active_low = smoke_active_low
        self.motor_speed = 0

  
        self.leds = {
            "DO1": 17,
            "DO2": 27,
            "DO3": 22,
            "DO4": 23,
            "DO5": 16,
            "DO6": 20,
            "DO7": 12,
            "DO8": 21
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

        # Flame sensor and buzzer
        flame_pull_mode = GPIO.PUD_UP if self.flame_active_low else GPIO.PUD_DOWN
        GPIO.setup(self.flame_pin, GPIO.IN, pull_up_down=flame_pull_mode)

        # Smoke sensor
        smoke_pull_mode = GPIO.PUD_UP if self.smoke_active_low else GPIO.PUD_DOWN
        GPIO.setup(self.smoke_pin, GPIO.IN, pull_up_down=smoke_pull_mode)

        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.output(self.buzzer_pin, GPIO.LOW)

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

    def is_flame_detected(self):
        flame_state = GPIO.input(self.flame_pin)

        if self.flame_active_low:
            return flame_state == GPIO.LOW
        return flame_state == GPIO.HIGH

    def is_smoke_detected(self):
        smoke_state = GPIO.input(self.smoke_pin)

        if self.smoke_active_low:
            return smoke_state == GPIO.LOW
        return smoke_state == GPIO.HIGH

    def buzzer_on(self):
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def buzzer_off(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)

  
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

    def all_off(self):
        self.lock()
        self.stop_motor()
        self.buzzer_off()

        for led in self.leds:
            self.set_led(led, "OFF")

    def cleanup(self):
        self.all_off()
        self.motor_pwm.stop()
        GPIO.cleanup()
