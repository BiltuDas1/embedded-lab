@echo off
setlocal

REM This checks if arduino-cli is installed or not, otherwise it exit the program
where arduino-cli >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo [ERROR] arduino-cli is NOT in your Windows PATH.
  echo Please add the folder containing arduino-cli.exe to your Environment Variables.
  exit /b %ERRORLEVEL%
)

REM Main task starts here
call %~dp0config.bat

for %%I in ("%~1") do set "FOLDER_NAME=%%~nxI"
set BUILD_DIR=%~dp0..\..\build
set BUILD_FOLDER=%BUILD_DIR%\%FOLDER_NAME%

arduino-cli compile --fqbn %BOARD_ID% "%~1" --build-property "build.extra_flags=-I%~dp0..\..\shared" --warnings all --output-dir "%BUILD_FOLDER%"

if %ERRORLEVEL% equ 0 (
  echo %FOLDER_NAME%>%BUILD_DIR%\lastbuild.txt
)