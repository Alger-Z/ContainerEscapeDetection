import os,sys,re
from utils import *

def process_one_flle(filename):
    seq=[]
    failed={}
    with open(filename) as f:
        for line in iter(f.readline,'\n'):
            if not line :
                break
            x = line.strip('\n').split()
            if '>' not in x or '<' in x:
                continue
            pos = x.index('>')
            # a line abnormal may be the end line of log "+++ exited "
            if pos == -1  or x[pos+1]=='container':
                continue
            sc_name=x[pos+1]
            if sc_name not in sc_map :
                if  sc_name not in failed:
                    failed[sc_name]=1
                else:
                    failed[sc_name]=failed[sc_name]+1
                continue
            seq.append(sc_map[sc_name])
        #c = len(seq)
    # log2seq result save into txt
    txt_file=txt_path+os.path.splitext(os.path.basename(filename))[0]+'.txt'
    if len(seq)
    with open (txt_file, 'w') as t:
        for n in seq:
            t.write(str(n)+' ')
        

def process(fpath):
    if len(sc_map) ==0:
        print ("sc_map null")
        return
    x=[]
    if os.path.isdir(fpath):
        flist = os.listdir(fpath)
        for i in range(0,len(flist)):
            path = os.path.join(fpath, flist[i])
            if os.path.isfile(path):
                sc_list=process_one_flle(path)
                x.append(sc_list)
    else :
        sc_list=process_one_flle(fpath)
        x.append(sc_list)
    
    
        


if __name__ == "__main__":
    logpath = "data/dvwa/dvwa-test/log/"
    sc_map_json="sc_map.json"
    txt_path='data/dvwatxt/'
    sc_map={}
    if not sc_map :
        sc_map=load_sc_map(sc_map_json)
    
    process(logpath)