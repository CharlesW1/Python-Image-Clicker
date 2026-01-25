@echo off
REM run_image_clicker.bat
REM Double-click to run Image-Clicker(v1.2).py using the default python
REM Resolve script directory and use it for paths (%%~dp0 ends with a backslash)
SET "SCRIPT_DIR=%~dp0"
SET "PY_SCRIPT=%SCRIPT_DIR%Image-Clicker(v1.2).py"
IF NOT EXIST "%PY_SCRIPT%" (
  ECHO Python script not found: %PY_SCRIPT%
  PAUSE
  EXIT /B 1
)

REM Prefer virtualenv in project if present
SET "VENV_DIR=%SCRIPT_DIR%venv"
IF EXIST "%VENV_DIR%\Scripts\python.exe" (
  SET "PY=%VENV_DIR%\Scripts\python.exe"
) ELSE (
  REM Allow overriding python via PYTHON_CMD environment variable
  IF DEFINED PYTHON_CMD (
    SET "PY=%PYTHON_CMD%"
  ) ELSE (
    SET "PY=python"
  )
)

"%PY%" "%PY_SCRIPT%" %*
PAUSE
