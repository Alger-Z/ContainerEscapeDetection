#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logging import debug
import os
import sys
import numpy as np
import io_helper
mydebug=False

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


def get_all_call_sequences(dire):
    try:
        files = dirlist(dire,[])
    except Exception as e:
        print ("%s dir error",dire)
        return []
    allthelist = []
    #print (len(files))
    for eachfile in files: 
        allthelist.append(readCharsFromFile(eachfile))  

    elements = []
    for item in allthelist:
        for key in item:
            if key not in elements:
                elements.append(key)

    elements = map(int,elements)
    elements = sorted(elements)

    print ("The total unique elements:")
    print (elements)

    print ("The maximum number of elements:")
    print (max(elements))

    #print ("The length elements:")
    #print (len(elements))
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

"""
The num_class here is set as 341
"""

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
    global mydebug
    if mydebug :
        arraysize = 2000
        arraycount=2 
    else :
        arraysize = 1000000
        arraycount=10
    array = sequence_n_gram_parsing(allthelist[0][:],n_gram=n_gram)
    arraylist = []
    if len(allthelist) == 1 :
        arraylist.append(array)
        print(array.shape)
        return arraylist
    for i in range(1,len(allthelist),1):
        tmp = sequence_n_gram_parsing(allthelist[i][:],n_gram=n_gram)
        
        if (len(array)> arraysize):
            arraylist.append(array)
            array=tmp
        else:
            array = np.concatenate((array, tmp), axis=0)
        
        if len(arraylist) > arraycount :
                break 
            
        percent = (i+0.0)/len(allthelist)
        io_helper.drawProgressBar(percent)

        #print ("array shape")
        #print (array.shape)

    for array in arraylist:
        print (array.shape)
    print ("done")

    return arraylist

def process_log(step='dvwa_train',save=False,n=20):
    att_arrlist=[]
    train_arrlist=[]
    val_arrlist=[]
    
    dir_mysql_train = "data/mix_txt"
    dir_mysql_test = "data/mysqltxt_test"
    dir_dvwa_train ="data/dvwatxt"
    dir_dvwa_test = "data/dvwatxt_test"
    dir_escp="data/att_withreq"
    
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
    if save :
        fpath="arrayfile/"+step+"/"
        for i in range (len(train_arrlist)):
            fname = fpath+step+str(i)+".pickle"
            io_helper.saveintopickle(train_arrlist[i],fname)    
            
    return train_arrlist

    
    
if __name__ == "__main__":
    mydebug =True
    process_log(step='dvwa_train')


