@echo off
REM run_image_clicker_from_dist.bat - wrapper to run the built app and keep the console open for diagnostics
REM Place this in the project root. It will run the exe from dist\Image-Clicker and pause so output is visible.

:: Adjust path if you used a different --name in PyInstaller or a different output folder
set DIST_DIR=%~dp0dist\Image-Clicker
if not exist "%DIST_DIR%\Image-Clicker.exe" (
  echo Could not find %DIST_DIR%\Image-Clicker.exe
  echo Make sure you copied the whole dist\Image-Clicker folder to this machine.
  pause
  exit /b 1
)

cd /d "%DIST_DIR%"
echo Running Image-Clicker.exe from %DIST_DIR%

REM Run the exe and let it print output; pause afterwards so window doesn't immediately close.
Image-Clicker.exe
set RC=%ERRORLEVEL%
echo Exit code: %RC%
pause
exit /b %RC%

