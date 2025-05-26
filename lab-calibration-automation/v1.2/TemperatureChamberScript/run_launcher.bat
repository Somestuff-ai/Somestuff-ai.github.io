@echo off
REM Locate the Anaconda environment directory
@echo off
REM Locate the Anaconda environment directory
echo Activating Anaconda environment...
call C:\Users\gpt\AppData\Local\anaconda3\Scripts\activate.bat base

REM Check if the environment is activated
if %errorlevel% neq 0 (
    echo Failed to activate Anaconda environment
    pause
    exit /b 1
)

REM Change directory to the script location
echo Changing directory to script location...
cd /d C:\Users\gpt\Desktop\TempScriptRD\TemperatureChamberScript

REM Locate the Launcher.py directory 
echo Running Python script...
echo Current directory:
cd
dir

python Launcher.py

if %errorlevel% neq 0 (
    echo Failed to run Python script
    pause
    exit /b 1
)

REM Pause to keep the command prompt window open
echo Script execution finished
pause