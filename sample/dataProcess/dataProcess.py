import pymongo
import pprint

#print all the data in a mongo collection
def datashow(col):
    for c in col.find():
        pprint.pprint(c)

def main():
    client = pymongo.MongoClient()
    db = client.xdrs
    col = db.logs
    datashow(col)

if __name__ == "__main__":
    main()







