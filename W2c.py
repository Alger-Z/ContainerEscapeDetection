# -*- coding:utf-8 -*-


import os
import numpy as np


# 
from sklearn.decomposition import IncrementalPCA    # inital reduction
from sklearn.manifold import TSNE                   # final reduction
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics import roc_curve
from sklearn.metrics import auc

from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model

from load_helper import *
from visualization import *
from utils import *

def word2idx(word,word_model):
  return word_model.wv.vocab[word].index

def idx2word(idx,word_model):
  return word_model.wv.index2word[idx]
   



class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.dim = len(word2vec.itervalues().next())

    def fit(self):
        return self

    # 遍历输入词序列中的每个词，取其在此向量表中的向量，若是词不在词向量词表中（即训练集中未出现），则填0
    def transform(self, X):
        return np.array([np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                                or [np.zeros(self.dim)], axis=0)
                        for words in X
                        ])
def build_lstm():
    # LSTM搭建
    
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=emdedding_size, 
                        weights=[pretrained_weights]))
    model.add(LSTM(units=emdedding_size,return_sequences=True))
    model.add(LSTM(units=emdedding_size,return_sequences=False))
    model.add(Dense(2, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    
    return model


if __name__ == '__main__':
    #action={0:"train",1:"predict",2:"debug"}
    act=0
    
#    x1, y1 = load_adfa_training_files("./ADFA-LD/Training_Data_Master/")  # 训练集（normal）
#    x2, y2 = load_adfa_webshell_files("./ADFA-LD/Attack_Data_Master/")    # 训练集（attack）
#    x3, y3 = load_adfa_training_files("./ADFA-LD/Validation_Data_Master/")  # 验证集（normal）
#    att_x,att_y =load_adfa_Attack_files("./ADFA-LD/Attack_Data_Master/")

    x1, y1 = load_training_files("/data/mysqltxt/mix")  # 训练集
    x2, y2 = load_training_files("data/dvwatxt/")    # 训练集
    esp_x,esp_y = load_escp_files("data/new/")  # 测试集
    
    # 训练集黑白样本混合
    x_train_mixed = x1[:2000] + att_x
    y_train_mixed = y1[:2000] + att_y
    x_validate_mixed = x3[:2000] + att_x
    y_validate_mixed = y3[:2000] + att_y
    x_=x1+x2+x3
    y_=y1+y2+y3
    
    modelpath = "./word2vec.test.txt"
    modelpath2="./lstm.h5"
    
    model = None
    wv_model=None
    #w2c训练/加载
    if os.path.isfile(modelpath):
        # 导入模型
        print "load w2c modeling..."
        wv_model = gensim.models.Word2Vec.load(modelpath)
    else:
        # 将词嵌入到一个50维的向量空间中
        wv_model = gensim.models.Word2Vec(x_, min_count=1, size=50)
        # 保存模型
        wv_model.save(modelpath)
    
    #提供给LSTM embedding层
    pretrained_weights = wv_model.wv.syn0
    vocab_size, emdedding_size = pretrained_weights.shape
    #查看词向量结果
    print "word emberding vocab: ", wv_model.wv.vocab.keys()
    # 生成词向量词表，每个词映射到向量
    words_vocab = dict()
    for key in wv_model.wv.vocab.keys():
        nums = map(float, wv_model[key])
        words_vocab[key] = np.array(nums)
    #
    
    #show_wv(model.wv.vocab.keys(),wv_model.wv)

    # 尝试用预训练embedding的lstm做文本分类问题如下：
    # 1 输入没搞懂，现在将样本序列切并填充到指定长度，然后经过词向量编码取均值变成行向量。y是1,0标签。
    # 看kaggle示例代码作文本分类，输入用的是w2v的词库idx转化，一个词对应一个整数，然后分类也映射到整数
    # 我的预测输出是对应到词表的向量概率分布。。。不知道怎么回事
    
    # lstm 输入填充 
    # from keras.preprocessing import sequence
    # maxlen = 300
    # xtr_pad=sequence.pad_sequences(x_train_mixed,maxlen=maxlen)
    # xte_pad=sequence.pad_sequences(x_validate_mixed,maxlen=maxlen)
    
    # #正常样本词向量化,将训练语料经过词向量表编码成一个行向量（取均值）
    # meanVectorizer = MeanEmbeddingVectorizer(words_vocab)
    # xtrain_vecs = meanVectorizer.transform(xtr_pad)
    # xtest_vecs=meanVectorizer.transform(xte_pad)
    
    # foundone(y_validate_mixed,"yval")
    # foundone(y_train_mixed,"ytrain")
    
    # if os.path.isfile(modelpath2):
    #     # 导入模型
    #     print "load lstm modeling..."
    #     model = load_model(modelpath2)
    # else:
    #     model=build_lstm()
    #     history=model.fit(
    #                 xtrain_vecs, y_train_mixed,
    #                 epochs=50,
    #                 validation_split=0.05)
    #     model.summary()
    #     model.save(modelpath2)
    #     saveintopickle(history.history,"tr_history.txt")
    
    # # Make predictions using the validate set
    # if act == 1 :
    #     y_pre = model.predict(xtest_vecs)
    #     print "Predict result: ", y_pre
        
    #     #foundone(y_pre,"ypre")

    #     roc_plt(y_validate_mixed,y_pre)
    # # if 1 in y_pre:
    #     print y_pre.index(1)
    #     print "found 1 in pre"

    
    
    #knn
    meanVectorizer = MeanEmbeddingVectorizer(words_vocab)
    
    x_trainVecs = meanVectorizer.transform(x_train_mixed)
    #for i in range(len(x_train)):
    #    print x_train[i]
    #    print x_trainVecs[i]
    #    print ""
    # 将验证语料经过词向量表编码成一个行向量（取均值）
    x_validateVecs = meanVectorizer.transform(x_validate_mixed)
    #for i in range(len(x_train)):
    #    print x_validate[i]
    #    print x_validateVecs[i]
    #    print ""
    
    # 根据训练集生成KNN模型
    clf = KNeighborsClassifier(n_neighbors=4).fit(x_trainVecs, y_train_mixed)
    
    scores = cross_val_score(clf, x_trainVecs, y_train_mixed, n_jobs=-1, cv=10)
    # 反映KNN模型训练拟合的程度
    print "Training accurate: "
    print scores
    print np.mean(scores)

    # Make predictions using the validate set
    y_pre = clf.predict(x_validateVecs)
    print "Predict result: ", y_pre
    # if 1 in y_pre:
    #     print y_pre.index(1)
    #     print "found 1 in pre"
 
    # 预测的准确度
    print "Prediction accurate: %2f" % np.mean(y_pre == y_validate_mixed)
