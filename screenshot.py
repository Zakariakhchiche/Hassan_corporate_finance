import ctypes
from PIL import ImageGrab
import os

def take_screenshot():
    # Capture the whole screen
    screenshot = ImageGrab.grab()
    screenshot.save("C:\\Users\\zkhch\\.openclaw\\workspace\\screen.png")
    print("Screenshot saved to workspace as screen.png")

if __name__ == "__main__":
    take_screenshot()
