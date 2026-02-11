# Building a Windows executable for Python-Image-Clicker

This project can be packaged into a Windows executable using PyInstaller.

Recommended: build on a Windows machine (or WSL with wine, but not covered here). Use a virtual environment for a clean build.

Quick build steps (from project root):

1. Create and activate a venv (optional but recommended):

   python -m venv venv
   venv\Scripts\activate

2. Install dependencies:

   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python -m pip install pyinstaller

3. Run the provided build script (recommended):

   build_exe.bat

What the script does
- Installs deps (if not already installed)
- Runs PyInstaller in one-folder mode (`--onedir`) to produce `dist\Image-Clicker\Image-Clicker.exe`
- Bundles the `images` folder so the packaged app can access templates at runtime.

One-file vs one-folder
- The default in `build_exe.bat` is `--onedir` (one-folder). This is faster to build and makes it simpler to include asset folders like `images/`.
- If you want a single-file executable, replace `--onedir` with `--onefile` in the script and use `--add-data` the same way. Note: `--onefile` extracts at runtime and can be slower on startup.

Runtime notes
- The app uses the `keyboard` package which typically requires Administrator privileges on Windows to capture global key presses. Run the produced `.exe` as Administrator to allow the killswitch key to be detected.
- If you run with `--onefile`, PyInstaller extracts resources to a temporary folder at runtime; the script uses package-relative file paths, so the `images` folder will be available in the bundled app when using `--onedir`. For `--onefile`, the script will need to read files from the temporary extraction folder; PyInstaller sets a `_MEIPASS` environment to help with that. If you'd like, I can update the Python code to gracefully handle `--onefile` builds.

Testing the build
- Double-click `dist\Image-Clicker\Image-Clicker.exe` (or run from an elevated prompt).
- Ensure `images/` templates are present in the extracted directory (for onedir builds the folder is present next to the exe).

Follow-ups I can do for you
- Update `image_clicker.py` to support PyInstaller `--onefile` (`sys._MEIPASS`) automatically.
- Create an installer (NSIS or Inno Setup).
- Add code signing instructions or automation.

