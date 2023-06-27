
def getTmpPath(path, name):
    return path + '/___' + name + '_tmp/'


def numlen(num):
    return len(str(num))

def numformat(num, width):
    return '{:0{}}'.format(num, width)
