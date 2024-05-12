from machine import Pin
from neopixel import NeoPixel
import machine
import time
import threading
import network
import socket

import secrets

# -- Define constants

network.country('DE')
switch = True

# Which GPIO pin is used to control the LEDs?
LED_DATA_PIN_NUMBER = 10
# How many LEDs does the board have in total?
LED_TOTAL_COUNT = 16

# -- Setup device

# Set up the Neopixel library, which is an easy way to control the LEDs.
led_pin = Pin(LED_DATA_PIN_NUMBER, Pin.OUT)
neopixel = NeoPixel(led_pin, LED_TOTAL_COUNT)

gray_button = Pin(2, Pin.IN)
red_button = Pin(8, Pin.IN)
black_button = Pin(9, Pin.IN)

# Define an array of colors
color_combinations = [
    # Transgender pride flag
    # [
    #    (255, 255, 255),
    #    (2, 186, 247),
    #    (247, 2, 239),
    #    (2, 186, 247),
    # ],
    # Pansexual pride flag
    # [
    #    (255, 2, 2),
    #    (243, 247, 2),
    #    (2, 80, 247),
    # ],
    # Gummy Worm!
    [
        (247, 2, 2),
        (247, 47, 2),
        (247, 149, 2),
        (222, 247, 2),
        (59, 247, 2),
        (2, 247, 112),
        (2, 247, 231),
        (2, 108, 247),
        (2, 10, 247),
        (75, 2, 247),
        (149, 2, 247),
        (194, 2, 247),
        (247, 2, 223),
        (247, 2, 169),
        (247, 2, 116),
        (247, 2, 59),
    ]
]

color_combination_index = 0

# Set brightness by multiplying all color values with a value between 0 and 1
brightness_levels = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]    

def demo(neopixel):
    n = neopixel.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            neopixel[j] = (0, 0, 0)
        neopixel[i % n] = (255, 255, 255)
        neopixel.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            neopixel[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            neopixel[i % n] = (0, 0, 0)
        else:
            neopixel[n - 1 - (i % n)] = (0, 0, 0)
        neopixel.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xFF
            else:
                val = 255 - (i & 0xFF)
            neopixel[j] = (val, 0, 0)
        neopixel.write()

    # clear
    for i in range(n):
        neopixel[i] = (0, 0, 0)
    neopixel.write()


def heartbeat():
    ii = 0
    ramp_delay = 0.001
    beat_delay = 0.25
    skip_interval = 10

    while ii < 10:
        # ramp brightness up using the ramp_delay
        for i in range(0, 255, skip_interval):
            neopixel[0] = (i, 0, 0)
            neopixel.write()
            time.sleep(ramp_delay)
        # ramp brightness down using the same delay
        for i in range(255, 0, -skip_interval):
            neopixel[0] = (i, 0, 0)
            neopixel.write()
            time.sleep(ramp_delay)
        neopixel[0] = (0, 0, 0)
        neopixel.write()
        time.sleep(beat_delay)
        ii += 1


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(wait):
    global LED_TOTAL_COUNT, neopixel
    for j in range(255):
        for i in range(LED_TOTAL_COUNT):
            rc_index = (i * 256 // LED_TOTAL_COUNT) + j
            # print(rc_index)
            neopixel[i] = wheel(rc_index & 255)
        neopixel.write()
    time.sleep(wait)


def demo3():
    iii = 0
    counter = 0
    while iii < 5:
        print("Running cycle", counter)
        rainbow_cycle(0.05)
        counter += 1
        iii += 1


def white_light(neopixel):
    n = neopixel.n
    i = 0
    iiii = 0
    for i in range(n):
        neopixel[i] = (255, 255, 255)
    neopixel.write()
    while iiii < 1:
        print("white light for ", iiii, " seconds")
        time.sleep(1)
        iiii += 1


def around(count):
    ii = 0
    n = neopixel.n
    while ii < count:
        for i in range(n):
            for j in range(n):
                neopixel[j] = (0, 0, 0)
            neopixel[i % n] = (255, 255, 255)
            neopixel.write()
            time.sleep_ms(25)
        ii += 1
    neopixel[i] = (0, 8, 0)
    neopixel.write()


def read_pins():
    black_button_value = black_button.value()
    gray_button_value = gray_button.value()
    red_button_value = red_button.value()
    if black_button_value == 0 and red_button_value == 0:
        return False
    elif red_button_value == 0 and gray_button_value == 0:
        return False
    elif red_button_value == 0:
        white_light(neopixel)
    elif black_button_value == 0:
        demo(neopixel)
    elif gray_button_value == 0:
        rainbow_cycle(1)
    else:
        return False
    return True

def blink_red():
    n = neopixel.n
    i = 0
    wait = 0.05
    for i in range(n):
        neopixel[i] = (255, 0, 0)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 0, 0)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (255, 0, 0)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 0, 0)
    neopixel.write()

def blink_green():
    n = neopixel.n
    i = 0
    wait = 0.05
    for i in range(n):
        neopixel[i] = (0, 255, 0)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 0, 0)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 255, 0)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 0, 0)
    neopixel.write()

def blink_blue():
    n = neopixel.n
    i = 0
    wait = 0.05
    for i in range(n):
        neopixel[i] = (0, 0, 255)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 0, 0)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 0, 255)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 0, 0)
    neopixel.write()

def blink_rgb():
    n = neopixel.n
    i = 0
    wait = 0.05
    for i in range(n):
        neopixel[i] = (255, 0, 0)
    neopixel.write()
    time.sleep(2 * wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 255, 0)
    neopixel.write()
    time.sleep(2 * wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 0, 255)
    neopixel.write()
    time.sleep(wait)
    i = 0
    for i in range(n):
        neopixel[i] = (0, 0, 0)
    neopixel.write()
    time.sleep(wait)

def disconnect_from_wifi():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
        print('WLAN-Verbindung beendet')
        blink_red()
        time.sleep(2)

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('WLAN-Verbindung herstellen:', secrets.WiFi_Name)
        wlan.active(True)
        wlan.connect(secrets.WiFi_Name, secrets.WiFi_Pass)
        for i in range(10):
            if wlan.status() == 1010:
                break
            print('.', wlan.status())
            time.sleep(1)
        time.sleep(1)
    if wlan.isconnected():
        print('WLAN-Verbindung hergestellt')
        blink_green()
        print('WLAN-Status:', wlan.status())
        netConfig = wlan.ifconfig()
        print('IPv4-Adresse:', netConfig[0], '/', netConfig[1])
        print('Standard-Gateway:', netConfig[2])
        print('DNS-Server:', netConfig[3])
    else:
        print('Keine WLAN-Verbindung')
        blink_red()
        print('WLAN-Status:', wlan.status())

def sock():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    sock = socket.socket(socket.AF_INET)
    sock.bind(addr)
    print('listening on', addr)
    sock.listen(5)
    sock.accept()
    print('client connected from', addr)

disconnect_from_wifi()
connect_to_wifi()
#sock()
#blink_blue()

print("hello from within the code before the while loop! :D")

while True:
    if read_pins():
        around(1)
        time.sleep(0.1)
        
print("hello after the while loop")