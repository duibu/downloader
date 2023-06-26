import os

def newdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
        

def writeTextFile(filename, filepath, content):
    newdir(filepath)
    with open(filepath + '/' + filename, 'w') as f:
        f.write(content)
