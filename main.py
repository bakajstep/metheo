import gc
import time
import uasyncio as asyncio
from dep.microdot import Microdot, Response
import machine
import utime
import ujson
import ubinascii

from lib.sensor_pico import SensorPico
from lib.sensor_bmp import SensorBmp
from lib.sensor_ds18b20 import SensorDS18b20
from lib.wifi import connect_wifi

# Globální WiFi objekt
wlan = connect_wifi()

# Inicializace aplikace a senzorů
app = Microdot()
bmp = SensorBmp()
ds18 = SensorDS18b20()
pico = SensorPico()

# Async WiFi reconnect monitor
async def wifi_monitor():
    while True:
        if wlan is None or not wlan.isconnected():
            print("WiFi disconnected! Trying to reconnect...")
            connect_wifi()
        await asyncio.sleep(10)  # každých 10 sekund kontrola

@app.route('/status')
async def status(request):
    if wlan is not None and wlan.isconnected():
        ifconfig = wlan.ifconfig()
        ip_address, subnet_mask, gateway, dns_server = ifconfig
    else:
        ip_address = subnet_mask = gateway = dns_server = None
    status_info = {
        'device_id': ubinascii.hexlify(machine.unique_id()).decode(),
        'ip_address': ip_address,
        'subnet_mask': subnet_mask,
        'gateway': gateway,
        'dns_server': dns_server,
        'uptime': utime.ticks_ms() // 1000,  # v sekundách
        'free_memory': gc.mem_free()
    }
    return Response(body=ujson.dumps(status_info))

@app.route('/meteo')
async def meteo(request):
    try:
        return {
            'temperature_pico': pico.read_temperature(),
            'temperature_air': bmp.read_temperature(),
            'temperature_water': ds18.read_temperature(),
            'pressure': bmp.read_pressure(),
            'altitude_ibf': bmp.altitude_ibf(),
            'timestamp': time.localtime()
        }
    except Exception as e:
        return {'error': str(e)}, 500  # status 500, JSON s chybou

async def main():
    # Spusť WiFi monitor jako background task
    asyncio.create_task(wifi_monitor())
    # Počkej, než se stabilizuje připojení
    await asyncio.sleep(5)
    # Spusť Microdot server
    app.run()

# Start
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
