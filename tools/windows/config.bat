@echo off

:: Load settings from config.env
for /f "tokens=*" %%i in (%~dp0../../config.env) do set %%i