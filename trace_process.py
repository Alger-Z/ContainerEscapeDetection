#!/usr/bin python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from typing import KeysView
from utils import *
import glbal

def log_to_seq(filepath):
    seq=[]
    with open (filepath,'r') as f:
        c=0
        for line in iter(f.readline,'\n'):
            if not line :
                break
            info = line.split()[1]
            pos = info.find('(')
            # a line abnormal may be the end line of log "+++ exited "
            if pos == -1  :
                continue
            sc_name=info[:pos]
            c=c+1
            if sc_name not in sc_map :
                if  sc_name not in failed:
                    failed[sc_name]=1
                else:
                    failed[sc_name]=failed[sc_name]+1
                continue
            seq.append(sc_map[sc_name])      
    # log2seq result save into txt
    txt_file=txt_path+os.path.splitext(os.path.basename(filepath))[0]+'.txt'
    with open (txt_file, 'w') as t:
        for n in seq:
            t.write(str(n)+' ')
    
    
def start_process():
    global sc_map
    if not sc_map :
        sc_map=load_sc_map(sc_map_json)
    if len(sc_map) ==0:
        print ("sc_map null")
        return
    files = os.listdir(log_path)
    for i in files:
        log_to_seq(os.path.join(log_path,i))
    if len(failed):
        with open ('diff.json','w') as df:
            json.dump(failed,df)
        print("convert failed for sycall :",failed)
        # deal with failed ones
        keylist=[i for i in sc_map.keys()]
        keylist = sorted(keylist)
        for sc_fl in failed.keys():
            if sc_fl in sc_n2o: 
                sc_map[sc_fl]=sc_map[sc_n2o[sc_fl]]
            elif sc_fl in sc_n:
                sc_map[sc_fl]=sc_n[sc_fl]
            else:
                print (sc_fl," map to known syscall failed ")
        with open(sc_map_json,'w') as tmp:
            json.dump(sc_map,tmp)
            #automatic find nearest key
            # for key in keylist:
            #     if sc_fl in key:
            #         sc_map[sc_fl]=sc_map[key]
            #         print (sc_fl,"\r",key,"\n")
                #         continue   
    

if __name__ == "__main__":

    sc_map_json=glbal.get_data_dir("sc_map_json")
    log_path=glbal.get_data_dir("mysql_log_path")
    txt_path=glbal.get_data_dir("mysql_txt_path")
    sc_map={}
    failed={}
    start_process()