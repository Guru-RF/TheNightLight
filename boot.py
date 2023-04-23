import usb_cdc
import board
import storage
from digitalio import DigitalInOut, Direction, Pull

btn = DigitalInOut(board.GP18)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

# Disable devices only if dah/dit is not pressed.
if btn.value is True:
    print(f"boot: button not pressed, disabling drive")
    storage.disable_usb_drive()
    storage.remount("/", readonly=False)

    usb_cdc.enable(console=False, data=True)
else:
    print(f"boot: button pressed, enable console, enabling drive")

    usb_cdc.enable(console=True, data=True)

    new_name = "NiLight"
    storage.remount("/", readonly=False)
    m = storage.getmount("/")
    m.label = new_name
    storage.remount("/", readonly=True)
