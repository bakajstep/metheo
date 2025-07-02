import time
import machine


class SensorPico:
    def __init__(self, cache_duration=30):
        self.sensor_temp = machine.ADC(4)  # ADC kanál 4 je teplotní senzor
        self.conversion_factor = 3.3 / 65535  # Převodní faktor pro ADC

        self.cache_duration = cache_duration
        self.last_read_time = 0
        self.temperature_cache = None

    def _update_cache(self):
        reading = self.sensor_temp.read_u16() * self.conversion_factor  # Přečtěte hodnotu a převeďte
        temperature = 27 - (reading - 0.706) / 0.001721  # Vzorec pro převod na teplotu v Celsiu
        self.temperature_cache = temperature
        self.last_read_time = time.time()

    def read_temperature(self):
        if time.time() - self.last_read_time > self.cache_duration or self.temperature_cache is None:
            self._update_cache()
        return self.temperature_cache
