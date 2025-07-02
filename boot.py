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
    # 1. Získej UTC čas
    utc_time = time.time()  # sekundy od epochy (v UTC)
    # 2. Přičti offset (v sekundách)
    local_epoch = utc_time + (offset_hours * 3600)
    # 3. Rozbal na pole (MicroPython localtime/UTC stejný výstup)
    local_time = time.localtime(local_epoch)
    # 4. Převeď weekday (0=Mon...6=Sun) -> (1=Mon...7=Sun)
    weekday = local_time[6] + 1
    rtc = machine.RTC()
    rtc.datetime((
        local_time[0],  # year
        local_time[1],  # month
        local_time[2],  # day
        weekday,
        local_time[3],  # hour
        local_time[4],  # minute
        local_time[5],  # second
        0               # subsecond
    ))
    print("local_time", local_time)
    print("rtc.datetime:", rtc.datetime())

print("WiFi a čas initialization...")
wlan = connect_wifi()
if wlan and wlan.isconnected():
    set_time_from_ntp()
    set_local_rtc(offset_hours=2)
else:
    print("Boot: WiFi not connected, RTC not set!")
