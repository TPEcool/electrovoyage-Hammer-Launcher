import venv
import os

print('Creating virtual environment...')
venv.main(['hammerlauncher', '--system-site-packages'])

print('Starting...')
os.system('call "hammerlauncher/Scripts/activate.bat" && py richpresence.py')