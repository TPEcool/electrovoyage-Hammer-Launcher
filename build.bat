@echo off
py -m PyInstaller --onefile -y --workpath temp/ --distpath "electrovoyage's Hammer Launcher" --upx-dir F:/upx --clean main.py
py -m PyInstaller --onefile --workpath temp_startup/ --distpath "Startup program" --upx-dir F:/upx --clean --add-binary "electrovoyage's Hammer Launcher/main.exe";"launcher" --add-data "startenv.bat";"launcher" launcher.py
rmdir /s /q "hammerlauncher"
py -m venv hammerlauncher --system-site-packages
move /Y hammerlauncher "Startup program"
rmdir /s /q "electrovoyage's Hammer Launcher"