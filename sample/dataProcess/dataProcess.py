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
    with open('chatLogs', 'w') as f:
        for c in col.find():
            out = c['snick'].encode('utf-8').strip() + " "
            out += c['cnick'].encode('utf-8').strip() + " "
            out += c['msg'].encode('utf-8').strip()
            out += "\n"
            f.write(out)
    logging.warning('Have write chat logs into logs file')

def main():
    client = pymongo.MongoClient()
    db = client.xdrs
    col = db.logs
    dataFile(col)

if __name__ == "__main__":
    main()







