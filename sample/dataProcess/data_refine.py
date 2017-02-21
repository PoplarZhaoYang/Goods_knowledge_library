#!/usr/bin/python
#-*- coding:utf-8 -*-

import pymongo
import pprint
import jieba
import json
import logging
import bson
import codecs

#print all the data in a mongo collection
def dataShow(col):
    for c in col.find():
        pprint.pprint(c)

#return a set include stopwrods
def getStopWords(fileName):
    with codecs.open(fileName, 'r', encoding='utf-8') as f:
         ret = set(f.readlines())
         return ret

#judge if a Unicode is number
def isNumber(cur):
    if len(cur) > 0:
        if cur[0] >= u'\u0030' and cur[0] <= u'\u0039':
            return True
    return False

#split the words and delete stopwords
def wordsRefine(words):
    seg = jieba.cut(words, cut_all = True)
    stopWords = getStopWords("tmp/stopwords.txt")

    ret = u""
    for s in seg:
        #do a special process about digit
        if isNumber(s):
            s = u"{数字}"

        #don't choos stopwords
        if s + u"\n" not in stopWords:
            ret += u"/" + s
    return ret



#open the col save into outfile
def dataFile(ofile):

    with codecs.open(ofile, 'r', encoding='utf-8') as f:
        answer = f.readlines()
    with codecs.open(ofile, 'w', encoding='utf-8') as f:
        for strs in answer:
            words = wordsRefine(strs)
            print words
            #f.write(words)


def main():
    dataFile('tmp/answer')

if __name__ == "__main__":
    main()







