#!/usr/bin/env python
# -*- coding:'utf-8' -*-
import codecs
import json
import os, sys


try:
    import cPickle as pickle
except ImportError:
    import pickle

#make the file which has chat log into list 
def makeDictList(fileName):
    ret = []
    dictSet = set() #include the answer which have been marked
    if os.path.exists('tmp/have_marked_answer.dict'):
        with open('tmp/have_marked_answer.dict', 'r') as f:
            ret = pickle.load(f)
        with open('tmp/have_marked_answer.set', 'r') as f:
            dictSet = pickle.load(f)


    with codecs.open(fileName, 'r', encoding = 'utf-8') as f:
        an = f.readlines()
        for a in an:
            b = {u'answer': a, u'tag': -1}
            if a not in dictSet:
                dictSet.add(a)
                ret.append(b)

        with open('tmp/have_marked_answer.dict', 'w') as dicts:
            pickle.dump(ret, dicts)
        with open('tmp/have_marked_answer.set', 'w') as dicts:
            pickle.dump(dictSet, dicts)
        return ret

#mark the content of the list and save into a file in json format
def markList(fileName):
    dicts = makeDictList("tmp/answer")
    with codecs.open(fileName, 'a', encoding = 'utf-8') as temp:
        cnt = 0
        for c in dicts:
            if c['tag'] != -1:
                continue
            jt = json.dumps(c, encoding='utf-8', ensure_ascii=False)
            print '\n' + jt + " [{0}]".format(cnt)

            #operator
            ansStr = raw_input("Is it about the knowledge of commodity?")
            if ansStr == "q":
                break
            if ansStr == "":
                print "please input number!!!!"
                continue
            else:
                ans = int(ansStr)

            c['tag'] = 1 if ans == 1 else 0
            cnt += 1

            ojs = json.dumps(c, encoding='utf-8', ensure_ascii=False)
            temp.write(ojs)
        with open('tmp/have_marked_answer.dict', 'w') as dts:
            pickle.dump(dicts, dts)

        

def main():
    markList('tmp/sourceData')

if __name__ == "__main__":
    main()



