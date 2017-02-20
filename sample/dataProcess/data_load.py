import pymongo
import pprint
import json
import logging
import bson
import codecs

#print all the data in a mongo collection
def dataShow(col):
    for c in col.find():
        pprint.pprint(c)


#open the col save into outfile
def dataFile(col, ofile, limit):
    #the set number of answers
    strSet = set()
    cnt = 0

    with codecs.open(ofile, 'w', encoding='utf-8') as f:
        for c in col.find():
            out = c['answers']
            strs = ""
            for substr in out:
                strs += substr
            strs += "\n"
            words = strs.encode('utf-8')
            if words and words not in strSet:
                cnt += 1
                strSet.add(words)
                f.write(words)
                limit -= 1
            if limit == 0:
                break
    logging.info('Have writen {0} chat answers into logs file!'.format(cnt)} 

def main():
    client = pymongo.MongoClient()
    db = client.xdmp_bk
    col = db.question_b_shop_answer
    dataFile(col, 'tmp/answer', 10000)

if __name__ == "__main__":
    main()







