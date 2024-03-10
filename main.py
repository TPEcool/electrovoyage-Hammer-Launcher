from os import path

'''system('rmdir /s /q hammerlauncher')
print('Setting up virtual environment...')
venv.main(['hammerlauncher'])

print('Setting up virtual environment...')
system('hammerlauncher\Scripts\\activate && pip install pygetwindow --yes && pip install pypresence --yes')'''

import pygetwindow as gw
from pypresence import Presence, DiscordNotFound
import time

old_hammername = ''
hammer_name = ''
starttime = time.time()

print('Setting up rich presence:')
try:
    rpc = Presence('1216087154581573803', pipe=0)
    print('\t1/3 - Rich Presence set up')
    rpc.connect()
    print('\t2/3 - Rich Presence connected')
    rpc.update(
        details='Idling',
        state='electrovoyage\'s Hammer Launcher is open',
        start = time.time(),
        large_image='hammerlauncher',
        large_text='electrovoyage\'s Hammer Launcher'
    )
    print('\t3/3 - Rich Presence set')
except DiscordNotFound:
    print('Discord not found, failed to start Rich Presence')

FOUND, IDLE, MISSING = (0, 1, 2)

while True:
    hammer_state = None
    # Get a list of all windows
    windows_list = gw.getAllWindows()

    # Extract names of all windows
    window_names = [window.title for window in windows_list]

    # Print the list of window names
    #print('Searching for Hammer...')
    for name in window_names:

        #print('Hammer - ' in name) 
        if 'Hammer - [' in name:
            hammer_state = FOUND

            if old_hammername != hammer_name:
                starttime = time.time()

            old_hammername = hammer_name
            hammer_name = name
        elif name == 'Hammer':
            hammer_state = IDLE
        else:
            hammer_state = MISSING

    # Extract the 'path to file' part
    if hammer_state is FOUND:
        path_to_file = path.basename(hammer_name.split('-')[1].strip().split('-')[0].strip()[1:-1])

        try:
            rpc.update(
                details='Editing a map',
                state=f'Editing {path_to_file}',
                start = starttime,
                large_image='hammerlauncher',
                large_text='electrovoyage\'s Hammer Launcher'
            )
        except DiscordNotFound:
            print('Discord not found, failed to start Rich Presence')
        except NameError:
            pass
    elif hammer_state is IDLE:
        try:
            rpc.update(
                details='Idling',
                state='electrovoyage\'s Hammer Launcher is open',
                start = starttime,
                large_image='hammerlauncher',
                large_text='electrovoyage\'s Hammer Launcher'
            )
        except DiscordNotFound:
            print('Discord not found, failed to start Rich Presence')

'''
discord_APPID = '1132691764755578910'

def setPresence(filename:str | None):
    try:
        startTime.set(int(time.time()))
        rpc = Presence(discord_APPID, pipe = 0)
        rpc.connect()
        rpc.update(
            state = 'In Game',
            details = 'File: '+('none' if filename is None else '\''+os.path.basename(filename)+'\''),
            start = startTime.get(),
            large_image = 'beemmx_r',
            large_text = 'beeMMX R is a tool which generates music packages for BEE2. Learn more by clicking the GitHub button.',
            buttons = [
            {
                'url':'https://github.com/TPEcool/beeMMX-R',
                'label': 'beeMMX R on GitHub'
            },
            {
                'url':'https://discord.gg/gb7cp6asJF',
                'label':'Discord server'
            }
        ]
    )
    except DiscordNotFound:
        print('[RPC] Discord not found: unable to refresh rich presence!')
'''