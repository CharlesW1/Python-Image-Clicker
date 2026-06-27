# LoL Auto-Accepter

A simple Windows tool that watches your screen during League of Legends queue and lobby screens, automatically clicks **Accept** when a match is found, and re-queues for another game. It works purely by looking at and clicking on your screen — it never reads or modifies any game files.

## Showcase|Example:

https://github.com/2cz5/Python-Image-Clicker/assets/169117434/c915386e-9d5f-44ef-9988-90ca2efb501b

## What it automates
- **Accept** — clicks the ready-check Accept button so you never miss a queue pop.
- **Find Match** — re-queues for another game once you're back at the client home screen.
- **Post-game** (full build only) — also clicks Play Again / Continue / Skip Waiting for Stats, so you don't have to babysit the post-game screens either.

## Prebuilt Executables
Each [release](https://github.com/CharlesW1/lol-auto-accepter/releases) publishes two standalone Windows executables — no Python install required:
- **`Image-Clicker-auto-accept.exe`** — accept-only: just clicks the ready-check Accept button, nothing else (no re-queue, no post-game).
- **`Image-Clicker-auto-queue.exe`** — the full loop: Accept, Find Match (re-queue), and the post-game buttons.

Download whichever one matches what you want automated and run it directly.

## Features
- **Image Recognition**: Uses OpenCV template matching to locate buttons on the screen.
- **Killswitch**: A global hotkey to pause/resume the script without closing it.
- **Logging**: Logs events and errors to `clicker.log` for debugging and monitoring.
- **Customizable**: Match threshold, click delay, and the killswitch key are all configurable.

## Requirements
- Python 3.10+
- OpenCV (`opencv-python`)
- NumPy
- PyAutoGUI
- pywin32
- keyboard

## Running from source
See [RUNNING.md](RUNNING.md) for full setup steps. In short:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python "Image-Clicker(v1.2).py"
```

## Building the executables
See [BUILD.md](BUILD.md), or just run `build_exe.bat`, which builds both the full `auto-queue` and the `auto-accept`-only executables.

## Configuration
Defaults live in `src/clicker/config.py`:
- `DEFAULT_THRESHOLD` (0.85) — template-matching sensitivity; higher is stricter.
- `DEFAULT_CLICK_DELAY` — delay in seconds between consecutive clicks.
- `DEFAULT_LOOP_DELAY` — delay between screen checks, to keep CPU usage low.
- `KILLSWITCH_KEY` (`[`) — the hotkey that pauses/resumes the script.

### Contributing:
Contributions are welcome! Feel free to open an issue or submit a pull request.

## Credits
- **Author**: 2cz5
- **GitHub**: [2cz5](https://github.com/2cz5)
- **Discord**: 2cz5 (for questions, feedback, etc.)
