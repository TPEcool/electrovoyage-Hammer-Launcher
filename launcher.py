from ttkbootstrap import *
from srctools import keyvalues
import os
from richpresence import main as presence, stop as stoppresence
import threading

#system('rmdir /s /q hammerlauncher > nul')

# required to use files written into the executable
def getcwd() -> str:
    return os.path.dirname(__file__)

'''#print('Creating virtual environment...')
#venv.main(['hammerlauncher', '--system-site-packages'])

print('Launching Rich Presence...')
#print(listdir(getcwd()), listdir(getcwd() + '/launcher'))
#system(join(getcwd(), 'launcher', f'startenv.bat "{getcwd()}" "{_getcwd()}"'))
system(f'call "{_getcwd()}\hammerlauncher\Scripts\Activate.bat" && "{getcwd()}\launcher\\richpresence.exe"')'''

win = Window('electrovoyage\'s Hammer Launcher', 'litera', os.path.join(getcwd(), 'resources/logo.png'))
presencethread = threading.Thread(target=presence)
presencethread.start()

win.mainloop()