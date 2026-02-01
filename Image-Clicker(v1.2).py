# | Made by 2cz5 | https://github.com/2cz5 | Discord:2cz5 (for questions etc..)

import os
import sys
import traceback
from pathlib import Path

import sys
from pathlib import Path

# Ensure src is on sys.path so we can import the clicker package during development
ROOT = Path(__file__).parent
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from clicker.config import IMAGE_DIR, SUPPORTED_EXTS
from clicker.logging import setup_logging, get_logger
from clicker.killswitch import register_hotkey_with_fallback
from clicker.imaging import search_and_click

# Minimal entrypoint: collect templates, register killswitch, and run the search loop.
setup_logging()
logger = get_logger(__name__)


def main():
    image_paths = []
    if IMAGE_DIR.exists() and IMAGE_DIR.is_dir():
        for p in IMAGE_DIR.iterdir():
            if p.suffix.lower() in SUPPORTED_EXTS:
                image_paths.append(str(p))
    else:
        logger.error("Images directory not found: %s", IMAGE_DIR)
        return

    if not image_paths:
        logger.error("No image templates found in images/ — add .png/.jpg files to the images folder and re-run.")
        return

    register_hotkey_with_fallback()
    while True:
        search_and_click(image_paths)


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
