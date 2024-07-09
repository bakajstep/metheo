import network
import time
import ntptime
import machine


ssid = 'biometeo'
password = 'iUDWBDjQJYxx'


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

ntptime.settime()
utc_time = time.localtime()
time_offset = 2 * 60 * 60
local_time = time.localtime(time.mktime(utc_time) + time_offset)
rtc = machine.RTC()
rtc.datetime((local_time[0], local_time[1], local_time[2], local_time[6], local_time[3], local_time[4], local_time[5], 0))
