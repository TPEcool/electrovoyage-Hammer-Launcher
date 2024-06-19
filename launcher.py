from ttkbootstrap import *
from srctools import keyvalues, Keyvalues
import os
from richpresence import main as presence, stop as stoppresence
import threading
from PIL import Image, ImageTk, ImageFilter
from tkinter.messagebox import showinfo, showwarning, showerror
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.font import Font
from ttkbootstrap.scrolled import ScrolledFrame
import sys
import json

PYINSTALLER = False

try:
    import pyi_splash as spl # type: ignore
    spl.update_text('Hold on a second, VMText is loading...')
    spl.close()
    
    del spl
    PYINSTALLER = True
except ImportError:
    pass

VERSION = '0.1'

# required to use files written into the executable
def getcwd() -> str:
    return os.path.dirname(__file__)

win = Window('electrovoyage\'s Hammer Launcher', 'darkly', os.path.join(getcwd(), 'resources/logo.png'), (500, 400), minsize=(400, 300), hdpi=False)
presencethread = threading.Thread(target=presence)
presencethread.start()

def onWindowClosed():
    stoppresence()
    win.destroy()
    
trebuchet_bold = Font(family='Trebuchet MS', size=16, weight='bold')
    
pil_logo = Image.open(os.path.join(getcwd(), 'resources', 'logo.png'))

global logo, large_logo
logo = ImageTk.PhotoImage(pil_logo.resize((48, 48), Image.BILINEAR))
large_logo = ImageTk.PhotoImage(pil_logo.resize((100, 100), Image.BILINEAR))

welcome_frame = Frame(win, style=DARK)
welcome_frame.pack(side=TOP, fill=BOTH, anchor=N)

Label(welcome_frame, text='Welcome to', justify=LEFT, font = ('Trebuchet MS', 11), background='#303030').grid(row=0, column=0, sticky=NW)
Label(welcome_frame, text='electrovoyage.\'s Hammer Launcher', justify=LEFT, font=trebuchet_bold, background='#303030').grid(row=1, column=0, sticky=SW)
Label(welcome_frame, image=logo, background='#303030').grid(row=0, column=1, rowspan=2, sticky=S)

welcome_frame.columnconfigure(0, weight=1)
welcome_frame.columnconfigure(1, weight=0)

#applist.pack(expand=True, fill=BOTH)

app_pane = PanedWindow(win, orient=HORIZONTAL)
app_pane.pack(expand=True, fill=BOTH, anchor=N)

applist = ScrolledFrame(win)

app_prev_frame = Frame(win, padding=10)

# Workaround for shortcuts / "open with" and working directory
if PYINSTALLER:
    APP_DIRECTORY = os.path.dirname(sys.executable)
else:
    APP_DIRECTORY = getcwd()
    
global launcherpath, sdkdata
sdkdata = launcherpath = None

if 'sdk.json' in os.listdir(APP_DIRECTORY):
    with open(os.path.join(APP_DIRECTORY, 'sdk.json')) as jsfile:
        sdkdata = json.load(jsfile)
else:
    showinfo('Media list not found', 'Could not find the media list file (sdk.json). Please locate your game\'s bin folder in the next dialog.')
    while True:
        dir = askdirectory(mustexist=True, title='Locate your bin folder')
        if not dir:
            sys.exit()
        elif 'SDKLauncher' not in os.listdir(dir):
            showerror('Invalid bin folder', 'Could not find SDKLauncher in specified folder. Please specify the correct bin folder.')
        else: break
    launcherpath = os.path.join(dir, 'SDKLauncher')
    with open(os.path.join(launcherpath, 'MediaList.txt')) as fp:
        kv = Keyvalues.parse(fp.read())
        
    sdkdata = {'basepath': launcherpath, 'medialist': kv.as_dict()}

    with open(os.path.join(APP_DIRECTORY, 'sdk.json'), 'w') as jsfile:
        json.dump(sdkdata, jsfile, indent=4)

class App:
    def __init__(self, name: str, icon: Image.Image):
        self.name = name
        self.icon = icon.resize((100, 100), Image.BICUBIC)
        self.smallicon = icon.resize((32, 32), Image.BICUBIC)
        self.icontk = ImageTk.PhotoImage(self.icon)
        self.smallicontk = ImageTk.PhotoImage(self.smallicon)
        
class ApplicationList:
    def __init__(self, base: ScrolledFrame):
        self.base = base
        self.apps: list[App] = []
        self.app_frames: list[Frame] = []
        
    def addApp(self, name: str, icon: Image.Image):
        newapp = App(name, icon)
        self.apps.append(newapp)
        self._makeframe(newapp)
        
    def _makeframe(self, app: App):
        frame = Frame(self.base, padding=5)
        Label(frame, text=app.name, justify=LEFT, font=('Inter', 12)).grid(row=0, column=0)
        Label(frame, image=app.smallicontk).grid(column=1, row=0, sticky=E, padx=5)
        
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        
        frame.bind('<Button-1>', lambda _: selectApp(app, frame))
        frame.bind('<ButtonRelease-1>', lambda _: releaseAppButton(frame))
        frame.pack(side=TOP, expand=True, fill=X)
        
def selectApp(app: App, frame: Frame):
    frame.configure(relief=SUNKEN)
    app_prev_image.configure(text=app.name, image=app.icontk)
    
def releaseAppButton(frame: Frame):
    frame.configure(relief=FLAT)
        
app_list_manager = ApplicationList(applist)
    
for i in range(50):
    app_list_manager.addApp(f'app {i}', Image.open(os.path.join(getcwd(), 'resources', 'noicon.png')))


app_prev_image = Label(app_prev_frame, image = large_logo, text=f'Launcher v{VERSION}', compound=TOP, justify=CENTER, font = ('Inter', 16))
app_prev_image.pack(side=TOP, expand=True, anchor=N, pady=10)

app_pane.add(applist.container, weight=0)
app_pane.add(app_prev_frame, weight=1)
    
win.wm_protocol('WM_DELETE_WINDOW', onWindowClosed)

win.mainloop()