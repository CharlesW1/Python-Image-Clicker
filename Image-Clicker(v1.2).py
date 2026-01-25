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
import sys
import traceback

# -------------------------
# Configurable settings
# Edit these values at the top of the file to change behavior
# -------------------------
# Base directory for resources. When PyInstaller bundles the app with --onefile,
# resources are extracted at runtime to sys._MEIPASS. Otherwise use the script dir.
if getattr(sys, 'frozen', False):
    # PyInstaller onefile/frozen case
    base_dir = Path(sys._MEIPASS)
else:
    base_dir = Path(__file__).parent

# Directory (relative to base_dir) that contains template images
IMAGE_DIR = base_dir / "images"

# Supported image extensions for templates
SUPPORTED_EXTS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'}

# Template matching threshold (0-1). Higher -> stricter match
DEFAULT_THRESHOLD = 0.85

# Delay between clicks (seconds)
DEFAULT_CLICK_DELAY = 0.5

# Delay between successive screen checks to reduce CPU usage (seconds)
DEFAULT_LOOP_DELAY = 0.1

# Killswitch key (single character/string recognized by `keyboard`)
KILLSWITCH_KEY = '['

# Logging config
# Write logs to the current working directory so the file is writable at runtime
LOG_FILE = str(Path.cwd() / 'clicker.log')
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
def toggle_killswitch():
    """Toggle the killswitch state and log/print status."""
    global killswitch_activated
    killswitch_activated = not killswitch_activated
    logging.info("Killswitch toggled to %s", "ON" if not killswitch_activated else "OFF")
    print(f"Auto Accept toggled to {'ON' if not killswitch_activated else 'OFF'}.")

# Function to search for images on the screen and click on them if found
def search_and_click(images, threshold=DEFAULT_THRESHOLD, click_delay=DEFAULT_CLICK_DELAY, loop_delay=DEFAULT_LOOP_DELAY):
    # Set the template matching method
    method = TEMPLATE_METHOD

    while not killswitch_activated:
        # Sleep a short time between iterations to reduce CPU and input lag
        time.sleep(loop_delay)
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
    
    # Register a hotkey to toggle killswitch (non-blocking). If registration fails,
    # fall back to a polling thread so functionality remains.
    try:
        keyboard.add_hotkey(KILLSWITCH_KEY, toggle_killswitch)
        logging.info("Registered hotkey for killswitch: %s", KILLSWITCH_KEY)
    except Exception as e:
        logging.warning("Could not register hotkey; falling back to polling: %s", e)
        def fallback_monitor():
            while True:
                try:
                    if keyboard.is_pressed(KILLSWITCH_KEY):
                        toggle_killswitch()
                        time.sleep(1.5)
                except Exception:
                    # keyboard may raise if not permitted; keep looping but don't crash
                    pass
                time.sleep(DEFAULT_LOOP_DELAY)

        killswitch_thread = threading.Thread(target=fallback_monitor, daemon=True)
        killswitch_thread.start()

    # Call the function with the list of image paths and optional parameters
    while True:
        search_and_click(image_paths)

# Entry point of the script with error handling and an exit pause when appropriate
if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Log and print traceback so users running the bundled exe can see the error
        logging.exception("Unhandled exception in main")
        traceback.print_exc()
        try:
            # On Windows, if the exe was double-clicked the stdin is typically not a TTY.
            # Pause so the terminal window remains visible for the user to read the error.
            if os.name == 'nt' and not sys.stdin.isatty():
                input("An error occurred. Press Enter to exit...")
        except Exception:
            pass
        # Re-raise to allow the process to exit with a non-zero code if desired
        raise
    else:
        # Normal exit: if run by double-click (non-interactive), pause so the window doesn't close immediately
        try:
            if os.name == 'nt' and not sys.stdin.isatty():
                input("Press Enter to exit...")
        except Exception:
            pass
