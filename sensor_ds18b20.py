from machine import Pin
import onewire, ds18x20
import time


class SensorDS18b20:
    def __init__(self):
        dat = Pin(4)
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(dat))
        self.roms = self.ds_sensor.scan()

    def read_temperature(self):
        if len(self.roms) == 0:
            print("No DS18B20 sensors found!")
            return -1
        else:
            rom = self.roms[0]  # Předpokládáme, že je připojen pouze jeden senzor
            self.ds_sensor.convert_temp()
            time.sleep_ms(750)  # čekání na konverzi teploty
            temp_ds = self.ds_sensor.read_temp(rom)
            return temp_ds
