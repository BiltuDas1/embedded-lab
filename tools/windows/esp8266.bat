@echo off

REM This checks if arduino-cli is installed or not, otherwise it exit the program
where arduino-cli >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo [ERROR] arduino-cli is NOT in your Windows PATH.
  echo Please add the folder containing arduino-cli.exe to your Environment Variables.
  exit /b %ERRORLEVEL%
)

:: Add the ESP8266 index
arduino-cli config add board_manager.additional_urls http://arduino.esp8266.com/stable/package_esp8266com_index.json

:: Update and Install
arduino-cli core update-index
arduino-cli core install esp8266:esp8266