#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import time
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.models import model_from_json
from utils import saveintopickle
import sys
from W2c import build_lstm
import preprocess
from visualization import *
import glbal

# Global hyper-parameters

def load_model_and_weight_from_file(modelname="model.json", weight="model.h5"):

    try:
        json_file = open(modelname, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(weight)
        print("Loaded model from disk, you can do more analysis more")
    except Exception as e:
        print("Loaded model error:",e)
        loaded_model=None
    
    return loaded_model

def get_topk_index_list(prob_list,k):
    return np.argsort(prob_list)[-k:]



def predict(model=None,act='test',n_gram=20):

    global_start_time = time.time()

    if act == 'test':
        print ('\n Loading  test data... ')
        xtestlist,ytestlist = preprocess.preprocess(step='test',n=n_gram)
    if act == 'escp':
        print ('\n Loading  escp data... ')
        xtestlist,ytestlist = preprocess.preprocess(step='escp',n=n_gram)
 
    
    
    if model is None:
        try :
            print("\n \n model load from file:{} {} \n \n".format(modname,modweight))
            model=load_model_and_weight_from_file(modelname=modname,weight=modweight)
        except Exception as e:
            print ('\n load model failed :{}'.format(e))
            return
    model.compile(loss="categorical_crossentropy", optimizer='rmsprop',  metrics=['accuracy'])
   
    acc=[] 
    
    print("\n \n Start predicting \n \n")
    count =1 
    for xtest,ytest in zip(xtestlist,ytestlist):
        print("\n \n predicting for testlist {} \n \n".format(count))
        count+=1
        predicted = model.predict(xtest[:sq_size])
        if save :
            saveintopickle(predicted,"output/predict.pickle")
            saveintopickle(ytest[:sq_size],"output/ytest.pickle")
        if pic:
            sq_prob_pic(ytrue=ytest[:sq_size],pred=predicted,name="dvwa_test")
        
        y_prd = [np.argmax(y) for y in predicted]  # 取出y中元素最大值所对应的索引
        y_tr = [np.argmax(y) for y in ytest[:sq_size]]
        acc=0
        for yp,yt in zip(y_prd,y_tr):
            if yp == yt :
                acc =acc+1
        acc= acc/float(len(y_prd))
        print ("\n acc for len {} : {} ".format(len(y_prd),acc ))
        
        #roc_plt(predicted,ytest)
        
        # print("Reshaping predicted")
        # predicted = np.reshape(predicted, (predicted.size,))
        break
        
    print("done")


if __name__ == "__main__":
    glbal._init()
    debug = glbal.set_debug()
    #debug = glbal.get_debug()
    act = 'test'
    ngram=20
    sq_size=2000
    save= False
    pic =False
    load =True
    modname = "output/model"+str(ngram)+"gram.json"
    modweight ="output/model"+str(ngram)+"gram.h5"
    predict(act=act,n_gram=ngram)
