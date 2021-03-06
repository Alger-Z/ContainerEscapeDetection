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
sequence_length = 19
epochs = 30
save=True
load =True
batch_size = 50
feature_dimension = 323
    

def save_model_weight_into_file(model, modelname="model.json", weight="model.h5"):
    model_json = model.to_json()
    with open(modelname, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(weight)
    print("Saved model to disk in {} and {}".format(modelname,weight))


def load_model_and_weight_from_file(modelname="model.json", weight="model.h5"):

    try:
        json_file = open(modelname, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(weight)
        print("Loaded model from disk, you can do more analysis more")
    except:
        print("Loaded model error")
        loaded_model=None
    
    return loaded_model

def get_topk_index_list(prob_list,k):
    return np.argsort(prob_list)[-k:]


def build_model(mod='lstm'):
    # if mod == 'lstm':
    #     return build_lstm
    
    model = Sequential()
    layers = {'input': feature_dimension, 'hidden1': 64, 'hidden2': 256, 'hidden3': 100, 'output': feature_dimension}

    model.add(LSTM(
            input_shape=(sequence_length,layers['input']),
            output_dim=layers['hidden1'],
            return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
            layers['hidden2'],
            return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
            layers['hidden3'],
            return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
            output_dim=layers['output'],activation='softmax'))
    #model.add(Activation("linear"))

    start = time.time()

    model.compile(loss="categorical_crossentropy", optimizer='rmsprop',  metrics=['accuracy'])
    #model.compile(loss="mse", optimizer="rmsprop")

    print ("Compilation Time : ", time.time() - start)
    return model


def run_network(model=None, train_data=None,act='train',n_gram=20):

    global_start_time = time.time()

    if act == 'train':
        print ('\n Loading  train data... ')
        xtrainlist, ytrainlist  = preprocess.preprocess(step='train',n=n_gram)
    
    if model is None and load is True:
        try :
            print("\n \n model load from file:",modname,modweight)
            model=load_model_and_weight_from_file(modelname=modname,weight=modweight)
        except Exception as e:
            print ('\n load model failed :%s',e)
    if model is None:
        model= build_model()
    
    print ('\n Model compile \n')
    model.compile(loss="categorical_crossentropy", optimizer='rmsprop',  metrics=['accuracy'])
    
    if act == 'train':
        for X_train,y_train in zip(xtrainlist,ytrainlist):    
            print ("\n X_train, y_train,shape")
            print (X_train.shape)
            print (y_train.shape)
            print ('\n \n Start Training...\n \n')
            history=model.fit(
                X_train, y_train,
                batch_size=batch_size,
                epochs=epochs,
                validation_split=0.05)
            model.summary()
        if save :
            save_model_weight_into_file(model,modelname=("output/model"+str(n_gram)+"gram.json"),weight=("output/model"+str(n_gram)+"gram.h5"))
            saveintopickle(history.history,("output/history"+str(n_gram)+"gram.txt"))
        print("\n Done Training...")
        


    

if __name__ == "__main__":
    action='train'
    glbal._init()
    debug = glbal.set_debug()
    #debug = glbal.get_debug()
    modname = "output/model20gram.json"
    modweight ="output/model20gram.h5"
    try: 
        if len(sys.argv) > 1 :
            action=sys.argv[1]
        if debug :
            epochs = 3
            save = False
        if action == 'train':
            load = False
        # n=[10,15,20,25]
        # for ngram in n :
        #     sequence_length=ngram-1
        #     print( "\n run for %s debug = %s epoch= %d save = %s ngram=%d").format(action,debug,epochs,save,ngram)
        #     run_network(act=action,n_gram=ngram)
        run_network(act=action,n_gram=20)
    except Exception as e:
        print(sys.argv,e)
