# view/lcd_view.py
from RPLCD.i2c import CharLCD
import time

class LCDView:
    def __init__(self):
        self.lcd = CharLCD(
            i2c_expander='PCF8574',
            address=0x27,
            port=1,
            cols=16,
            rows=2,
            charmap='A00'
        )
        self.show("System Ready")
        time.sleep(1)

    def show(self, line1, line2=""):
        self.lcd.clear()
        self.lcd.write_string(line1[:16])
        if line2:
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string(line2[:16])