#!/usr/bin/env python
# -*- coding:'utf-8' -*-
import codecs
import json

#make the file which has chat log into list 
def makeDictList(fileName):
    ret = []
    with codecs.open(fileName, 'r', encoding = 'utf-8') as f:
        an = f.readlines()
        for a in an:
            b = {u'answer': a, u'tag': 0}
            ret.append(b)
        return ret

#mark the content of the list and save into a file in json format
def markList(fileName):
    dicts = makeDictList("answer")
    with codecs.open(fileName, 'w', encoding = 'utf-8') as temp:
        cnt = 0
        for c in dicts:
            jt = json.dumps(c, encoding='utf-8', ensure_ascii=False)
            print '\n' + jt + " [{0}]".format(cnt)

            ansStr = raw_input("Is it about the knowledge of commodity?")
            if ansStr == "":
                print "please input number!!!!"
                continue
            else:
                ans = int(ansStr)

            c['tag'] = 1 if ans == 1 else 0
            cnt += 1

            ojs = json.dumps(c, encoding='utf-8', ensure_ascii=False)
            temp.write(ojs)


def main():
    markList('sourceData')


if __name__ == "__main__":
    main()


