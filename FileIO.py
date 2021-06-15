import json

def readFile(file):
    _file = open(file, 'r+')
    data = dict()
    try:
        data = dict(json.load(_file))
    except:
        data = dict()
    _file.close()
    return data


def writeFile(data, file):
    _file = open(file, 'w')
    json.dump(data, _file, indent=4)
    _file.close()
