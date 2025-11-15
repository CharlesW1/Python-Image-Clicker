Python-Image-Clicker — Quick start (Windows PowerShell, Python 3.10)

1) Create and activate a virtual environment

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2) Upgrade pip and install dependencies

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

3) Notes
- `keyboard` may require running PowerShell as Administrator for global hotkey detection.
- `pyautogui` depends on `pillow` (included) and may require additional accessibility permissions.
- OpenCV (`opencv-python`) on Windows installs prebuilt wheels; if you need optimised builds, follow OpenCV docs.
- If you see errors during install, paste the error and I can help troubleshoot.
