
def getTmpPath(path, name):
    result = path
    if path.endswith('/'):
        print(1)
        result = path + '__' + name + '_tmp__/'
    else:
        print(2)
        result = path + '/__' + name + '_tmp__/'
    return result


def numlen(num):
    return len(str(num))

def numformat(num, width):
    return '{:0{}}'.format(num, width)
