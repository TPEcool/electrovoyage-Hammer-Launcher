from ttkbootstrap import *
from srctools import keyvalues, Keyvalues
import os
from richpresence import main as presence, stop as stoppresence
import threading
from PIL import Image, ImageTk, ImageChops
from tkinter.messagebox import showinfo, showwarning, showerror
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.font import Font
from ttkbootstrap.scrolled import ScrolledFrame
import sys
import json
import medialist_transform
import webbrowser
import subprocess
from shlex import split as splitcommand
import electrovoyage_asset_unpacker

PYINSTALLER = False

try:
    '''import pyi_splash as spl # type: ignore
    spl.update_text('electrovoyage\'s Hammer Launcher')
    spl.close()
    
    del spl'''
    PYINSTALLER = True
except ImportError:
    pass

VERSION = '0.1'

# required to use files written into the executable
def getcwd() -> str:
    return os.path.dirname(__file__)

assetpack = electrovoyage_asset_unpacker.AssetPack(os.path.join(getcwd(), 'resources', 'assets.packed'))

with assetpack.exportToTempfile('resources/logo.png') as f:
    win = Window('electrovoyage\'s Hammer Launcher', 'darkly', f.name, (450, 600), minsize=(450, 300), hdpi=False)
win.withdraw()
presencethread = threading.Thread(target=presence)
presencethread.start()

def RightclickMenu(widget: tk.Widget, menu: Menu):
    widget.bind('<Button-3>', lambda x: menu.tk_popup(x.x_root, x.y_root))

def onWindowClosed():
    stoppresence()
    win.destroy()
    
trebuchet_bold = Font(family='Trebuchet MS', size=16, weight='bold')
    
pil_logo = Image.open(assetpack.getfile('resources/logo.png'))

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

appframe = Frame(win)
appframe.pack(expand=True, fill=BOTH)

applist = ScrolledFrame(appframe, padding=10, width=400)
applist.pack(expand=True, fill=BOTH)

statusstr = Label(win, text=f'Version {VERSION}', style=INVERSE + DARK)
statusstr.pack(side=BOTTOM, anchor=S, fill=X)

# Workaround for shortcuts / "open with" and working directory
if PYINSTALLER:
    APP_DIRECTORY = os.path.dirname(sys.executable)
else:
    APP_DIRECTORY = getcwd()
    
global launcherpath, sdkdata
sdkdata = launcherpath = None

def invertAlpha(_im: Image.Image) -> Image.Image:
    im = _im.copy()
    alpha = im.getchannel('A')
    alpha = ImageChops.invert(alpha)
    im.putalpha(alpha)
    return im

ProgramType = str | None

class App:
    def __init__(self, name: str, icon: Image.Image, Program: ProgramType = None, ShellExecute: ProgramType = None):
        if not (Program or ShellExecute):
            raise ValueError(f'invalid application {name}: no ShellExecute or Program defined')
        
        if Program:
            self.program = Program
            self.shellexecute = False
        else:
            self.program = ShellExecute
            self.shellexecute = True
        
        self.name = name
        self.smallicon = icon.resize((32, 32), Image.NEAREST)
        self.smallicontk = ImageTk.PhotoImage(self.smallicon)
    def runcommand(self):
        if self.shellexecute:
            webbrowser.open(self.program)
        else:
            original_directory = os.getcwd()
            os.chdir(sdkdata['binpath'])
            subprocess.Popen(splitcommand(self.program), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            #os.system(self.program)
            os.chdir(original_directory)
        
class ApplicationList:
    def __init__(self, base: ScrolledFrame):
        self.base = base
        self.apps: list[App] = []
        self.app_frames: list[Frame] = []
        self.groups: dict[str, Frame] = {}
        
    def addApp(self, name: str, icon: Image.Image, groupname: str, program: ProgramType = None, shellexecute: ProgramType = None):
        newapp = App(name, icon, program, shellexecute)
        self.apps.append(newapp)
        self._makeGroupIfNecessary(groupname)
        self._makeframe(newapp, groupname)
        
    def _makeGroupIfNecessary(self, groupname: str):
        if groupname in self.groups.keys(): return
        self.groups[groupname] = Labelframe(self.base, text=groupname)
        self.groups[groupname].pack(side=TOP, fill=X, padx=5, pady=5)
        
    def _makeframe(self, app: App, groupname: str):
        frame = Frame(self.groups[groupname], padding=5)
        namelabel = Label(frame, text=app.name, justify=LEFT, font=('Inter', 12))
        namelabel.grid(row=0, column=0)
        imagelabel = Label(frame, image=app.smallicontk)
        imagelabel.grid(column=1, row=0, sticky=E, padx=5)
        
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)

        for widget in (frame, namelabel, imagelabel):
            widget.bind('<Button-1>', lambda _: selectApp(app, frame))
            widget.bind('<ButtonRelease-1>', lambda _: releaseAppButton(frame))
        frame.pack(side=TOP, expand=True, fill=X)
    def run_app(self, app: App):
        #print(app.shellexecute, app.program)
        app.runcommand()
        
def selectApp(app: App, frame: Frame):
    frame.configure(relief=SUNKEN)
    win.update()
    app_list_manager.run_app(app)
    
def releaseAppButton(frame: Frame):
    frame.configure(relief=FLAT)
        
app_list_manager = ApplicationList(applist)

if 'sdk.json' in os.listdir(APP_DIRECTORY):
    with open(os.path.join(APP_DIRECTORY, 'sdk.json')) as jsfile:
        sdkdata = json.load(jsfile)
    
    #app_list_manager.addApp()
    
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
        
    sdkdata = {'binpath': dir, 'sdkpath': launcherpath, 'medialist': medialist_transform.transformMediaList(kv.as_dict())}
    medialist_transform.transformMediaList(kv.as_dict())

    with open(os.path.join(APP_DIRECTORY, 'sdk.json'), 'w') as jsfile:
        json.dump(sdkdata, jsfile, indent=4)
        
binpath = sdkdata['binpath']
sdkpath = sdkdata['sdkpath']

medialist: dict[str, dict[str, dict[str, str]]] = sdkdata['medialist']
for group, programs in medialist.items():
    for _, program in programs.items():
        img = invertAlpha(Image.open(os.path.join(sdkdata['sdkpath'], 'vgui', program['Image'] + '.tga')))
        program.setdefault('Program', None)
        program.setdefault('ShellExecute', None)
        app_list_manager.addApp(program['Title'], img, group, program['Program'], program['ShellExecute'])

class _Command:
    def __init__(self, command: str, shellexecute: bool):
        self.command = command
        self.run = webbrowser.open if shellexecute else os.startfile
        
'''class _Application:
    def __init__(self, title: str, image: str, shellexecute: str | None = None, program: str | None = None):
        shell = False
        _command = program
        if program == None and shellexecute == None:
            raise ValueError(f'invalid application {title}')
        if shellexecute:
            shell = True
            _command = shellexecute
        
        self.command = _Command(_command, shell)'''
    
win.wm_protocol('WM_DELETE_WINDOW', onWindowClosed)

win.deiconify()
win.mainloop()