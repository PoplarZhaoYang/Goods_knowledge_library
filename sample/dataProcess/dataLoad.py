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
    stopWords = getStopWords("stopwords.txt")

    for c in stopWords:
        break
    ret = u""
    for s in seg:
        #do a special process about digit
        if isNumber(s):
            s = u"{数字}"

        #don't choos stopwords
        if s + u"\n" not in stopWords:
            ret += u"/" + s
    return ret + u"\n"



#open the col save into outfile
def dataFile(col, ofile):
    #set the number of answers
    limit = 1000
    strSet =set()

    with codecs.open(ofile, 'w', encoding='utf-8') as f:
        for c in col.find():
            out = c['answers']
            strs = u""
            for substr in out:
                strs += substr
            words = wordsRefine(strs)

            if words not in strSet:
                strSet.add(words)
                f.write(words)
                limit -= 1

            if limit == 0:
                break
    logging.info('Have write chat logs into logs file')

def main():
    client = pymongo.MongoClient()
    db = client.xdmp_bk
    col = db.question_b_shop_answer
    dataFile(col, 'answer')

if __name__ == "__main__":
    main()







