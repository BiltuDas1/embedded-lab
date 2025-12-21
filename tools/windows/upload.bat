@echo off
setlocal

REM This checks if arduino-cli is installed or not, otherwise it exit the program
where arduino-cli >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo [ERROR] arduino-cli is NOT in your Windows PATH.
  echo Please add the folder containing arduino-cli.exe to your Environment Variables.
  exit /b %ERRORLEVEL%
)

call %~dp0config.bat

arduino-cli upload -p %PORT% --fqbn %BOARD_ID% --input-dir "%~dp0..\..\build\%~1"