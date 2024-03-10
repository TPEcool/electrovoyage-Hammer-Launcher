@echo off
"%~2\venv\Scripts\activate"
pip install pypresence | y
pip install pygetwindow | y
start "%~1\launcher\hammerlauncher.exe"