import sys
from pathlib import Path
import cv2

# Base directory for resources. When PyInstaller bundles the app with --onefile,
# resources are extracted at runtime to sys._MEIPASS. Otherwise use the script dir.
if getattr(sys, 'frozen', False):
    # PyInstaller onefile/frozen case
    base_dir = Path(sys._MEIPASS)
else:
    module_dir = Path(__file__).resolve().parent

    # Prefer a top-level `images/` directory if one exists in parent folders.
    # Walk up a few levels to find a repo-level images folder (helps when code is under src/).
    base_dir = module_dir
    for ancestor in [module_dir, module_dir.parent, module_dir.parent.parent, module_dir.parent.parent.parent]:
        candidate = ancestor / 'images'
        if candidate.exists() and candidate.is_dir():
            base_dir = ancestor
            break

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
LOG_LEVEL = 20  # logging.INFO

# Template matching method (cv2 constant)
TEMPLATE_METHOD = cv2.TM_CCOEFF_NORMED
