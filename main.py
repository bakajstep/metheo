import random
import time

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


@app.route('/')
async def index(request):
    return {'hello': 'world'}


@app.route('/temp')
@api_key_required
@rate_limit(max_requests=5, window_seconds=60)
async def temp(request):
    return {'temperature_pico': pico.read_temperature(),
            'temperature_air': bmp.read_temperature(),
            'temperature_water': ds18.read_temperature(),
            'pressure': bmp.read_pressure(),
            'timestamp': time.localtime()}


# Spuštění serveru
app.run(debug=True)
