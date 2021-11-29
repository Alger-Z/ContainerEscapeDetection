# -*- coding:utf-8 -*-

import re
import os
import numpy as np
import random
import matplotlib.pyplot as plt
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
from keras.models import Sequential

class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.dim = len(word2vec.itervalues().next())

    def fit(self):
        return self

    # 遍历输入词序列中的每个词，取其在此项量表中的向量，若是改词不在词向量词表中（即训练集中未出现），则填0
    def transform(self, X):
        return np.array([np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                                or [np.zeros(self.dim)], axis=0)
                        for words in X
                        ])

def load_one_flle(filename):
    x = []
    with open(filename) as f:
        line = f.readline()
        x = line.strip('\n').split()
    return x

def load_adfa_training_files(rootdir):
    x = []
    y = []
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            x.append(load_one_flle(path))
            y.append(0)
    return x, y

def dirlist(path, allfile):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            allfile.append(filepath)
    return allfile

def load_adfa_webshell_files(rootdir):
    x = []
    y = []
    allfile=dirlist(rootdir,[])
    for file in allfile:
        if re.match(r"\./ADFA-LD/Attack_Data_Master/Web_Shell_\d+/UAD-W*", file):
            x.append(load_one_flle(file))
            y.append(1)
    return x, y

def word2idx(word,word_model):
  return word_model.wv.vocab[word].index

def idx2word(idx,word_model):
  return word_model.wv.index2word[idx]



def reduce_dimensions(model):
    num_dimensions = 2  # final num dimensions (2D, 3D, etc)

    vectors = [] # positions in vector space
    labels = [] # keep track of words to label our data again later
    for word in model.wv.vocab:
        vectors.append(model.wv[word])
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

def roc_plt(y_tar,y_prd):
    y_prd = [np.argmax(y) for y in y_prd]  # 取出y中元素最大值所对应的索引
    y_tar = [np.argmax(y) for y in y_tar]
    fpr, tpr, thresholds_keras = roc_curve(y_tar, y_prd) 
    auc_ = auc(fpr, tpr)
    print("AUC : ", auc_)
    plt.figure()
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr, tpr, label='S3< val (AUC = {:.3f})'.format(auc_))
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='best')
    plt.savefig('ROC.jpg')
    #plt.show()    
    
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
    fig_path =os.getcwd()+'/w2c.png'
    plt.savefig(fig_path)
    
def show_wv(model):
    print "word emberding vocab: ", model.wv.vocab.keys()
    # 生成词向量词表，每个词映射到向量
    words_vocab = dict()
    for key in model.wv.vocab.keys():
        nums = map(float, model[key])
        words_vocab[key] = np.array(nums)
    #二维展示词向量分布
    x_vals, y_vals, labels = reduce_dimensions(model)
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

if __name__ == '__main__':
    x1, y1 = load_adfa_training_files("./ADFA-LD/Training_Data_Master/")  # 训练集（normal）
    x2, y2 = load_adfa_webshell_files("./ADFA-LD/Attack_Data_Master/")    # 训练集（attack）
    x3, y3 = load_adfa_training_files("./ADFA-LD/Validation_Data_Master/")  # 验证集（normal）

    # 训练集黑白样本混合
    x_train = x1 + x2
    y_train = y1 + y2
    x_validate = x3 + x2
    y_validate = y3 + y2

    #w2c训练/加载
    modelpath = "./word2vec.test.txt"
    model = None
    if os.path.isfile(modelpath):
        # 导入模型
        print "load modeling..."
        model = gensim.models.Word2Vec.load(modelpath)
    else:
        # 将词嵌入到一个100维的向量空间中
        model = gensim.models.Word2Vec(x_train, min_count=1, size=50)
        # 保存模型
        model.save(modelpath)
    
    #提供给LSTM embedding层
    pretrained_weights = model.wv.syn0
    vocab_size, emdedding_size = pretrained_weights.shape
    #查看词向量结果
    #show_wv(model)
        
    
    # LSTM搭建
    modelpath2="./lstm.test.txt"
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=emdedding_size, 
                        weights=[pretrained_weights]))
    model.add(LSTM(units=emdedding_size))
    model.add(Dense(units=vocab_size))
    model.add(Activation('softmax'))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    
    history=model.fit(
                x1, y1,
                epochs=1,
                validation_split=0.05)
    model.summary()
    model.save(modelpath2)
    
    # Make predictions using the validate set
    y_pre = model.predict(x3)
    print "Predict result: ", y_pre
    roc_plt(x3,y_pre)
    # if 1 in y_pre:
    #     print y_pre.index(1)
    #     print "found 1 in pre"
'''
    meanVectorizer = MeanEmbeddingVectorizer(words_vocab)
    # 将训练语料经过词向量表编码成一个行向量（取均值）
    x_trainVecs = meanVectorizer.transform(x_train)
    #for i in range(len(x_train)):
    #    print x_train[i]
    #    print x_trainVecs[i]
    #    print ""
    # 将验证语料经过词向量表编码成一个行向量（取均值）
    x_validateVecs = meanVectorizer.transform(x_validate)
    #for i in range(len(x_train)):
    #    print x_validate[i]
    #    print x_validateVecs[i]
    #    print ""
    
    # 根据训练集生成KNN模型
    clf = KNeighborsClassifier(n_neighbors=4).fit(x_trainVecs, y_train)
    
    scores = cross_val_score(clf, x_trainVecs, y_train, n_jobs=-1, cv=10)
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
    print "Prediction accurate: %2f" % np.mean(y_pre == y_validate)
'''