from PIL import Image
import time

import mss

time.sleep(1)

with mss.mss() as sct:
    # Get rid of the first, as it represents the "All in One" monitor:
    # Get raw pixels from the screen
    sct_img = sct.grab(sct.monitors[1])

    # Create the Image
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    # The same, but less efficient:
    # img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)

    # And save it!
    output = f"monitor-3.png"
    img.save(output)
    img.show()
    print(output)