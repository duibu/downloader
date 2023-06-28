
def getTmpPath(path, name):
    result = path
    if path.endswith('/'):
        result = path + '__' + name + '_tmp__/'
    else:
        result = path + '/__' + name + '_tmp__/'
    return result


def numlen(num):
    return len(str(num))

def numformat(num, width):
    return '{:0{}}'.format(num, width)
