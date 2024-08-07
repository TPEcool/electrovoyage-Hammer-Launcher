import os
import webbrowser

def transformMediaList(medialist: dict) -> dict:
    '''
    Convert MediaList.txt contents to sdk.json contents.
    '''
    media = medialist['media']
    images: dict[str, dict] = media['images']
    image_directory = {}
    for _, i in images.items():
        image_directory.update({i['index']: i['image']})
        
    newdict = {}
        
    #print(image_directory)
        
    sections: dict[str, dict[str, dict]] = media['sections']
    for _group, i in sections.items():
        group = i.pop('name')
        i.pop('id')
        newdict[group] = {}
        for program, j in i.items():
            newdict[group][program] = {}
            
            #print(program, j)
            newdict[group][program]['Image'] = image_directory[j['image']]
            if 'shellexecute' in j.keys():
                newdict[group][program]['ShellExecute'] = j['shellexecute']
            elif 'program' in j.keys():
                newdict[group][program]['Program'] = j['program']
            else:
                raise ValueError(f'invalid program {j['title']}: no Program or ShellExecute value')
            newdict[group][program]['Title'] = j['title']
            
    return newdict

LATEST_SDK_VERSION = "2"
VALVE_ORIGINAL_ICONS = ['icon_create', 'icon_document', 'icon_faceposer', 'icon_file', 'icon_files', 'icon_folder', 'icon_folder_16', 'icon_hammer', 'icon_hl2_media', 'icon_hlmv', 'icon_refresh', 'icon_reset', 'icon_scenemanager', 'icon_soft', 'icon_weblink']

def upgradeMediaList(medialist: dict) -> dict:
    '''
    Convert a sdk.json file to the latest version.
    '''
    medialist.setdefault('version', '1')
    version = medialist['version']
    #print(medialist)
    if version == LATEST_SDK_VERSION:
        return medialist
    elif float(version) > float(LATEST_SDK_VERSION):
        raise ValueError('sdk.json version is too new. To regenerate file, please delete it and restart program.')
    else:
        match version:
            case "1":
                newmedialist: dict[str, list[dict[str, str]]] = {}
                for categoryname, categoryapps in medialist['medialist'].items():
                    #print(categoryname, categoryapps)
                    newmedialist[categoryname] = []
                    
                    for _, programdata in categoryapps.items():
                        programdata['invert_image'] = programdata['Image'] not in VALVE_ORIGINAL_ICONS
                        newmedialist[categoryname].append(programdata)
                        
                return {
                    'binpath': medialist['binpath'],
                    'sdkpath': medialist['sdkpath'],
                    'version': LATEST_SDK_VERSION,
                    'medialist': newmedialist,
                }