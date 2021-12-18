import re
import os
from utils import *
def load_one_flle(filename):
    x = []
    with open(filename) as f:
        line = f.readline()
        x = line.strip('\n').split()
    return x

def load_adfa_training_files(rootdir):
    x = []
    y = []
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            x.append(load_one_flle(path))
            y.append(0)
    return x, y

def load_escp_files(rootdir):
    x = []
    y = []
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            x.append(load_one_flle(path))
            y.append(0)
    return x, y

def dirlist(path, allfile):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            allfile.append(filepath)
    return allfile

def load_adfa_webshell_files(rootdir):
    x = []
    y = []
    allfile=dirlist(rootdir,[])
    for file in allfile:
        if re.match(r"\./ADFA-LD/Attack_Data_Master/Web_Shell_\d+/UAD-W*", file):
            x.append(load_one_flle(file))
            y.append(1)
    return x, y
def load_adfa_Adduser_files(rootdir):
    x = []
    y = []
    allfile=dirlist(rootdir,[])
    for file in allfile:
        if re.match(r"\./ADFA-LD/Attack_Data_Master/Adduser_\d+/UAD-W*", file):
            x.append(load_one_flle(file))
            y.append(1)
    return x, y
def load_adfa_Attack_files(rootdir):
    x = []
    y = []
    allfile=dirlist(rootdir,[])
    for file in allfile:
         if re.match(r".*txt$", file):
            x.append(load_one_flle(file))
            y.append(1)
    return x, y
if __name__ =='__main__':
    load_adfa_Attack_files("./ADFA-LD/Attack_Data_Master/")