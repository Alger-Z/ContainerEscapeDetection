#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas 
import os
import random
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.manifold import TSNE

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
