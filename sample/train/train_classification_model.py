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
from sklearn.svm import SVC 
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfTransformer

try:
    import cPickle as pickle
except ImportError:
    import pickle


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

    #TF-IDF向量加权处理
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(s)
    return csr_matrix(tfidf.toarray())

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


class Validation(object):
    """验证模型的类
    """

    def __init__(self, AI, trainX, trainy, testX, testy):
        self.AI = AI
        self.trainX = trainX
        self.trainy = trainy
        self.testX = testX
        self.testy = testy

    def normal_val(self):
        self.AI.fit(self.trainX, self.trainy)
        predicted = self.AI.predict(self.testX)
        target_names = ['非商品知识', '是商品知识']
        print ""
        print classification_report(self.testy, predicted, target_names = target_names)
        print "\n混淆矩阵："
        print confusion_matrix(self.testy, predicted)
    
    def cross_val(self):
        scores = cross_val_score(self.AI, self.trainX, self.trainy, cv = 5, scoring='precision')
        print "Precision: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2) 
        scores = cross_val_score(self.AI, self.trainX, self.trainy, cv = 5, scoring='recall')
        print "Recall: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2) 


    def self_test(self, X, y):
        """test the model use the train data
        """

        self.AI.fit(X, y)
        predicted = self.AI.predict(X)
        print "accuracy:" + str(np.mean(predicted == y))
        print classification_report(y, predicted)
        print confusion_matrix(y, predicted)



def makePara(start, end, bas):
    ret = []
    while start <= end:
        ret.append(start)
        start += bas
    return ret

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

        trainX, testX, trainy, testy = train_test_split(
            X, y, test_size = 0.3, random_state=0)

       
        """GridSearch
        pg = makePara(0, 0.2, 0.2 / 10)
        pC = makePara(1, 20, 20 / 10)
        tuned_parameters = [{'kernel': ['rbf'], 'gamma': pg,
            'C': pC}]

        #rbf C=9, gama=0.08
        clf = GridSearchCV(SVC(C=1), tuned_parameters, cv = 5, scoring='accuracy', n_jobs=-1)
        clf.fit(trainX, trainy)
        
        print clf.best_score_
        print clf.best_params_
        """

        clf = SVC(C=9, gamma=0.08, kernel='rbf')
        clf.fit(X, y)

        pickled_clf = pickle.dumps(clf)

        with open('tmp/clf.model', 'w') as f:
            logging.info("Have save the train model to tmp/clf.model ")
            f.write(pickled_clf)



        """test
        val = Validation(clf, trainX, trainy, testX, testy)
        val.normal_val()
        val.cross_val()
        val.self_test(X, y)
        """


if __name__ == '__main__':
    main()








