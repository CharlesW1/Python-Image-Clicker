# | Made by 2cz5 | https://github.com/2cz5 | Discord:2cz5 (for questions etc..)

import os
import sys
import time
import traceback
from pathlib import Path

# Ensure src is on sys.path so we can import the clicker package during development
ROOT = Path(__file__).parent
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from clicker.config import IMAGE_DIR, SUPPORTED_EXTS
from clicker.logging import setup_logging, get_logger
from clicker import killswitch
from clicker.killswitch import register_hotkey_with_fallback
from clicker.imaging import search_and_click

# Minimal entrypoint: collect templates, register killswitch, and run the search loop.
setup_logging()
logger = get_logger(__name__)


def main():
    templates = []
    if IMAGE_DIR.exists() and IMAGE_DIR.is_dir():
        # rglob('*') finds images in all subfolders (common, 1600, 1900, etc.)
        import cv2
        for p in IMAGE_DIR.rglob('*'):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
                path_str = str(p)
                template = cv2.imread(path_str, cv2.IMREAD_GRAYSCALE)
                if template is not None:
                    templates.append((template, path_str))
                else:
                    logger.error("Failed to load template image: %s", path_str)
    else:
        logger.error("Images directory not found: %s", IMAGE_DIR)
        return

    if not templates:
        logger.error("No image templates found in images/ — add .png/.jpg files to the images folder and re-run.")
        return

    register_hotkey_with_fallback()
    while True:
        if killswitch.killswitch_activated:
            time.sleep(0.5)
            continue
        search_and_click(templates)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception in main")
        traceback.print_exc()
        try:
            if os.name == 'nt' and not sys.stdin.isatty():
                input("An error occurred. Press Enter to exit...")
        except Exception:
            pass
        raise
    else:
        try:
            if os.name == 'nt' and not sys.stdin.isatty():
                input("Press Enter to exit...")
        except Exception:
            pass
