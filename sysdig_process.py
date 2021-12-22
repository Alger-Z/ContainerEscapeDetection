import os,sys,re
from utils import *
import glbal


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
    if save_into_txt  :
        seq_size=glbal.get_seq_limit()
        if len(seq) < seq_size:
            txt_file=txt_path+os.path.splitext(os.path.basename(filename))[0]+'.txt'
            with open (txt_file, 'w') as t:
                for n in seq:
                    t.write(str(n)+' ')
        else :
            for i in range (seq_size,len(seq),seq_size):
                tmp = seq[i-seq_size:i]
                txt_file=txt_path+os.path.splitext(os.path.basename(filename))[0]+str(i/seq_size)+'.txt'
                with open (txt_file, 'w') as t:
                    for n in tmp:
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
    glbal._init()
    logpath=glbal.get_data_dir("logpath")
    sc_map_json=glbal.get_data_dir("sc_map_json")
    txt_path=glbal.get_data_dir("txt_path")
    sc_map={}
    save_into_txt= False
    if not sc_map :
        try:
            sc_map=load_sc_map(sc_map_json)
        except Exception as e:
            print(e)
            exit 
    try :
        process(logpath)
    except Exception as e:
        print(e) 