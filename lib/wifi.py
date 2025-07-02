import network
import time

SSID = 'biometeo'
PASSWORD = 'iUDWBDjQJYxx'

def connect_wifi(timeout=20):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        for _ in range(timeout):
            if wlan.isconnected():
                print("WiFi connected:", wlan.ifconfig())
                return wlan
            time.sleep(1)
        print("WiFi connection failed!")
        return None
    else:
        print("WiFi already connected:", wlan.ifconfig())
        return wlan
