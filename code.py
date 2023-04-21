import time
import board
from rainbowio import colorwheel
import neopixel
import rotaryio
import digitalio

encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP16)

button = digitalio.DigitalInOut(board.GP18)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

pixel_pin = board.GP21
num_pixels = 8

brightness=0.05

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=brightness, auto_write=False)

YELLOW = (255, 150, 40)

last_position = encoder.position
button_state = None

pixels.fill(YELLOW)
pixels.show()

while True:
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            if brightness < 0.99:
                brightness=brightness+0.01
                pixels.brightness=brightness
                pixels.show()
                print(str(brightness))
    elif position_change < 0:
        for _ in range(-position_change):
            if brightness > 0.02:
                brightness=brightness-0.01
                pixels.brightness=brightness
                pixels.show()
                print(str(brightness))
    last_position = current_position
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button pressed.")
        brightness=0.00
        pixels.brightness=brightness
        pixels.show()
        button_state = None