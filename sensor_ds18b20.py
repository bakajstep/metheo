from machine import Pin
import onewire, ds18x20
import time


class SensorDS18b20:
    def __init__(self, cache_duration=30):
        dat = Pin(4)
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(dat))
        self.roms = self.ds_sensor.scan()

        self.cache_duration = cache_duration
        self.last_read_time = 0
        self.temperature_cache = None

    def _update_cache(self):
        if len(self.roms) == 0:
            print("No DS18B20 sensors found!")
            self.temperature_cache = -1
        else:
            rom = self.roms[0]  # Předpokládáme, že je připojen pouze jeden senzor
            self.ds_sensor.convert_temp()
            time.sleep_ms(750)  # čekání na konverzi teploty
            self.temperature_cache = self.ds_sensor.read_temp(rom)
        self.last_read_time = time.time()

    def read_temperature(self):
        if time.time() - self.last_read_time > self.cache_duration or self.temperature_cache is None:
            self._update_cache()
        return self.temperature_cache
