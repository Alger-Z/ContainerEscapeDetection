#!/usr/bin python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from typing import KeysView

def gen_sc_map():
    #get sc map from new syscall table
    with open(sc_tb_file) as tbf:
        for line in iter(tbf.readline,'\n'):
            line=line.split()
            sc_map[line[2]]=line[0]
    
    # get sc map from ADFA syscall table
    # with open(sc_adfa) as tbf:
    #     for line in iter(tbf.readline,''):
    #         if not line:
    #             break
    #         if line=='\n':
    #             continue
    #         if(line.startswith("#define")): 
    #             #print (line)
    #             line=line.split()
    #             # lines.append(line)
    #             if len(line) ==3 and str(line[2]).isdigit() :
    #                 sc_name= line[1][5:]
    #                 sc_num=line[2]
    #                 sc_map[sc_name]=sc_num
            # if line[0] == "#define":
            #     sc_name=line[1][5:]
            #     sc_map[sc_name]=line[2]
                
    with open(sc_map_json,'w') as tmp:
        json.dump(sc_map,tmp)
    return sc_map
def load_sc_map():
        sc_map={}
        try :
            with open (sc_map_json,'r') as jsfile:
                sc_map=json.load(jsfile)
        except IOError as e:
            print("load syscall  error:%s", e)   
            try :
                sc_map=gen_sc_map()
            except Exception as e:
                print("generate syscall pickle error:%s",e)
        return sc_map
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
            t.write(n+' ')
    t.close()
    
def start_process():
    global sc_map
    if not sc_map :
        sc_map=load_sc_map()
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
    sc_tb_file = "syscall_64.tbl"
    #sc_tb_pickle= "sc_map.pickle"
    sc_adfa="adfa-syscall.h"
    sc_map_json="sc_map.json"
    log_path= "data/mysql/read"
    txt_path="data/mysqltxt/read/"
    sc_map={}
    failed={}
    sc_n2o={ 
     "select":"pselect6",
    "pipe":"pipe2",
    "access":"faccessat",
    "newfstatat":"fstatat",
    "lstat":"fstatat",
    "open_by_handle_at":"openat",
    "stat":"fstatat",
    "mkdir":"mkdirat",
    "readlink":"readlinkat",
    "getdents":"getdents64",
    "dup2":"dup",
    "chown":"fchown",
    "getpgrp":"getpgid",
    "arch_prctl":"prctl"
    }
    sc_n={
    }
    start_process()