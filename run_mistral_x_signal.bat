@echo off
setlocal

REM Wait for 60 seconds
REM timeout /T 60 /NOBREAK - Superfluous wait now that we are not loading Ollama in this script

REM Start ollama serve in WSL2 in the background
REM We no longer need to do this part as Ollama can be installed to Windows to auto-start - we assume that now
REM wsl -d Ubuntu -- bash -c "daemonize -e ~/ollama.log -o ~/ollama.log /usr/local/bin/ollama serve; true"


REM Change directory to the location of the .env file
cd C:\Users\danie\OneDrive\- Files -\Passion\Tech\AI\Mistral x Signal

REM Load SIGNAL_PHONE_NUMBER_TO_SEND_FROM from .env
for /F "delims== tokens=1,2" %%G in (.env) do (
    if "%%G"=="SIGNAL_PHONE_NUMBER_TO_SEND_FROM" set "SIGNAL_PHONE_NUMBER_TO_SEND_FROM=%%H"
)

REM Start signal-cli daemon in the background
start /B cmd /C "cd signal-cli\bin && signal-cli -a %SIGNAL_PHONE_NUMBER_TO_SEND_FROM% daemon --http localhost:11535 --receive-mode=manual >> signal-cli.log 2> error.tmp"

:: Check if error.tmp exists, after waiting a short while
timeout /T 10 /NOBREAK
if exist signal-cli\bin\error.tmp (
    :: Acknowledge on-screen
    echo Error loading signal-cli, see signal-cli-error.log for details

    :: Append the error message to the error log file
    echo [%date% %time%] Error code: %errorlevel%. Error message: >> signal-cli\bin\signal-cli-error.log
    type signal-cli\bin\error.tmp >> signal-cli\bin\signal-cli-error.log

    :: Delete the temporary error file
    del signal-cli\bin\error.tmp

    :: Exit the script with error code 1
    exit /b 1
)
    
REM Activate the virtual environment and run signal_mistral.py
call .venv\Scripts\activate
python signal_mistral.py
