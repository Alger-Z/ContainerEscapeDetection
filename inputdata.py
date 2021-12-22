#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logging import debug
import os
from re import L
import sys
import numpy as np
from numpy.core.defchararray import count
from numpy.core.numeric import array_repr
import matplotlib.pyplot as plt
from io_helper import loadfrompickle, saveintopickle
import utils
import glbal


def readfilesfromAdir(datadir):
    #read a list of files
    files = os.listdir(datadir)
    files_absolute_paths = []
    for file in files:
        files_absolute_paths.append(os.path.join(datadir,str(file)))
    return files_absolute_paths

def dirlist(path, allfile):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            allfile.append(filepath)
    return allfile

#this is used to read a char sequence from
def readCharsFromFile(file):
    channel_values = open(file).read().split()
    #print (len(channel_values))
    #channel_values is a list
    return channel_values
    #print (channel_values[800:819])

def get_attack_subdir(path):
    subdirectories = os.listdir(path)
    for i in range(0,len(subdirectories)):
        subdirectories[i] = path + subdirectories[i]

    #print (subdirectories)
    return (subdirectories)

def gen_scgram_dic(allthelist,n_gram=20):
    ngramdic={}
    for alist in allthelist:
        for i in range(0,len(alist)-n_gram+1,1):
            tmp = str(alist[i:i+n_gram])
            if tmp in ngramdic:
                ngramdic[tmp]+=1
            else:
                ngramdic[tmp]=1
    print("ngram count:",len(ngramdic.keys()))
    ngramdic_sorted=sorted(ngramdic.items(),key = lambda a:a[1],reverse = True)
    saveintopickle(ngramdic_sorted, str(n_gram)+"output/gramdic_sorted.pickle")
    
def statis_ngram_dic(dic_name):
    dic=loadfrompickle(dic_name)
    print ("top 5 frequence ngram")
    for i in range (0,5):
        print(dic[i])
    print ("bottom 5 frequence ngram")
    for i in range (0,5):
        print(dic[len(dic)-i-1])
    total=0
    #count_dic=[ 0 for i in range (dic[0][1]+1)]
    count_dic={}
    for key,times in dic:
        total+=times
        if times in count_dic:
            count_dic[times]+=1
        else:
            count_dic[times]=1
    count_tuplist=sorted(count_dic.items(),key = lambda a:a[1])
    timeslist=[]
    countlist=[]
    for tp in count_tuplist:
        timeslist.append(tp[0])
        countlist.append(tp[1])

    #count_dic=[x/total for x in count_dic]
    
    
    plt.figure()
    plt.title("20 gram distribution")
    plt.plot(timeslist,countlist,'black')
    plt.savefig("pic/20gramd_dist.png")
        
def get_all_call_sequences(dire):
    try:
        files = dirlist(dire,[])
    except Exception as e:
        print ("{} get sequence error",e)
        return []
    allthelist = []
    #print (len(files))
    for eachfile in files: 
        allthelist.append(readCharsFromFile(eachfile))  
    #generate sc ngram dictionary,sorted by apperance times
    if runalone:
        gen_scgram_dic(allthelist,15)
    
    print("The length of all the list ")
    print (len(allthelist))
    
    #clean the all list data set
    _max = 0
    for i in range(0,len(allthelist)):
        _max = max(_max,len(allthelist[i]))
        allthelist[i] = map(int,allthelist[i])
    print ("The maximum length of a sequence is that {}".format(_max))

    return (allthelist)

## shift the data for analysis
def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]


def convertToOneHot(vector, num_classes=None):
    """
    Converts an input 1-D vector of integers into an output
    2-D array of one-hot vectors, where an i'th input value
    of j will set a '1' in the i'th row, j'th column of the
    output array.

    Example:
        v = np.array((1, 0, 4))
        one_hot_v = convertToOneHot(v)
        print one_hot_v

        [[0 1 0 0 0]
         [1 0 0 0 0]
         [0 0 0 0 1]]
    """

    assert isinstance(vector, np.ndarray)
    assert len(vector) > 0

    if num_classes is None:
        num_classes = np.max(vector)+1
    else:
        assert num_classes > 0
        assert num_classes >= np.max(vector)

    result = np.zeros(shape=(len(vector), num_classes))
    result[np.arange(len(vector)), vector] = 1
    return result.astype(int)



#one function do one thing
def sequence_n_gram_parsing(alist,n_gram=20,num_class=323):
    if len(alist) <= n_gram:
        return alist

    ans = []
    for i in range(0,len(alist)-n_gram+1,1):
        tmp = alist[i:i+n_gram]
        
        oneHot = convertToOneHot(np.asarray(tmp), num_class)
        ans.append(oneHot)

    #transform into nmup arrray
    ans = np.array(ans)
    return (ans)

def list_to_matrix(allthelist,n_gram=20):
    print("\n convert list to matrix")
    arraysize,arraycount= glbal.get_array_limit()
    arraylist = []
    array=None
    # array = sequence_n_gram_parsing(allthelist[0][:],n_gram=n_gram)
    # if len(allthelist) == 1 :
    #     arraylist.append(array)
    #     print(array.shape)
    #     return arraylist
    for i in range(0,len(allthelist),1):
        #limit series array list size
        if len(arraylist) > arraycount :
            print("\n reach limit of array list size")
            break 
        arraysize=arraysize if(len(allthelist[i])>arraysize) else len(allthelist[i])
        tmp = sequence_n_gram_parsing(allthelist[i][:arraysize],n_gram=n_gram)
        # limit signle series array size
        arraylist.append(tmp)
        percent = (i+0.0)/len(allthelist)
        utils.drawProgressBar(percent)
        #print ("array shape")
        #print (array.shape)

    for array in arraylist:
        print (array.shape)
    print ("done")

    return arraylist

def process_log(step='dvwa_train',save_into_pickle=False,n=20):
    att_arrlist=[]
    train_arrlist=[]
    val_arrlist=[]
    
    dir_mysql_train =glbal.get_data_dir("dir_mysql_train")  
    dir_mysql_test =glbal.get_data_dir("dir_mysql_test")  
    dir_dvwa_train =glbal.get_data_dir("dir_dvwa_train")
    dir_dvwa_test =glbal.get_data_dir("dir_dvwa_test")  
    dir_escp =glbal.get_data_dir("dir_escp")
    
    if step == 'dvwa_train':
        print('dvwa Train data processing ...........')
        all_train = get_all_call_sequences(dir_dvwa_train)
        train_arrlist=list_to_matrix(all_train,n_gram=n)
    if step == 'dvwa_test':
        print('dvwa test data processing ...........')
        all_train = get_all_call_sequences(dir_dvwa_test)
        train_arrlist=list_to_matrix(all_train,n_gram=n)
    if step == 'mysql_train':
        print('mysql Train data processing ...........')
        all_train = get_all_call_sequences(dir_mysql_train)
        train_arrlist=list_to_matrix(all_train,n_gram=n)
    if step == 'mysql_test':
        print('mysql test data processing ...........')
        all_train = get_all_call_sequences(dir_mysql_test)
        train_arrlist=list_to_matrix(all_train,n_gram=n)
    if step == 'escp':
        print('escape data processing ...........')
        alltrain = get_all_call_sequences(dir_escp,n_gram=n)
        train_arrlist=list_to_matrix(alltrain)
    if save_into_pickle :
        fpath="arrayfile/"+step+"/"
        for i in range (len(train_arrlist)):
            fname = fpath+step+str(i)+".pickle"
            utils.saveintopickle(train_arrlist[i],fname)    
            
    return train_arrlist

    
    
if __name__ == "__main__":
    glbal._init()
    runalone=True
    #glbal.set_debug()
    dir_dvwa_train =glbal.get_data_dir("dir_dvwa_train")
    #get_all_call_sequences(dir_dvwa_train)
    statis_ngram_dic("output/15gramdic_sorted.pickle")


