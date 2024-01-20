@echo off
REM Wait for 60 seconds
timeout /T 60 /NOBREAK

REM Start ollama serve in WSL2 in the background
wsl -d Ubuntu -- bash -c "daemonize -e ~/ollama.log -o ~/ollama.log /usr/local/bin/ollama serve; true"


REM Change directory to the location of the .env file
cd C:\Users\danie\OneDrive\- Files -\Passion\Tech\AI\Mistral x Signal

REM Load SIGNAL_PHONE_NUMBER_TO_SEND_FROM from .env
for /F "delims== tokens=1,2" %%G in (.env) do (
    if "%%G"=="SIGNAL_PHONE_NUMBER_TO_SEND_FROM" set "SIGNAL_PHONE_NUMBER_TO_SEND_FROM=%%H"
)

REM Start signal-cli daemon in the background
start /B cmd /C "cd signal-cli\bin && signal-cli -a %SIGNAL_PHONE_NUMBER_TO_SEND_FROM% daemon --http localhost:11535 --receive-mode=manual >> signal-cli.log"

REM Wait for 60 seconds
timeout /T 60 /NOBREAK

REM Activate the virtual environment and run signal_mistral.py
call .venv\Scripts\activate
python signal_mistral.py
