from machine import Pin, I2C
from bmp280 import *
import time


class SensorBmp:
    def __init__(self, cache_duration=30):
        i2c = I2C(0, scl=Pin(9), sda=Pin(8))
        devices = i2c.scan()
        self.bmp280_object = BMP280(i2c, addr=devices[0], use_case=BMP280_CASE_WEATHER)
        self.bmp280_object.power_mode = BMP280_POWER_NORMAL
        self.bmp280_object.oversample = BMP280_OS_HIGH
        self.bmp280_object.temp_os = BMP280_TEMP_OS_8
        self.bmp280_object.press_os = BMP280_TEMP_OS_4
        self.bmp280_object.standby = BMP280_STANDBY_250
        self.bmp280_object.iir = BMP280_IIR_FILTER_2

        self.cache_duration = cache_duration
        self.last_read_time = 0
        self.temperature_cache = None
        self.pressure_cache = None
        self.altitude_hyp_cache = None
        self.altitude_ibf_cache = None

    def _update_cache(self):
        self.temperature_cache = self.bmp280_object.temperature
        self.pressure_cache = (self.bmp280_object.pressure * 0.01) - 3
        self.altitude_hyp_cache = self._compute_altitude_hyp()
        self.altitude_ibf_cache = self._compute_altitude_ibf()
        self.last_read_time = time.time()

    def read_temperature(self):
        if time.time() - self.last_read_time > self.cache_duration or self.temperature_cache is None:
            self._update_cache()
        return self.temperature_cache

    def read_pressure(self):
        if time.time() - self.last_read_time > self.cache_duration or self.pressure_cache is None:
            self._update_cache()
        return self.pressure_cache

    def altitude_hyp(self):
        if time.time() - self.last_read_time > self.cache_duration or self.altitude_hyp_cache is None:
            self._update_cache()
        return self.altitude_hyp_cache

    def altitude_ibf(self):
        if time.time() - self.last_read_time > self.cache_duration or self.altitude_ibf_cache is None:
            self._update_cache()
        return self.altitude_ibf_cache

    def _compute_altitude_hyp(self):
        # Hypsometric Equation (Max Altitude < 11 Km above sea level)
        temperature = self.bmp280_object.temperature
        local_pressure = (self.bmp280_object.pressure * 0.01) - 3
        sea_level_pressure = 1013.25  # hPa
        pressure_ratio = sea_level_pressure / local_pressure  # sea level pressure = 1013.25 hPa
        h = (((pressure_ratio ** (1 / 5.257)) - 1) * temperature) / 0.0065
        return h

    def _compute_altitude_ibf(self):
        # Altitude from international barometric formula, given in BMP 180 datasheet
        local_pressure = (self.bmp280_object.pressure * 0.01) - 3  # Unit : hPa
        sea_level_pressure = 1013.25  # Unit : hPa
        pressure_ratio = local_pressure / sea_level_pressure
        altitude = 44330 * (1 - (pressure_ratio ** (1 / 5.255)))
        return altitude
