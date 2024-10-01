'''
Unpacker for electrovoyage's asset packs.
'''

import gzip
from io import BufferedReader, BytesIO, StringIO
from os import PathLike, path, makedirs
from typing import Literal
from assetpack_exceptions import *
from tqdm import tqdm
from tempfile import TemporaryDirectory, TemporaryFile, NamedTemporaryFile
from shutil import make_archive

class AssetPack:
    '''
    Asset package.
    '''
    def __init__(self, file: BufferedReader | PathLike | str):
        '''
        Read asset bundle.
        '''

        if isinstance(file, (PathLike, str)):
            self.path = str(file)
            with open(file, 'rb') as binf:
                content = binf.read()
        else:
            content = file.read()
            self.path = file.name

        if not content.startswith(b'!PACKED\n'):
            raise MissingHeaderException('file doesn\'t start with "!PACKED"')
        else:
            content = content.replace(b'!PACKED\n', b'')

        dirdict = eval(gzip.decompress(content).decode())
        
        self.tree: dict[str, bytes] = dirdict['tree']
        self.dirinfo: dict[str, bytes] = dirdict['dirinfo']

    def getfile(self, filepath: PathLike | str, bytes_: bool = True) -> BytesIO | StringIO:
        '''
        Get file from asset bundle.
        If `bytes_` is true, returns an `AssetIO` with `bytes` read support. Else, it will support reading `str` instead.
        Extracted file is temporary and will only be deleted when closed.
        '''
        if bytes_:
            return BytesIO(self.tree[filepath])
        else:
            return StringIO(self.tree[filepath])
    
    def getDir(self) -> dict['files': list[str], 'dirs': list[str]]:
        '''
        Return dictionary of packfile's directory.
        '''
        return self.dirinfo
    
    def reload(self):
        '''
        Reload file.
        '''
        self.__init__(self.path)
        
    def extract(self, epath: str):
        '''
        Export all files from bundle and recreate directory structure.
        `epath` is the base directory, so for example the asset path 'resources/images/file.png' would be exported as '<`epath`>/resources/images/file.png'.
        '''
        progressbar = tqdm(list(self.getDir().keys()), 'Extracting bundle', len(list(self.getDir().keys())))
        
        for key, value in self.getDir().items():
            makedirs(path.join(epath, *(key.split('/'))), exist_ok=True)
            files, dirs = value['files'], value['dirs']
            for dir in dirs:
                makedirs(path.join(epath, *(key.split('/')), dir), exist_ok=True)
            for file in files:
                self.exportfile(key + '/' + file, path.join(epath, *(key.split('/')), file))
                
            progressbar.update(list(self.getDir().keys()).index(key) + 1)
            
    def extract_tozip(self, efile: str):
        '''
        Extract this bundle to a ZIP file.
        '''
        with TemporaryDirectory(prefix='assets.packed_zipexport_') as tempdir:
            self.extract(tempdir)
            make_archive(path.splitext(efile)[0], 'zip', tempdir)
    
    def exportfile(self, packpath: str, exp_path: str):
        '''
        Export file from asset bundle.
        '''
        with open(exp_path, 'wb') as expfile:
            expfile.write(self.getfile(packpath).read())
        
    def listobjects(self) -> list[str]:
        return list(self.tree.keys())
    
    def getDirList(self) -> list[str]:
        return list(self.dirinfo.keys())
    
    def exportToTempfile(self, packpath: str) -> NamedTemporaryFile:
        '''
        Extract file to temporary file.
        '''
        f = TemporaryFile(prefix='AssetPackTempFile', suffix='.'+packpath.split('.')[-1])
        f.write(self.getfile(packpath).read())
        return f
    
class AssetPackEmulator:
    '''
    Fake asset pack that actually streams in from a real folder.
    '''
    def __init__(self, basefolder: str):
        '''
        Initialize a new assetpack emulator with `basefolder` as package root.
        '''
        self.basefolder = basefolder
    def getfile(self, filepath: str) -> BufferedReader:
        '''
        Return handle for file at path.
        '''
        return open(path.join(self.basefolder, *filepath.split('/')), 'rb')
    
def AssetPackWrapper(pack: str, frozen: bool, resourcepath: str | None = None) -> AssetPack | AssetPackEmulator:
    '''
    Return a real AssetPack if `frozen`, otherwise return an assetpack emulator from a resource path.
    `pack` is a path to the asset pack and must be specified.
    `resourcepath` is an optional path to the `resources` folder. If not specified, assume the asset pack specified by `pack` is in the `resources` folder.
    '''
    if frozen:
        resourcepath_ = resourcepath if resourcepath is not None else path.dirname(pack)
        return AssetPackEmulator(resourcepath_)
    else:
        return AssetPack(pack)
    
class StreamingAssetPack:
    '''
    Asset pack that is extracted to a temporary folder.
    '''
    def __init__(self, file: BufferedReader | PathLike | str):
        '''
        Load streaming asset pack.
        The temporary folder needs to be closed after every file is loaded from it. This can be done
        using the `with` context manager or by calling the `close` method.
        '''
        self.assetpack = AssetPack(file)
        self.tempdir = TemporaryDirectory(prefix='assets.packed_streaming_pack_')
        
        self.assetpack.extract(self.tempdir.name)
    def __exit__(self):
        self.tempdir.__exit__()