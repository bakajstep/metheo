import time
import machine


class SensorPico:
    def __init__(self):
        self.sensor_temp = machine.ADC(4)  # ADC kanál 4 je teplotní senzor
        self.conversion_factor = 3.3 / (65535)  # Převodní faktor pro ADC

    def read_temperature(self):
        reading = self.sensor_temp.read_u16() * self.conversion_factor  # Přečtěte hodnotu a převeďte
        temperature = 27 - (reading - 0.706) / 0.001721  # Vzorec pro převod na teplotu v Celsiu
        return temperature
