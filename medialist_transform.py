import os
import webbrowser

def transformMediaList(medialist: dict) -> dict:
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