import random
import time
import machine

from microdot import Microdot
from authentication import api_key_required
from rate_limiter import rate_limit


def read_temperature_pico():
    sensor_temp = machine.ADC(4)  # ADC kanál 4 je teplotní senzor
    conversion_factor = 3.3 / (65535)  # Převodní faktor pro ADC
    reading = sensor_temp.read_u16() * conversion_factor  # Přečtěte hodnotu a převeďte
    temperature = 27 - (reading - 0.706) / 0.001721  # Vzorec pro převod na teplotu v Celsiu
    return temperature


# Vytvoření aplikace Microdot
app = Microdot()


@app.route('/')
async def index(request):
    return {'hello': 'world'}


@app.route('/temp')
@api_key_required
@rate_limit(max_requests=5, window_seconds=60)
async def temp(request):
    # Generování náhodné teploty pro demo účely
    temperature = random.uniform(20.0, 30.0)
    return {'temperature_pico': read_temperature_pico(),
            'temperature_air': temperature,
            'humidity': temperature,
            'timestamp': time.localtime()}


# Spuštění serveru
app.run(debug=True)
