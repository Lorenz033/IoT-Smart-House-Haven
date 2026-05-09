class EnvironmentModel:
    
    def __init__(self):
        self.temp = 0
        self.humi = 0

    def update(self, temp, humi):
        self.temp = temp
        self.humi = humi


