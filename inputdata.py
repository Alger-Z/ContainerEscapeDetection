#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ ="Ktian"
import os
import sys
import numpy as np

import io_helper

def readfilesfromAdir(datadir):
    #read a list of files
    files = os.listdir(datadir)
    files_absolute_paths = []
    for file in files:
        files_absolute_paths.append(os.path.join(datadir,str(file)))
    return files_absolute_paths


file = "ADFA-LD/Training_Data_Master/UTD-0001.txt"
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
    files = readfilesfromAdir(dire)
    allthelist = []
    print (len(files))

    for eachfile in files:
        if not eachfile.endswith("DS_Store"):
            allthelist.append(readCharsFromFile(eachfile))
        else:
            print ("Skip the file "+ str(eachfile))

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
def sequence_n_gram_parsing(alist,n_gram=20,num_class=341):
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

def list_to_matrix(allthelist,atype,n_gram=20,save=True):

    array = sequence_n_gram_parsing(allthelist[0])
    arraylist = []
    
    for i in range(1,len(allthelist),1):
        tmp = sequence_n_gram_parsing(allthelist[i])

        #print ("tmp shape")
        #print (tmp.shape)
        
        if (len(array)> 100):
            arraylist.append(array)
            array=tmp
        else:
            array = np.concatenate((array, tmp), axis=0)
        
        if len(arraylist) > 2 :
            break 
        percent = (i+0.0)/len(allthelist)
        io_helper.drawProgressBar(percent)

        #print ("array shape")
        #print (array.shape)

    for array in arraylist:
        print (array.shape)
    print ("done")
    
    if save :
        if '/' in atype:
            att_type,atype=atype.split('/')[1],atype.split('/')[0]
        fpath="arrayfile/"+atype+"/"
        for i in range (len(arraylist)):
            fname = fpath+att_type+str(i)+".pickle"
            io_helper.saveintopickle(arraylist[i],fname)
    return arraylist



if __name__ == "__main__":
    dirc = "ADFA-LD/Training_Data_Master/"
    dirc_val = "ADFA-LD/Validation_Data_Master/"
    dic_att ="ADFA-LD/Attack_Data_Master/"
    # train1 = get_all_call_sequences(dirc)

    # test = [i for i in range(0,300)]
    # array = sequence_n_gram_parsing(test)
    # print (type(array))
    # print (array.shape)

    # print('Train data processing ...........')
    # all_train = get_all_call_sequences(dirc)
    # list_to_matrix(all_train,'train')
    
    # print('Val data processing ...........')
    # all_val = get_all_call_sequences(dirc_val)
    # list_to_matrix(all_val,'val')
    
    print('Att data processing ...........')
    att_subdir=get_attack_subdir(dic_att)
    for att in att_subdir:
        all_att = get_all_call_sequences(att)
        list_to_matrix(all_att,'att'+'/'+os.path.basename(att))
