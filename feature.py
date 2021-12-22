import os,sys,re
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import append
from sklearn.feature_extraction.text import TfidfVectorizer
from load_helper import load_one_flle
from inputdata import readfilesfromAdir
from utils import load_sc_map

#sc_dic is tuple
def dist_pic(sc_dic,name,sc_map=None):
    sc=[]
    counts=[]
    if len(sc_dic)>15:
        sc_num = 15
    else:
        sc_num=len(sc_dic)
        if sc_num < 10:
            return
    for x in sc_dic :
        sc.append(x[0])
        counts.append(x[1])
    plt.figure(dpi=150)
    
    bar_width= 0.2
    sc=sc[:sc_num]
    if sc_map:
        sc=[sc_map[x] for x in sc] 
    counts=counts[:sc_num]
    
    index= np.arange(sc_num)
    p2=plt.bar(index,counts,width=bar_width,label="count",color='b')
    plt.xlabel('syscall')
    plt.ylabel('count')
    plt.title(name)
    plt.xticks(index,sc,rotation=60)
    plt.tight_layout() 
    plt.legend()
    
    plt.savefig('pic/'+name+'.png')
    


def sysdig_line(sc,line):
    x = line.strip('\n').split()
    if '>' not in x or '<' in x :
        return
    pos = x.index('>')
    if pos == -1  or x[pos+1]=='container':
        return
    
    sc_n= x[pos+1]
    if sc_n in sc:
        sc[sc_n]=sc[sc_n]+1
    else :
        sc[sc_n]=1

def strace_line(sc,line):
    info = line.split()[1]
    pos = info.find('(')
    # a line abnormal may be the end line of log "+++ exited "
    if pos == -1  :
        return
    sc_n=info[:pos]
    if sc_n in sc:
        sc[sc_n]=sc[sc_n]+1
    else :
        sc[sc_n]=1
        
def statis(file,type):
    sc={}
    with open (file,'r') as f:
        for line in iter(f.readline,'\n'):
            if not line :
                break
            if type == 'sysdig':
                sysdig_line(sc,line)
            else:
                strace_line(sc,line)
    
    sc=sorted(sc.items(),key = lambda a:a[1],reverse = True)
    if (len(sc)<5):
        print("%s ignored for less than 5 types:%d",file,len(sc))
        print()
    #print(sc)
    
    #dist_pic(sc,os.path.basename(file).split('.')[0])
    
def log_():
    if len(sys.argv) > 1 :
        logpath=sys.argv[1]
    else :
        #logpath = "data/mysql/mix/mixed_0001"
        logpath = "data/syscall_log/shim.log"
    if logpath.endswith('txt'):
        statis(logpath,'sysdig')
    else :
        statis(logpath,'strace')
        
def sysindex_():

    #path = "data/att_withreq"
    #path = "data/mysqltxt/mix_big"
    path = "data/dvwatxt/"
    flist = readfilesfromAdir(path)
    # flist=[]
    # flist.append("data/runc_cpt.txt.new")
    
    # generate map for syscall number to syscall name
    sc_map = load_sc_map()
    if not sc_map :
        print("sc_map load failed")
        return
    reverse_map={}
    for sc,idex in sc_map.items():
        reverse_map[str(idex)]=sc
        
    datal=[]
    
    for f in flist:
        sc_count ={}
        sc_index_list=load_one_flle(f)
        print("%s count %d",f,len(sc_index_list))
        limit = 10000
        for n in sc_index_list:
            limit-=1
            if limit <= 0 :
                break
            if n not in sc_count:
                sc_count[n] = 1
            else:
                sc_count[n] += 1
        sc_count=sorted(sc_count.items(),key = lambda a:a[1],reverse = True)
        if (len(sc_count)<5):
            print("%s ignored for less than 5 types:%d",f,len(sc_count))
            # mixfile=os.path.basename(f).split('.')[0] 
            # mixfilepath='data/mysql/mix/'+mixfile
            # try:
            #     os.remove(mixfilepath)
            # except:
            #     pass
        else :
            datal.append([f,sc_count]) 
         
    #print(sc)
    for data in datal:
        dist_pic(data[1],os.path.basename(data[0]).split('.')[0],reverse_map)
        
if __name__ == "__main__":
    #log_()
    sysindex_()