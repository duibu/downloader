import os

def getTmpPath(path, name):
    result = path
    if path.endswith(os.sep):
        result = path + '__' + name + '_tmp__' + os.sep
    else:
        result = path + os.sep + '__' + name + '_tmp__' + os.sep
    return result


def numlen(num):
    return len(str(num))

def numformat(num, width):
    return '{:0{}}'.format(num, width)
