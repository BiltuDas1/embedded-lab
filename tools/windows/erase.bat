@echo off
setlocal

REM This checks if arduino-cli is installed or not, otherwise it exit the program
where esptool >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo [ERROR] esptool is NOT in your Windows PATH.
  echo Please install esptool and then try again.
  exit /b %ERRORLEVEL%
)

call %~dp0config.bat

esptool --port %PORT% erase-flash