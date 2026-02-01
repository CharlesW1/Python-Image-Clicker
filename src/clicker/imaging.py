import os
import time
import cv2
import numpy as np
import pyautogui
from .config import TEMPLATE_METHOD, DEFAULT_THRESHOLD, DEFAULT_CLICK_DELAY, DEFAULT_LOOP_DELAY
from .logging import get_logger
from .killswitch import killswitch_activated
from .window import minimize_cmd_window

logger = get_logger(__name__)


def search_and_click(images, threshold=DEFAULT_THRESHOLD, click_delay=DEFAULT_CLICK_DELAY, loop_delay=DEFAULT_LOOP_DELAY):
    method = TEMPLATE_METHOD

    while not killswitch_activated:
        time.sleep(loop_delay)
        minimize_cmd_window()

        screenshot = pyautogui.screenshot()
        screen_np = np.array(screenshot)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

        for image_path in images:
            if not os.path.exists(image_path):
                logger.error("Image not found at '%s'", image_path)
                continue

            template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                logger.error("Failed to load template image: %s", image_path)
                continue

            result = cv2.matchTemplate(screen_gray, template, method)
            loc = np.where(result >= threshold)

            if loc[0].size > 0:
                for pt in zip(*loc[::-1]):
                    x, y = pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2
                    pyautogui.click(x, y)
                    logger.info("Clicked on %s at (%d, %d)", image_path, x, y)
                    time.sleep(click_delay)

                    if killswitch_activated:
                        break

            if killswitch_activated:
                break

        if killswitch_activated:
            break
