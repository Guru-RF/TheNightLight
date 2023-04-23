import alarm
import time
import board
from rainbowio import colorwheel
import neopixel
import rotaryio
import digitalio

pin_alarm = alarm.pin.PinAlarm(pin=board.GP18, value=False, pull=True)

encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP16)

button = digitalio.DigitalInOut(board.GP18)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

while button.value is False:
    time.sleep(0.001)

pixel_pin = board.GP21
num_pixels = 8

brightness=0.05

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=brightness, auto_write=False)

YELLOW = (200, 120, 00)

last_position = encoder.position
button_state = None

pixels.fill(YELLOW)
pixels.show()

while True:
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change*2):
            if brightness < 0.99:
                brightness=brightness+0.01
                pixels.brightness=brightness
                pixels.show()
    elif position_change < 0:
        for _ in range(-position_change*2):
            if brightness > 0.02:
                brightness=brightness-0.01
                pixels.brightness=brightness
                pixels.show()
    last_position = current_position
    if button.value and button_state == "pressed":
        brightness=0.00
        pixels.brightness=brightness
        pixels.show()
        button_state = None
        alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
    if not button.value and button_state is None:
        button_state = "pressed"