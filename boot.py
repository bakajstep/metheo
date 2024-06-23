import network
import time

ssid = 'Bakaj'
password = 'uvodojemu1234'


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Connecting to network...")
        time.sleep(1)

    if wlan.isconnected():
        print("Connected to network!")
        print(wlan.ifconfig())
    else:
        print("Failed to connect to network")


print("Connecting to your wifi...")
connect()
