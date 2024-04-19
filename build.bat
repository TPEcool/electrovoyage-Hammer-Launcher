@echo off
py -m PyInstaller --onefile -y --workpath temp/ --distpath "RP main" --upx-dir F:/upx --clean richpresence.py
py -m PyInstaller --onefile --workpath temp_startup/ --distpath "RP startup program" --upx-dir F:/upx --clean --add-binary "RP main/richpresence.exe";"launcher" --add-data "startenv.bat";"launcher" launcher.py
rmdir /s /q "hammerlauncher"
py -m venv hammerlauncher --system-site-packages
move /Y hammerlauncher "RP startup program"
rmdir /s /q "RP main"