# | Made by 2cz5 | https://github.com/2cz5 | Discord:2cz5 (for questions etc..)

import cv2
import numpy as np
import pyautogui
import threading
import time
import win32gui
import win32con
import keyboard
import os
from pathlib import Path
import logging

# -------------------------
# Configurable settings
# Edit these values at the top of the file to change behavior
# -------------------------
# Directory (relative to this script) that contains template images
IMAGE_DIR = Path(__file__).parent / "images"

# Supported image extensions for templates
SUPPORTED_EXTS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'}

# Template matching threshold (0-1). Higher -> stricter match
DEFAULT_THRESHOLD = 0.8

# Delay between clicks (seconds)
DEFAULT_CLICK_DELAY = 0.01

# Killswitch key (single character/string recognized by `keyboard`)
KILLSWITCH_KEY = 'q'

# Logging config
LOG_FILE = 'clicker.log'
LOG_LEVEL = logging.INFO

# Template matching method (cv2 constant)
TEMPLATE_METHOD = cv2.TM_CCOEFF_NORMED

# -------------------------

# Global variable to indicate if the killswitch is activated
killswitch_activated = False

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# Function to minimize the command prompt window (Windows-specific)
def minimize_cmd_window():
    try:
        # Find the command prompt window by its class name
        hwnd = win32gui.FindWindow("ConsoleWindowClass", None)
        if hwnd != 0:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    except Exception as e:
        logging.error(f"Error minimizing command prompt window: {e}")

# Function to monitor the killswitch key
def monitor_killswitch(killswitch_key):
    global killswitch_activated
    while True:
        if keyboard.is_pressed(killswitch_key):
            logging.info("Killswitch activated.")
            killswitch_activated = True
            break
        time.sleep(0.1)

# Function to search for images on the screen and click on them if found
def search_and_click(images, threshold=DEFAULT_THRESHOLD, click_delay=DEFAULT_CLICK_DELAY, killswitch_key=KILLSWITCH_KEY):
    # Set the template matching method
    method = TEMPLATE_METHOD

    # Start monitoring the killswitch key in a separate thread
    killswitch_thread = threading.Thread(target=monitor_killswitch, args=(killswitch_key,))
    killswitch_thread.start()

    while not killswitch_activated:
        minimize_cmd_window()  # Minimize the command prompt window

        # Capture the screen image
        screenshot = pyautogui.screenshot()
        screen_np = np.array(screenshot)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

        # Iterate through each image in the database
        for image_path in images:
            if not os.path.exists(image_path):
                logging.error(f"Image not found at '{image_path}'")
                continue  # Skip to the next image if the file doesn't exist

            # Load the image from the database
            template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                logging.error(f"Failed to load template image: {image_path}")
                continue

            # Perform template matching
            result = cv2.matchTemplate(screen_gray, template, method)

            # Get the location of matches above the specified threshold
            loc = np.where(result >= threshold)

            # Click on the matched locations
            if loc[0].size > 0:
                for pt in zip(*loc[::-1]):
                    # Calculate the center of the matched template
                    x, y = pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2

                    # Click on the center of the matched template
                    pyautogui.click(x, y)
                    logging.info(f"Clicked on {image_path} at ({x}, {y})")
                    time.sleep(click_delay)  # Delay between clicks

                    # Check if killswitch is activated after each click
                    if killswitch_activated:
                        break

            # Check if killswitch is activated after processing each image
            if killswitch_activated:
                break

        # Check if killswitch is activated after processing all images
        if killswitch_activated:
            break

    logging.info("Exiting the loop.")

# Main function to execute the script
def main():
    # List of image paths to search for on the screen
    # Collect image templates from the configured images directory
    image_paths = []
    if IMAGE_DIR.exists() and IMAGE_DIR.is_dir():
        for p in IMAGE_DIR.iterdir():
            if p.suffix.lower() in SUPPORTED_EXTS:
                image_paths.append(str(p))
    else:
        logging.error(f"Images directory not found: {IMAGE_DIR}")

    if not image_paths:
        logging.error("No image templates found in images/ — add .png/.jpg files to the images folder and re-run.")
        return

    # Call the function with the list of image paths and optional parameters
    search_and_click(image_paths)

# Entry point of the script
if __name__ == "__main__":
    main()
