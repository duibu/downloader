import os
import shutil
import csv

def newdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
        

def writeTextFile(filename, filepath, content):
    newdir(filepath)
    with open(filepath + '/' + filename, 'w') as f:
        f.write(content)

def del_dir_not_empty(filepath):
    if not is_folder_empty(filepath):
        shutil.rmtree(filepath)


def is_folder_empty(folder_path=''):
    if len(os.listdir(folder_path)) == 0:
        return True
    else:
        return False

def file_exists(filepath=''):
    return os.path.exists(filepath)

def file_is_csv(filepath = ''):
    file_extension = filepath.split('.')[-1]
    return file_extension.lower() == 'csv'

def file_is_txt(filepath = ''):
    file_extension = filepath.split('.')[-1]
    return file_extension.lower() == 'txt'

def read_csv(filename=''):
    result = []
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data = {}
            for key, value in row.items():
                data[key] = value
            result.append(data)
    
    return result

def read_txt(filepath=''):
    result = []
    file = open(filepath, 'r')
    for line in file:
        result.append(line.rstrip())
    file.close()
    return result
