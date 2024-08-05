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
from electrovoyage_asset_unpacker import AssetPack

PYINSTALLER = getattr(sys, 'frozen', False)

if PYINSTALLER:
    try:
        import pyi_splash as spl # type: ignore
        spl.update_text('electrovoyage\'s Hammer Launcher')
        spl.close()

        del spl
    except:
        pass

# required to use files written into the executable
def getcwd() -> str:
    return os.path.dirname(__file__)

# Workaround for shortcuts / "open with" and working directory
if PYINSTALLER:
    APP_DIRECTORY = os.path.dirname(sys.executable)
else:
    APP_DIRECTORY = getcwd()

VERSION = '0.9'
assetpack = AssetPack(os.path.join(getcwd(), 'resources', 'assets.packed'))

win = Window('electrovoyage\'s Hammer Launcher', 'darkly', os.path.join(getcwd(), 'resources', 'logo.png'), (450, 600), minsize=(450, 300), hdpi=False)
win.withdraw()
showwarning('Hammer launcher beta', 'This is a beta version of electrovoyage\'s Hammer Launcher. If another program shows up in your Discord profile instead of the Hammer launcher or if you encounter any other sort of issue, please report them to:\n\nelectrovoyagesoftware@gmail.com, or\n\nhttps://github.com/TPEcool/electrovoyage-Hammer-Launcher/issues')
presencethread = threading.Thread(target=presence, daemon=True)
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
    
global launcherpath, sdkdata
sdkdata = launcherpath = None

def invertAlpha(_im: Image.Image) -> Image.Image:
    im = _im.copy()
    alpha = im.getchannel('A')
    alpha = ImageChops.invert(alpha)
    im.putalpha(alpha)
    return im

ProgramType = str | None

'''class _FakeTkBoolVar:
    def __init__(self, setter, getter):
        self.setter = setter
        self.getter = getter
    def get() -> bool:
        return self.getter()
    def set(value: bool):
        self.setter(value)'''

class App:
    @property
    def invert_image(self) -> bool:
        return self._invert_var.get()
    
    def __init__(self, name: str, iconpath: str, icon: Image.Image, invertedicon: Image.Image, Program: ProgramType = None, ShellExecute: ProgramType = None, groupname: str = '', programid: str = '', invert_image: bool = True):
        if not (Program or ShellExecute):
            raise ValueError(f'invalid application {name}: no ShellExecute or Program defined')
        
        if Program:
            self.program = Program
            self.shellexecute = False
        else:
            self.program = ShellExecute
            self.shellexecute = True
        
        self.name = name
        self._invert_var = BooleanVar(value=invert_image)
        self.smallicon = icon.resize((32, 32), Image.NEAREST)
        self.smallicontk = ImageTk.PhotoImage(self.smallicon)
        self.smallinvicon = invertedicon.resize((32, 32), Image.NEAREST)
        self.smallinvicontk = ImageTk.PhotoImage(self.smallinvicon)
        self.groupname = groupname
        self.programid = programid
        self.iconpath = iconpath
        
        self.STARTED_INVERTED = invert_image
        
    def saveimageinversion(self): 
        self.img_label.configure(image=self.smallicontk if self.STARTED_INVERTED == self.invert_image else self.smallinvicontk)
        
        #medialist = [i.serialize() for i in app_list_manager.apps]
        medialist = {}
        
        for key, val in app_list_manager.group_lists.items():
            medialist[key] = [i.serialize() for i in val]
        
        sdkdata['medialist'] = medialist
        savesdk()
        
    def runcommand(self):
        if self.shellexecute:
            webbrowser.open(self.program)
        else:
            original_directory = os.getcwd()
            os.chdir(sdkdata['binpath'])
            subprocess.Popen(splitcommand(self.program), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            #os.system(self.program)
            os.chdir(original_directory)
            
    def setframe(self, frame: Frame):
        self.frame = frame
        
    def set_image_label(self, label: Label):
        self.img_label = label
        
    def __repr__(self) -> str:
        return f'<application name={self.name}>'
    
    def makemenu(self) -> Menu:
        menu = Menu(win)
        menu.add_command(label='Run', command=self.runcommand)
        menu.add_separator()
        #menu.add_command(label='Move to testgroup', command=lambda: app_list_manager.move_app(self, 'Assets'))
        menu.add_command(label='Move up', command=lambda: app_list_manager.swap_above(self))
        menu.add_command(label='Move down', command=lambda: app_list_manager.swap_below(self))
        menu.add_separator()
        menu.add_checkbutton(label='Invert image', onvalue=True, offvalue=False, variable=self._invert_var, command=self.saveimageinversion)
        
        return menu
    
    def serialize(self) -> dict:
        return {
            'Image': self.iconpath,
            'Program': None if self.shellexecute else self.program,
            'Title': self.name,
            'invert_image': self.invert_image,
            'ShellExecute': self.program if self.shellexecute else None
        }
    
def swapvalues(container: list | tuple, a: int, b: int):
    '''
    Swap values at indices a and b.
    '''
    _container = container.copy()
    old_a_value = _container[a]
    old_b_value = _container[b]
    _container[b] = old_a_value
    _container[a] = old_b_value
    
    return _container
        
class ApplicationList:
    def __init__(self, base: ScrolledFrame):
        self.base = base
        self.apps: list[App] = []
        self.app_frames: list[Frame] = []
        self.app_frame_dict: dict[str, Frame] = []
        self.groups: dict[str, Frame] = {}
        self.group_lists: dict[str, list[App]] = {}
        
    def addApp(self, name: str, iconpath: str, icon: Image.Image, invertedicon: Image.Image, groupname: str, program: ProgramType = None, shellexecute: ProgramType = None, programid: str = '', invert_image: bool = True):
        newapp = App(name, iconpath, icon, invertedicon, program, shellexecute, groupname, programid, invert_image)
        self.apps.append(newapp)
        if groupname not in tuple(self.group_lists.keys()):
            self.group_lists[groupname] = []
        self.group_lists[groupname].append(newapp)
        self._makeGroupIfNecessary(groupname)
        self._makeframe(newapp, groupname)
        
    def swap_above(self, app: App):
        #print(self.group_lists, sep='\n\n\n')
        item_group_key, item_group = self._find_group(app)
        
        if item_group.index(app) == 0:
            return
        else:
            item_group = swapvalues(item_group, item_group.index(app), item_group.index(app) - 1)
            #self.group_lists[item_group_key] = item_group
            _item_group = self.group_lists[item_group_key]
            
            oldapps = [
                _item_group[_item_group.index(app)],
                _item_group[_item_group.index(app) - 1],
            ]
            
            frames_to_repack = [i.frame for i in item_group]
            
            #print(oldapps)
            for i in oldapps:
                i.frame.pack_forget()
                
            for i in item_group:
                i.frame.pack_forget()
                
            #print(*frames_to_repack, sep='\n')
            for i in frames_to_repack:
                i.pack(side=TOP, expand=True, fill=X)
                
            self.group_lists[item_group_key] = item_group
            
            self.save_new_layout(item_group_key)
            
    def swap_below(self, app: App):
        #print(self.group_lists, sep='\n\n\n')
        item_group_key, item_group = self._find_group(app)
        
        if item_group.index(app) == len(item_group) - 1:
            return
        else:
            item_group = swapvalues(item_group, item_group.index(app), item_group.index(app) + 1)
            #self.group_lists[item_group_key] = item_group
            _item_group = self.group_lists[item_group_key]
            #print(*([(i, j) for i, j in enumerate(item_group)]), sep = '\n')
            oldapps = [
                _item_group[_item_group.index(app)],
                _item_group[_item_group.index(app) + 1],
            ]
            
            frames_to_repack = [i.frame for i in item_group]
            
            #print(oldapps)
            for i in oldapps:
                i.frame.pack_forget()
                
            for i in item_group:
                i.frame.pack_forget()
                
            #print(*frames_to_repack, sep='\n')
            for i in frames_to_repack:
                i.pack(side=TOP, expand=True, fill=X)
                
            self.group_lists[item_group_key] = item_group
            
            self.save_new_layout(item_group_key)
        
    def _find_group(self, app: App) -> tuple[str, list[App]]:
        for key, lst in self.group_lists.items():
            if app in lst:
                return key, lst
            
    def save_new_layout(self, groupname: str):
        #print(medialist, groupname)
        global medialist, sdkdata
        medialist[groupname] = [i.serialize() for i in self.group_lists[groupname]]
        sdkdata['medialist'] = medialist
        
        print(sdkdata)
        #print(json.dumps(sdkdata, indent=4))
        
        savesdk()        
        
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
            RightclickMenu(widget, app.makemenu())
        frame.pack(side=TOP, expand=True, fill=X)
        app.setframe(frame)
        app.set_image_label(imagelabel)
        self.app_frames.append(frame)
    
    def move_app(self, app: App, newgroup: str):
        app.frame.destroy()
        oldgroup = app.groupname
        newframe = self._makeframe(app, newgroup)
        app.setframe(newframe)
        global sdkdata
        appdata = sdkdata['medialist'][oldgroup].pop(app.programid)
        sdkdata['medialist'][newgroup][app.programid] = appdata
        #print(json.dumps(sdkdata, indent=4))
        
        #self.groups[newgroup]
    
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
sdkdata: dict[str, dict[str, dict[str, dict[str, str]]]]

def savesdk():
    with open(os.path.join(APP_DIRECTORY, 'sdk.json'), 'w') as sdk:
        json.dump(sdkdata, sdk, indent=4)

def opensdk():
    global sdkdata
    with open(os.path.join(APP_DIRECTORY, 'sdk.json')) as jsfile:
        sdkdata = json.load(jsfile)
        
def reloadsdk():
    opensdk()
    
    global binpath, sdkpath, medialist
    binpath = sdkdata['binpath']
    sdkpath = sdkdata['sdkpath']

    medialist = sdkdata['medialist']
    #print(medialist)

if 'sdk.json' in os.listdir(APP_DIRECTORY):
    reloadsdk()
    
    #app_list_manager.addApp()
    
else:
    showinfo('Media list not found', 'Could not find the media list file (sdk.json). Please locate your game\'s bin folder in the next dialog.')
    while True:
        dir = askdirectory(mustexist=True, title='Locate your bin folder')
        if not dir:
            stoppresence()
            sys.exit()
        elif 'SDKLauncher' not in os.listdir(dir):
            showerror('Invalid bin folder', 'Could not find SDKLauncher in specified folder. Please specify the correct bin folder.')
        else: break
    launcherpath = os.path.join(dir, 'SDKLauncher')
    with open(os.path.join(launcherpath, 'MediaList.txt')) as fp:
        kv = Keyvalues.parse(fp.read())
        
    sdkdata = medialist_transform.upgradeMediaList({'binpath': dir, 'sdkpath': launcherpath, 'medialist': medialist_transform.transformMediaList(kv.as_dict())})

    with open(os.path.join(APP_DIRECTORY, 'sdk.json'), 'w') as jsfile:
        json.dump(sdkdata, jsfile, indent=4)
        
    reloadsdk()
        
global medialist
for group, programs in medialist.items():
    sdkdata.setdefault('version', '1')
    
    with open(os.path.join(APP_DIRECTORY, 'sdk.json'), 'w') as sdk:
        json.dump(medialist_transform.upgradeMediaList(sdkdata), sdk, indent=4)
    
    if sdkdata['version'] == '1':
        for programid, program in programs.items():
            program.setdefault('invert_image', True)
            _img = Image.open(os.path.join(sdkdata['sdkpath'], 'vgui', program['Image'] + '.tga'))
            img = invertAlpha(_img) if program['invert_image'] else _img
            inverted_img = _img if program['invert_image'] else invertAlpha(_img)
            program.setdefault('Program', None)
            program.setdefault('ShellExecute', None)
            app_list_manager.addApp(program['Title'], program['Image'], img, inverted_img, group, program['Program'], program['ShellExecute'], programid, program['invert_image'])
            
    else:
        for program in programs:
            _img = Image.open(os.path.join(sdkdata['sdkpath'], 'vgui', program['Image'] + '.tga'))
            img = invertAlpha(_img) if program['invert_image'] else _img
            inverted_img = _img if program['invert_image'] else invertAlpha(_img)
            program.setdefault('Program', None)
            program.setdefault('ShellExecute', None)
            app_list_manager.addApp(program['Title'], program['Image'], img, inverted_img, group, program['Program'], program['ShellExecute'], program['Title'].lower(), program['invert_image'])
    
win.wm_protocol('WM_DELETE_WINDOW', onWindowClosed)

win.deiconify()
win.focus()
win.mainloop()
