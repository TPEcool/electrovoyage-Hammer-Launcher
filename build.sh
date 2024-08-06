SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
./packer -d resources -b SCRIPT_DIR
python3 -m PyInstaller --noconsole -y --add-data resources/logo.png:resources --add-data resources/assets.packed:resources --onefile --workpath temp --distpath HammerLauncher --clean --hidden-import='PIL._tkinter_finder' launcher.py