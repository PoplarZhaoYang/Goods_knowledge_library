#!/usr/bin/python
# -*- coding:'utf-8' -*-

import os
import sys
import pymongo
import pprint
import json
import logging
import bson
import logging
import codecs

try:
    import cPickle as pickle
except ImportError:
    import pickle

#the config of logging
logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', level = logging.INFO)

def set_make():

    ret = set()
    if os.path.exists('tmp/have_loaded_msg.set'):
        with open('tmp/have_loaded_msg.set', 'r') as f:
            ret = pickle.load(f)
    return ret


def dataFile(col, ofile, limit):
    """load the data from database and write into file
    """


    strSet = set_make()
    cnt = 0

    try:
        with codecs.open(ofile, 'w', encoding='utf-8') as f:
            for c in col.find():
                if c['act'] != 'close_send_msg': continue
                out = c['msg']
                strs = ""
                for substr in out:
                    strs += substr.strip()
                words = strs + "\n"
                #words = strs.encode('utf-8')
                if words and words not in strSet:
                    cnt += 1
                    strSet.add(words)
                    f.write(words)
                    limit -= 1
                if limit == 0:
                    break
    finally:
        with open('tmp/have_loaded_msg.set', 'w') as f:
                pickle.dump(strSet, f)
    logging.info('Have writen {0} chat answers into logs file!'.format(cnt))
    logging.info('There are {0} chat answers totally!'.format(len(strSet)))

def main():
    client = pymongo.MongoClient()
    db = client.xdrs
    col = db.logs
    dataFile(col, 'tmp/answer', 100000)

if __name__ == "__main__":
    main()







