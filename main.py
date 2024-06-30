import time
import uasyncio as asyncio

from microdot import Microdot
from authentication import api_key_required
from rate_limiter import rate_limit
from sensor_pico import SensorPico
from sensor_bmp import SensorBmp
from sensor_ds18b20 import SensorDS18b20

# Vytvoření aplikace Microdot
app = Microdot()

# Inicializace senzoru
bmp = SensorBmp()
ds18 = SensorDS18b20()
pico = SensorPico()


@app.route('/meteo')
@api_key_required
@rate_limit(max_requests=5, window_seconds=60)
async def temp(request):
    return {'temperature_pico': pico.read_temperature(),
            'temperature_air': bmp.read_temperature(),
            'temperature_water': ds18.read_temperature(),
            'pressure': bmp.read_pressure(),
            'altitude_ibf': bmp.altitude_ibf(),
            'timestamp': time.localtime()}


time.sleep(2)

# Spuštění serveru
app.run()
