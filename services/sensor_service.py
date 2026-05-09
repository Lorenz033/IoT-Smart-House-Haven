import board
import adafruit_dht

class SensorService:

    def __init__(self, pin=4):
        self.dht = adafruit_dht.DHT22(board.D4)

    def read(self):
        try:
            temp = self.dht.temperature
            humi = self.dht.humidity

            if temp is None or humi is None:
                return None

            return {
                "temp": round(temp, 1),
                "humi": round(humi, 1)
            }

        except RuntimeError as e:
            print("DHT error:", e)
            return None