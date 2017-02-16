import pymongo
import pprint
import json
import logging
import bson

#print all the data in a mongo collection
def dataShow(col):
    for c in col.find():
        pprint.pprint(c)


#open the col save into outfile
def dataFile(col, ofile):
    #set the number of answers
    limit = 1000

    with open(ofile, 'w') as f:
        for c in col.find():
            out = c['answers']
            strs = ""
            for substr in out:
                strs += substr
            strs += "\n"
            words = strs.encode('utf-8')
            if words:
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







