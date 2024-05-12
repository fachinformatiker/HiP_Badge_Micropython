import utime, machine, time
from machine import Pin
from neopixel import NeoPixel

gray_button = 2
red_button = 8
black_button = 9

button_presses = 0 # the count of times the button has been pressed.  A is +1, B is -1
last_time = 0 # the last time we pressed the button

builtin_led = machine.Pin(7, machine.Pin.OUT)
button_gray = machine.Pin(gray_button, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_red = machine.Pin(red_button, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_black = machine.Pin(black_button, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Which GPIO pin is used to control the LEDs?
LED_DATA_PIN_NUMBER = 10
# How many LEDs does the board have in total?
LED_TOTAL_COUNT = 16
# Set up the Neopixel library, which is an easy way to control the LEDs.
led_pin = Pin(LED_DATA_PIN_NUMBER, Pin.OUT)
neopixel = NeoPixel(led_pin, LED_TOTAL_COUNT)

# this is the interrupt callback handler
# get in and out quickly
def button_callback(pin):
    global button_presses, last_time
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - last_time) > 200:
        # print(pin)
        if '14' in str(pin):
            button_presses +=1
        else:
            button_presses -= 1
        last_time = new_time

# now we register the handler functions when either of the buttons is pressed
button_gray.irq(trigger=machine.Pin.IRQ_FALLING, handler = button_callback)
button_red.irq(trigger=machine.Pin.IRQ_FALLING, handler = button_callback)
button_black.irq(trigger=machine.Pin.IRQ_FALLING, handler = button_callback)

while True:
    # only print on change in the button_presses value
    button_gray_first = button_gray.value()
    button_red_first = button_red.value()
    button_black_first = button_black.value()
    time.sleep(0.01)
    button_gray_second = button_gray.value()
    button_red_second = button_red.value()
    button_black_second = button_black.value()
    if button_gray_first and not button_gray_second:
        print('Button pressed!')
        neopixel[-2] = (0, 8, 0)
        neopixel.write()
    elif not button_gray_first and button_gray_second:
        print('Button released!')
        neopixel[-2] = (0, 0, 0)
        neopixel.write()
    elif button_red_first and not button_red_second:
        print('Button pressed!')
        for j in range(16):
            neopixel[j] = (8, 8, 8)
        neopixel.write()
    elif not button_red_first and button_red_second:
        print('Button released!')
        for j in range(16):
            neopixel[j] = (0, 0, 0)
        neopixel.write()
    elif button_black_first and not button_black_second:
        print('Button pressed!')
        neopixel[2] = (8, 0, 0)
        neopixel.write()
    elif not button_black_first and button_black_second:
        print('Button released!')
        neopixel[2] = (0, 0, 0)
        neopixel.write()

