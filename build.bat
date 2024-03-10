@echo off
py -m PyInstaller --onefile -y --workpath temp/ --distpath "electrovoyage's Hammer Launcher" --upx-dir F:/upx --clean main.py
py -m PyInstaller --onefile --workpath temp_startup/ --distpath "Startup program" --upx-dir F:/upx --clean --add-data "electrovoyage's Hammer Launcher/main.exe";"launcher" --add-data "startenv.bat";"launcher" startup.py
py -m venv hammerlauncher
move hammerlauncher "Startup program/venv" /Y
rmdir /s /q "electrovoyage's Hammer Launcher"