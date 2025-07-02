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

def safe_read(fn, fallback=None):
    try:
        return fn()
    except Exception as e:
        print(f"Read failed: {fn.__name__} - {e}")
        return fallback

@app.route('/meteo')
async def meteo(request):
    return {
        'temperature_pico': safe_read(lambda: pico.read_temperature(), fallback='error'),
        'temperature_air': safe_read(lambda: bmp.read_temperature(), fallback='error'),
        'temperature_water': safe_read(lambda: ds18.read_temperature(), fallback='error'),
        'pressure': safe_read(lambda: bmp.read_pressure(), fallback='error'),
        'altitude_ibf': safe_read(lambda: bmp.altitude_ibf(), fallback='error'),
        'timestamp': safe_read(lambda: time.localtime(), fallback='error')
    }

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
