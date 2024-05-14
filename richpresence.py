from os import path
import pygetwindow as gw
from pypresence import Presence, DiscordNotFound
import time

global shouldend
shouldend = False

def main():
    global shouldend
    old_hammername = ''
    hammer_name = ''
    starttime = time.time()

    def sliceSplit(s: str, delimiter: str, start: int, end: int) -> str:
        '''
    Slice a split string from `start` to `end - 1`.
        '''
        return delimiter.join(s.split(delimiter)[start:end])

    def getViewportIndependentWindowName(name: str) -> str:
        return sliceSplit(name, '-', 0, -1)

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
    starttimes = {}

    def GetHammerFilename(win_name: str) -> str:
        return path.basename(win_name.split('-')[1].strip().split('-')[0].strip()[1:])

    while True:
        if shouldend:
            break
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

                if (getViewportIndependentWindowName(old_hammername) != getViewportIndependentWindowName(name)) and (getViewportIndependentWindowName(name) not in starttimes.keys()):
                    starttimes[getViewportIndependentWindowName(name)] = time.time()

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
            path_to_file = GetHammerFilename(hammer_name)

            try:
                rpc.update(
                    details='Editing a map',
                    state=f'Editing {path_to_file}',
                    start = starttimes[getViewportIndependentWindowName(hammer_name)],
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
              
def stop():
    global shouldend
    shouldend = True
            
if __name__ == '__main__':
    main()