import os
import time
import cv2
import numpy as np
import pyautogui
from .config import TEMPLATE_METHOD, DEFAULT_THRESHOLD, DEFAULT_CLICK_DELAY, DEFAULT_LOOP_DELAY
from .logging import get_logger
from . import killswitch
from .window import minimize_cmd_window

logger = get_logger(__name__)


def search_and_click(templates, threshold=DEFAULT_THRESHOLD, click_delay=DEFAULT_CLICK_DELAY, loop_delay=DEFAULT_LOOP_DELAY):
    """
    Search for multiple templates on screen and click if found.
    templates: List of tuples (template_cv2_image, image_path)
    """
    method = TEMPLATE_METHOD

    # Minimize once at the start of the loop
    minimize_cmd_window()

    while not killswitch.killswitch_activated:
        time.sleep(loop_delay)

        screenshot = pyautogui.screenshot()
        screen_np = np.array(screenshot)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

        for template, image_path in templates:
            result = cv2.matchTemplate(screen_gray, template, method)
            loc = np.where(result >= threshold)

            if loc[0].size > 0:
                for pt in zip(*loc[::-1]):
                    x, y = pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2
                    pyautogui.click(x, y)
                    logger.info("Clicked on %s at (%d, %d)", image_path, x, y)
                    # Re-minimize in case the click brought some window to front or if it was restored
                    minimize_cmd_window()
                    time.sleep(click_delay)

                    if killswitch.killswitch_activated:
                        break
            if killswitch.killswitch_activated:
                break
        if killswitch.killswitch_activated:
            break
