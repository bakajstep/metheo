import gc
import time
import uasyncio as asyncio

from microdot import Microdot, Response
import network
import machine
import utime
import ujson
import ubinascii
from sensor_pico import SensorPico
from sensor_bmp import SensorBmp
from sensor_ds18b20 import SensorDS18b20

# Vytvoření aplikace Microdot
app = Microdot()

# Inicializace senzoru
bmp = SensorBmp()
ds18 = SensorDS18b20()
pico = SensorPico()


@app.route('/status')
async def status(request):
        wlan = network.WLAN(network.STA_IF)
        ifconfig = wlan.ifconfig()

        status_info = {
                'device_id': ubinascii.hexlify(machine.unique_id()).decode(),
                'ip_address': ifconfig[0],
                'subnet_mask': ifconfig[1],
                'gateway': ifconfig[2],
                'dns_server': ifconfig[3],
                'uptime': utime.ticks_ms() // 1000,  # Uptime v sekundách
                'free_memory': gc.mem_free()
        }

        return Response(body=ujson.dumps(status_info))

@app.route('/meteo')
async def temp(request):
    return {'temperature_pico': pico.read_temperature(),
            'temperature_air': bmp.read_temperature(),
            'temperature_water': ds18.read_temperature(),
            'pressure': bmp.read_pressure(),
            'altitude_ibf': bmp.altitude_ibf(),
            'timestamp': time.localtime()}


time.sleep(15)

# Spuštění serveru
app.run()
