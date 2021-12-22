#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numpy.lib.shape_base import expand_dims
import pandas 
import os
import random
from utils import loadfrompickle
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.manifold import TSNE
from keras.utils import plot_model
from keras.models import model_from_json

from utils import foundone                   # final reduction
    
def wv_2d(x_vals, y_vals, labels):
    random.seed(0)
    plt.figure(figsize=(12, 12))
    plt.scatter(x_vals, y_vals)

    #
    # Label randomly subsampled 25 data points
    #
    indices = list(range(len(labels)))
    selected_indices = random.sample(indices, 200)
    for i in selected_indices:
        plt.annotate(labels[i], (x_vals[i], y_vals[i]))
    #plt.show()
    fig_path ='pic/w2c.png'
    plt.savefig(fig_path)
    

def reduce_dimensions(words,words_vec):
    num_dimensions = 2  # final num dimensions (2D, 3D, etc)

    vectors = [] # positions in vector space
    labels = [] # keep track of words to label our data again later
    for word in words:
        vectors.append(words_vec[word])
        labels.append(word)

    # convert both lists into numpy vectors for reduction
    vectors = np.asarray(vectors)
    labels = np.asarray(labels)

    # reduce using t-SNE
    vectors = np.asarray(vectors)
    tsne = TSNE(n_components=num_dimensions, random_state=0)
    vectors = tsne.fit_transform(vectors)

    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]
    return x_vals, y_vals, labels

def show_wv(words_vocab,words_vec):

    #二维展示词向量分布
    x_vals, y_vals, labels = reduce_dimensions(words_vocab,words_vec)
    wv_2d(x_vals, y_vals, labels)
    
    # 测试sc编号40-70的近义词组
    # siml=[]
    # for x in range(40,70,1):
    #     sc = str(x)
    #     try:
    #         idxlist=model.wv.most_similar_cosmul(sc)
    #         similar,max_value=max(idxlist,key=lambda item:item[1])
    #         print (sc,similar,'\n')
    #     except:
    #         continue
    

def sq_prob_pic(ytrue,pred,name):
    plt.figure(1)
    plt.title("Syscall subsequence probilities")
    y_tr_index = [np.argmax(y) for y in ytrue] # 得到真实系统调用index 的列表
    prob = [pred[it][y_tr_index[it]] for it in range (len(y_tr_index))] # 查找得到对应概率列表
    prob_sq=1
    prob_sq_list=[]
    for i in range (0,10,1):
        prob_sq*=prob[i]
    for i in range(10,len(prob),1):
        prob_sq =prob_sq*prob[i]/prob[i-10]
        prob_sq_list.append(prob_sq)
    # prob = [prob[x]  for x in range(0,len(prob),1) ] #直接给出目标系统调用概率变化
    plt.plot(prob_sq_list, 'b')
    plt.savefig('pic/'+name+".png")
    
def acc_loss_plt(history,pic_name):
    plt.figure()
    
    plt.subplot(211)
    plt.plot(history['acc'])
    plt.plot(history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')

    # 绘制训练 & 验证的损失值
    plt.subplot(212)
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    
    plt.savefig('pic/'+pic_name+"_loss.png")

def roc_plt(y_true,y_prd):
    y_prd = [np.argmax(y) for y in y_prd]  # 取出y中元素最大值所对应的索引
    y_tr = [np.argmax(y) for y in y_true]
    # y_p=[]
    # for res in y_prd:
    #     y_p.append(y_prd.index(np.max(res)))
    # foundone(y_prd)
    # foundone(y_tr)
    
    fpr, tpr, thresholds_keras = roc_curve(y_tr, y_prd) 
    auc_ = auc(fpr, tpr)
    print("AUC : ", auc_)
    plt.figure()
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr, tpr, label='S3< val (AUC = {:.3f})'.format(auc_))
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='best')
    plt.savefig('pic/ROC.png')
    
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
if __name__ == '__main__':
    #预测过程分析
    historyfile = "output/history15gram.txt"
    history=loadfrompickle(historyfile)
    acc_loss_plt(history=history,pic_name=os.path.basename(historyfile).split(".")[0])
    
    # 模型可视化
    # model=load_model_and_weight_from_file()
    # plot_model(model,to_file="pic/model.png",show_shapes=True)
    
    #预测结果分析
    # prd= loadfrompickle("predict.pickle")
    # ytest=loadfrompickle("ytest.pickle")
    # sq_prob_pic(ytest,prd,"dvwa_test")