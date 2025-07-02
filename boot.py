from lib.wifi import connect_wifi
import ntptime
import time
import machine

def set_time_from_ntp():
    try:
        ntptime.settime()
        print("Time set from NTP.")
    except Exception as e:
        print("NTP failed:", e)

def set_local_rtc(offset_hours=2):
    utc_time = time.localtime()
    time_offset = offset_hours * 60 * 60
    local_time = time.localtime(time.mktime(utc_time) + time_offset)
    rtc = machine.RTC()
    rtc.datetime((
        local_time[0], local_time[1], local_time[2],
        local_time[6],
        local_time[3], local_time[4], local_time[5], 0
    ))
    print("RTC set to local time:", rtc.datetime())

print("WiFi a čas initialization...")
wlan = connect_wifi()
if wlan and wlan.isconnected():
    set_time_from_ntp()
    set_local_rtc(offset_hours=2)
else:
    print("Boot: WiFi not connected, RTC not set!")
