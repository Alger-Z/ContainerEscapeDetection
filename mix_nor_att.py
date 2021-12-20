
import random,os
from inputdata import readfilesfromAdir


def load_one_flle(filename):
    x = []
    with open(filename) as f:
        line = f.readline()
        x = line.strip('\n').split()
    return x


def data_mix(att,nor,target):
    rint = random.randint(1,10)
    
    if os.path.isfile(att) and os.path.isfile(nor):
        att_d=load_one_flle(att)
        nor_d=load_one_flle(nor)
        stub_n=5
        insert_length=300
        rstart=rint*insert_length
        att_length=len(att_d)/stub_n
        tg_d=[]
        count=0
        while(count<stub_n):
            tg_d.extend(nor_d[rstart+count*insert_length:rstart+(count+1)*insert_length])
            tg_d.extend(att_d[count*att_length:(count+1)*att_length])
            count=count+1
        tg_d.extend(att_d[count*att_length:])
        
        with open (target, 'w') as t:
            for n in tg_d:
                t.write(n+' ')
    else :
        print ("%s or %s is not file",att,nor)
        
def mix_task():
    att_path="data/new/"
    nor="data/dvwatxt/dvwa2.txt"
    tarpath="data/att_withreq/"
    flist=readfilesfromAdir(att_path)
    for att in flist:
        tar=tarpath+os.path.basename(att)
        data_mix(att,nor,tar)
if __name__ =='__main__':
   
    mix_task()