#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import time
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.models import model_from_json

import sys
import preprocess
from visualization import roc_plt

# Global hyper-parameters
sequence_length = 19
epochs = 3
batch_size = 50
feature_dimension = 341


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

def build_model():
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

    print "Compilation Time : ", time.time() - start
    return model


def run_network(model=None, train_data=None,act='train'):

    global_start_time = time.time()

    if train_data is None:
        print 'Loading data... '
        if act == 'train':
            xtrainlist, ytrainlist  = preprocess.preprocess()
        if act == 'predict':
            xtestlist,ytestlist = preprocess.preprocess(step='test')
        if act == 'att':
            xtestlist,ytestlist = preprocess.preprocess(step='att')
        if act == 'escp':
            xtestlist,ytestlist = preprocess.preprocess(step='escp')
    else:
        X_train, y_train = train_data
    
    
    if model is None:
        try :
            model=load_model_and_weight_from_file()
        except Exception as e:
            print 'load model failed :',e
        if model is None:
            model= build_model()
    
    print 'Model compile'
    model.compile(loss="categorical_crossentropy", optimizer='rmsprop',  metrics=['accuracy'])
    if act == 'train':
        print("Training...")
        for X_train,y_train in zip(xtrainlist,ytrainlist):    
            print ("X_train, y_train,shape")
            print (X_train.shape)
            print (y_train.shape)
            print '\n \n Data Loaded. Compiling...\n \n'
            history=model.fit(
                X_train, y_train,
                batch_size=batch_size,
                epochs=epochs,
                validation_split=0.05)
            model.summary()
        save_model_weight_into_file(model)
        print("Done Training...")
    if act == 'predict' or 'att' or 'escp':
        acc=[] 
        for xtest,ytest in zip(xtestlist,ytestlist):
            print("\n \n predicting \n \n")
            predicted = model.predict(xtest)
            
            y_prd = [np.argmax(y) for y in predicted]  # 取出y中元素最大值所对应的索引
            y_tr = [np.argmax(y) for y in ytest]
            acc=0
            for yp,yt in zip(y_prd,y_tr):
                if yp == yt :
                    acc =acc+1
            acc= acc/float(len(y_prd))
            print ("acc for len %d : %f ",len(y_prd),acc )
            #roc_plt(predicted,ytest)
            
            # print("Reshaping predicted")
            # predicted = np.reshape(predicted, (predicted.size,))
            
            # plt.figure(1)
            # plt.subplot(311)
            # plt.title("Actual Test Signal w/Anomalies")
            # plt.plot(ytest[:len(ytest)], 'b')
            # plt.subplot(312)
            # plt.title("Predicted Signal")
            # plt.plot(predicted[:len(ytest)], 'g')
            # plt.subplot(313)
            # plt.title("Squared Error")
            # mse = ((ytest - predicted) ** 2)
            # plt.plot(mse, 'r')
            # #plt.show()
            # fig_path =os.getcwd()+'/test.png'
            # plt.savefig(fig_path)
            #break 
        print("done")


    

if __name__ == "__main__":
    try: 
        action=sys.argv[1]
        print( "run for %s",action)
        run_network(act=action)
    except Exception as e:
        print(sys.argv,e)
