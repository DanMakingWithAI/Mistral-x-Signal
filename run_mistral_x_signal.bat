@echo off
setlocal enabledelayedexpansion

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

:: Delete temporary error file before starting, if it exists
echo Deleting temporary signal-cli-errors-and-warnings.log if it exists
del signal-cli\bin\signal-cli-errors-and-warnings.log

REM Start signal-cli daemon in the background
:: Acknowledge on-screen
echo Starting signal-cli
start /B cmd /C "cd signal-cli\bin && signal-cli -a %SIGNAL_PHONE_NUMBER_TO_SEND_FROM% daemon --http localhost:11535 --receive-mode=manual >> signal-cli.log 2> signal-cli-errors-and-warnings.log"

:: Check for errors or warnings, after waiting a short while
timeout /T 10 /NOBREAK

:: Check all lines in signal-cli\bin\error.tmp to see if any begin with ERROR -
set is_error=0
set is_warning=0
for /f "tokens=*" %%i in ('type signal-cli\bin\signal-cli-errors-and-warnings.log') do (
    set line=%%i
    if "!line:~0,5!" == "ERROR" (
        set is_error=1
    ) else if "!line:~0,4!" == "WARN" (
        set is_warning=1
    )
)

if !is_error! == 1 (
    echo Error loading signal-cli, see signal-cli-errors-and-warnings.log for details
    exit /b 1
) else if !is_warning! == 1 (
    echo Warning generated by signal-cli, check signal-cli-errors-and-warnings.log file for details
) else (
    echo No errors or warnings from initial signal-cli startup
)
    
REM Activate the virtual environment and run signal_mistral.py
call .venv\Scripts\activate
python signal_mistral.py
