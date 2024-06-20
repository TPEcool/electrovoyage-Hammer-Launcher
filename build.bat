@echo off
packer.exe -d resources -b "%~dp0"
move assets.packed resources
py -m PyInstaller --noconsole -y --add-data resources/logo.png;resources --add-data resources/assets.packed;resources --onefile --workpath temp --distpath HammerLauncher --clean launcher.py