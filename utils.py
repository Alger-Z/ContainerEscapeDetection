import json,os
from logging import debug

from tensorflow.python.ops.gen_array_ops import debug_identity

import pickle
import sys
import glbal

def saveintopickle(obj, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(obj, handle)

    print ("[Pickle]: save object into {}".format(filename))
    return



def loadfrompickle(filename):
    with open(filename, 'rb') as handle:
        b = pickle.load(handle)
    return b

#draw the  process bar
def drawProgressBar(percent, barLen = 20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()

def get_sc_map_reverse():
    sc_map = load_sc_map()
    if not sc_map :
        print("sc_map load failed")
        return
    reverse_map={}
    for sc,idex in sc_map.items():
        reverse_map[str(idex)]=sc
    return reverse_map


def foundone (target,name):
    if 1 in target :
        print ('found 1 in' ,name,' and index',target.index(1))
        
        
def gen_sc_map_old(sc_adfa,sc_map_json):
    #get sc map from ADFA syscall table
    sc_map={}
    with open(sc_adfa) as tbf:
        for line in iter(tbf.readline,''):
            if not line:
                break
            if line=='\n':
                continue
            if(line.startswith("#define")): 
                #print (line)
                line=line.split()
                # lines.append(line)
                if len(line) ==3 and str(line[2]).isdigit() :
                    sc_name= line[1][5:]
                    sc_num=line[2]
                    sc_map[sc_name]=sc_num
            if line[0] == "#define":
                sc_name=line[1][5:]
                sc_map[sc_name]=line[2]
    with open(sc_map_json,'w') as tmp:
        json.dump(sc_map,tmp)
    return sc_map

def gen_sc_map(sc_map_json='sc_map.json',sc_tb_file='syscall_64.tbl'):
    sc_map={}
    #get sc map from new syscall table
    with open(sc_tb_file) as tbf:
        for line in iter(tbf.readline,'\n'):
            line=line.split()
            sc_map[line[2]]=int(line[0])+1
    with open(sc_map_json,'w') as tmp:
        json.dump(sc_map,tmp)
    return sc_map

def load_sc_map(sc_map_json="sc_map.json"):
    sc_map={}
    #sc_tb_pickle= "sc_map.pickle"
    #sc_adfa="adfa-syscall.h"

    if os.path.isfile(sc_map_json):
        with open (sc_map_json,'r') as jsfile:
            sc_map=json.load(jsfile)
    else:
        print("failed load syscall from json , generating ..." )   
        try :
            sc_map=gen_sc_map(sc_map_json)
        except Exception as e:
            print("generate syscall pickle error:{}".format(e))
    return sc_map
if __name__ == '__main__':
    gen_sc_map() 