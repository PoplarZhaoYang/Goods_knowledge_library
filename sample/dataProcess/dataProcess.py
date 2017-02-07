import pymongo
import pprint
import json
import logging
import bson

#print all the data in a mongo collection
def dataShow(col):
    for c in col.find():
        pprint.pprint(c)

def dataFile(col):
    #set the number of answers
    limit = 1000

    with open('answer', 'w') as f:
        for c in col.find():
            out = c['answers']
            strs = ""
            for substr in out:
                strs += substr
            strs += "\n"
            f.write(strs.encode('utf-8'))

            limit -= 1
            if limit == 0:
                break

    logging.warning('Have write chat logs into logs file')

def main():
    client = pymongo.MongoClient()
    db = client.xdmp_bk
    col = db.question_b_shop_answer
    dataFile(col)

if __name__ == "__main__":
    main()







