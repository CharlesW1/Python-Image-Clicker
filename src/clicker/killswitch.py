import threading
import time
import keyboard
from .config import KILLSWITCH_KEY, DEFAULT_LOOP_DELAY
from .logging import get_logger

logger = get_logger(__name__)

# Simple killswitch state (module-global)
killswitch_activated = False


def toggle_killswitch():
    """Toggle the killswitch state and log/print status."""
    global killswitch_activated
    killswitch_activated = not killswitch_activated
    logger.info("Killswitch toggled to %s", "ON" if not killswitch_activated else "OFF")
    print(f"Auto Accept toggled to {'ON' if not killswitch_activated else 'OFF'}.")


def register_hotkey_with_fallback():
    """Try to register a hotkey; if it fails, start a polling thread as fallback."""
    try:
        keyboard.add_hotkey(KILLSWITCH_KEY, toggle_killswitch)
        logger.info("Registered hotkey for killswitch: %s", KILLSWITCH_KEY)
        return None
    except Exception as e:
        logger.warning("Could not register hotkey; falling back to polling: %s", e)

        def fallback_monitor():
            while True:
                try:
                    if keyboard.is_pressed(KILLSWITCH_KEY):
                        toggle_killswitch()
                        time.sleep(1.5)
                except Exception:
                    pass
                time.sleep(DEFAULT_LOOP_DELAY)

        t = threading.Thread(target=fallback_monitor, daemon=True)
        t.start()
        return t
