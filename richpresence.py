from os import path
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

FOUND, IDLE, MISSING, SEARCHING = range(4)

import re

'''def detect_changes(old_str, new_str):
    pattern = r'Hammer - \[(Textured|Top|Front|Right|Wireframe|Polygon|Textured Shaded|Lightmap grid|Smoothing Group)\]'
    keyword_match = re.search(pattern, old_str)
    if keyword_match:
        keyword = keyword_match.group()
        old_content = re.search(r'\[.*?\]', old_str).group()
        new_content = re.search(r'\[.*?\]', new_str).group()
        if old_content == new_content:
            return "No changes detected"
        else:
            return new_content[1:-1]  # Return the content within the square brackets'''

# Example usage
'''old_string = "Hammer - [Textured] Some other changes"
new_string = "Hammer - [Textured] Some different changes"
changes = detect_changes(old_string, new_string)
print(changes)'''


while True:
    hammer_state = None
    # Get a list of all windows
    windows_list = gw.getAllWindows()

    # Extract names of all windows
    window_names: list[str] = [window.title for window in windows_list]

    # Print the list of window names
    #print('Searching for Hammer...')
    hammer_state = SEARCHING
    for name in window_names:
        

        #print('Hammer - ' in name) 
        if name.startswith('Hammer - ['):
            hammer_state = FOUND

            if old_hammername != hammer_name:
                starttime = time.time()

            old_hammername = hammer_name
            hammer_name = name
            #print('Hammer: map is open')
        elif name == 'Hammer':
            hammer_state = IDLE
            #print('Hammer found')
    if hammer_state == SEARCHING:
        hammer_state = MISSING

    # Extract the 'path to file' part
    if hammer_state == FOUND:
        path_to_file = path.basename(hammer_name.split('-')[1].strip().split('-')[0].strip()[1:])
        
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
            print('nameerror')
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