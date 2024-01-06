@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
start pythonw "%~dp0定时关机.py"