print('electrovoyage\'s Hammer Launcher')

#import venv
from os.path import dirname, join
from os import system, getcwd as _getcwd

system('rmdir /s /q hammerlauncher > nul')

# required to use files written into the executable
def getcwd() -> str:
    return dirname(__file__)

#print('Creating virtual environment...')
#venv.main(['hammerlauncher'])

print('Launching Rich Presence...')
system(join(getcwd(), 'launcher', f'startenv.bat "{getcwd()}" "{_getcwd()}"'))