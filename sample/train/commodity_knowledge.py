#!/usr/bin/python
# -*- coding=utf-8 -*-

"""The module choose the chat logs which are about commodity knowledge and distinct them into k logs to show.

    Author: Zhao Yang(jibancanyang@foxmail.com)
"""

import codecs
import logging
import jieba
import numpy as np
from scipy.sparse import csr_matrix
from gensim import corpora
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans

try:
    import cPickle as pickle
except ImportError:
    import pickle

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)


class DataWasher:
    """transform the documents to vectors
    """

    def __init__(self, dictionary, document=[], matrix=[[]]):
        self.dictionary = dictionary
        self.document = document
        self.raw_document = document
        self.matrix = csr_matrix(matrix)
        self.filtered_document = []

    def data_load(self, file_name, numbers=-1):
        """load the text from file_name to document list
        """

        i = 0
        with codecs.open(file_name, encoding='utf-8') as f:
            ret = []
            for c in f:
                if c != "" and c != "\n":
                    ret.append(c)
                    i += 1
                if i == numbers: break
            self.raw_document = self.document = ret

    def is_number(self, cur):
        if len(cur) > 0:
            if cur[0] >= u'\u0030' and cur[0] <= u'\u0039':
                return True
        return False

    def document_to_vector(self):
        """separate the document into words and remove stop words, then transformer into matrix.

        * the power for every element in the matrix is weighted by tf-idf.
        """

        with codecs.open('../dataProcess/tmp/stopwords.txt') as f:
            stop_words = set(f.readlines())

        temp = []
        for doc in self.document:
            seg = jieba.cut(doc, cut_all=True)
            ret = u""
            for s in seg:
                if self.is_number(s):
                    s = u"{数字}"
                if s + u"\n" not in stop_words:
                    ret += u"/" + s
            temp.append(ret)

        self.document = temp
        vectors = [self.dictionary.doc2bow(c.split('/')) for c in self.document]

        col = len(self.dictionary.keys())
        row = len(self.document)
        logging.info("this is a {0} X {0} vector matrix".format(row, col))
        matrix = np.zeros((row, col))

        i = 0
        for c in vectors:
            for d in c:
                matrix[i][d[0]] = d[1]
            i += 1

        transformer = TfidfTransformer()
        tf_idf = transformer.fit_transform(matrix)
        #self.matrix = csr_matrix(tf_idf.toarray())
        self.matrix = tf_idf.toarray()
        return self.matrix

    def filter(self):
        with open('tmp/clf.model', 'r') as f:
            logging.info("Have loaded the train model in 'tmp/clf.model' ")
            clf = pickle.loads(f.read())
        filtered = self.matrix[0]
        i = 0
        for c in self.matrix:
            if (clf.predict(c.reshape((1,-1))) == [1]):
                filtered = np.row_stack((c, filtered))
                self.filtered_document.append(self.raw_document[i])
            i += 1

        self.matrix = filtered
        logging.info("there is a {0} matrix.".format(self.matrix.shape))
        return self.matrix


def clustering(matrix, k = 20):
    """return the labels of k import chart logs
    """
    kmeans = KMeans(n_clusters=k, random_state=0).fit(matrix)
    distance = kmeans.transform(matrix)
    min_distance = [10000000] * k
    min_id = [0] * k
    t = 0
    for c in distance:
        for i in range(k):
            if c[i] < min_distance[i]:
                min_distance[i] = c[i]
                min_id[i] = t
        t += 1

    return min_id
        

    



def main():
    # load the dictionary defined before

    dictionary = corpora.dictionary.Dictionary.load('tmp/trainDict.dict')
    data = DataWasher(dictionary)
    data.data_load('../dataProcess/tmp/answer', 100000)
    data.document_to_vector()
    data.filter()

    #show filtered chat logs
    #for c in data.filtered_document:
    #    print c


    display_id = clustering(data.matrix, 15)
    for i in display_id:
        print data.filtered_document[i]


if __name__ == '__main__': main()
