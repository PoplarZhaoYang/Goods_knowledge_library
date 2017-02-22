#!/usr/bin/python
#-*- coding=utf-8 -*-

import os
import sys
import json
import codecs
import random
import cPickle
import logging
import pandas as pd
import numpy as np
import jieba
from collections import defaultdict
from pprint import pprint
from gensim import matutils, corpora, models
from scipy.sparse import csr_matrix


#日志输出格式设置
logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', level=logging.INFO)

def isNumber(cur):
    if len(cur) > 0:
        if cur[0] >= u'\u0030' and cur[0] <= u'\u0039':
            return True
    return False


def getStopWords(fileName):
    with codecs.open(fileName, 'r', encoding='utf-8') as f:
         ret = set(f.readlines())
         return ret


def answer_refine(d):
    """把字典的answer内容，分词去停用词
    """

    words = d['answer']
    seg = jieba.cut(words, cut_all = True)
    stopWords = getStopWords("../dataProcess/tmp/stopwords.txt")
    ret = u""
    for s in seg:
        if isNumber(s):
            s = u"{数字}"
        if s + u"\n" not in stopWords:
            ret += u"/" + s
    d['answer'] = ret
    return d
    





#显然训练数据不是标准的json，需要先预处理成一个成员为字典的list
def preprocess(trainDataPath):
    with codecs.open(trainDataPath, 'r+', encoding='utf-8') as f:
        stemp = f.read()
        #数据文本的处理，包括划分，切开，将字符串构造为字典
        stemp = stemp.replace('}{', '}|{')
        stemp = stemp.replace('\\n', '')
        slist = stemp.split('|')
        for i in range(len(slist) - 1):   
            slist[i] = eval(slist[i])
            slist[i]['answer'].decode('utf-8')
        alist = []
        for c in slist:
            if isinstance(c, dict):
                c = answer_refine(c)
                alist.append(c)
        logging.info("Have loaded {0} answer sentences!".format(len(alist)))
        random.shuffle(alist)
        return alist 



#根据slist建立数据字典
def buildDataDict(slist, persist=True, once=True):
    #全部词语表示成二维list 
    texts = []
    for c in slist:
        if not isinstance(c, dict):
            continue
        sent = c['answer']
        text = sent.split('/')
        if len(text) >= 2:
            texts.append(text)
    
    #去除只出现一次的词语
    if once:
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1
        texts = [[token for token in text if frequency[token] > 1]
                 for text in texts]
    
    dictionary = corpora.Dictionary(texts)
    #logging.info("Numbers of key are:{0}".format(dictionary.keys())) 
    if persist:
        dictionary.save('tmp/trainDict.dict')
    return dictionary

#根据字典把每个文本向量化，返回scipy的csr稀疏矩阵
def getTrainVector(tList, dictionary):
    trainVector = [dictionary.doc2bow(c['answer'].split('/')) for c in tList]
    #pprint (trainVector[0:10])
    col = len(dictionary.keys())
    row = len(tList)
    logging.info("this is a {0} x {1} vector matrix".format(row, col))
    s = np.zeros((row, col))
    
    #根据tList建立矩阵
    i = 0
    for c in trainVector:
        for d in c:
            s[i][d[0]] = d[1]
        i += 1

    return csr_matrix(s)

#训练集的输出y
def getTrainLabel(trainList):
    y = []
    positiveSample = 0
    for c in trainList:
        if c['tag'] == True:
            positiveSample += 1
        y.append(c['tag'])
    logging.info("The  proportion of positive samples are {0}".format(1.0 * positiveSample / len(trainList)))
    return y


#0.70 n_neighbors = 3
def knnModel():
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier()
    knn.n_neighbors = 3
    return knn

#0.80 C=1e0
def logisticRegressionModel():
    from sklearn import linear_model
    return linear_model.LogisticRegression(C=1e0)

#0.78 kernel = 'linear'
def svmModel():
    from sklearn import svm
    svc = svm.SVC(kernel='linear')
    return svc


def main():
    trainDataPath = '../dataProcess/tmp/sourceData'
    trainList = preprocess(trainDataPath)
    dictionary = buildDataDict(trainList, once=True) #once表示是否去除只出现一次的词语
    if os.path.exists('model/CKL1.model'):
        with open('model/CKL1.model', 'rb') as f:
            clf = cPickle.load(f)
            logging.info("Have loaded classify model from file successfully!")
    else:
        X = getTrainVector(trainList, dictionary)
        y = getTrainLabel(trainList)
        dataNumbers = len(y)
        gap = dataNumbers * 7 // 10 

        trainX = X[:gap]
        trainy = y[:gap]
        testX = X[gap:]
        testy = y[gap:]

        AI = svmModel()
        #AI = logisticRegressionModel()

        print AI.fit(trainX, trainy)
        predicted = AI.predict(testX)
        print "The accuracy is:{0}".format(np.mean(predicted == testy))


if __name__ == '__main__':
    main()



        
        



