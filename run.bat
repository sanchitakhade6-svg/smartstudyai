@echo off
setlocal
cd /d "%~dp0backend"
set PY=py -3.11

echo Installing/checking SmartStudy AI dependencies...
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Dependency installation failed. Make sure Python 3.11+ is installed.
  pause
  exit /b 1
)

echo.
echo Starting SmartStudy AI...
start "SmartStudy AI Backend" cmd /k "%PY% -m uvicorn main:app --host 127.0.0.1 --port 8000"
timeout /t 3 /nobreak >nul
start "" http://127.0.0.1:8000/app/

echo.
echo SmartStudy AI is opening at http://127.0.0.1:8000/app/
echo Keep the backend window open while using the app.
endlocal
