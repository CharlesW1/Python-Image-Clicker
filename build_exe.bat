@echo off
REM build_exe.bat - Build a distributable Windows application using PyInstaller
REM Usage: Open an elevated (Administrator) Developer PowerShell or CMD and run this from the project root.

REM Create a virtual environment in the project root if it doesn't exist, then activate it.
IF NOT EXIST "venv\Scripts\activate" (
  ECHO Creating virtual environment in %CD%\venv ...
  python -m venv venv
  IF %ERRORLEVEL% NEQ 0 (
    ECHO Failed to create virtual environment. Make sure Python is installed and on PATH.
    PAUSE
    EXIT /B %ERRORLEVEL%
  )
)

REM Activate the venv for the rest of the script (use CALL so control returns here)
CALL venv\Scripts\activate
IF %ERRORLEVEL% NEQ 0 (
  ECHO Failed to activate virtual environment.
  PAUSE
  EXIT /B %ERRORLEVEL%
)

REM Install required packages (will install into the venv)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist Image-Clicker.spec del /q Image-Clicker.spec

REM Ensure clicker.log exists so PyInstaller can add it as data without failing
IF NOT EXIST "clicker.log" (
  type NUL > clicker.log
)

REM Build: one-file (single exe). This bundles resources into a single executable.
REM Note: onefile extracts resources at runtime to a temp folder accessible via sys._MEIPASS
pyinstaller --noconfirm --clean --onefile --name "Image-Clicker" ^
  --add-data "images;images" ^
  --add-data "clicker.log;." ^
  "Image-Clicker(v1.2).py"

IF %ERRORLEVEL% NEQ 0 (
  ECHO PyInstaller failed with exit code %ERRORLEVEL%.
  PAUSE
  EXIT /B %ERRORLEVEL%
)

ECHO Build complete. See the dist\Image-Clicker folder.
PAUSE

