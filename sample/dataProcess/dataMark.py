#!/usr/bin/env python
# -*- coding:'utf-8' -*-


import json

def makeDictList(fileName):
    ret = []
    with open(fileName, 'r') as f:
        while True:
            an = f.readline()
            if not an:
                break
            b = {'answer': an, 'tag': 0}
            ret.append(b)
        return ret

def main():
    dicts = makeDictList("answer")
    temp = open('temp', 'w')
    for c in dicts:
        jt = json.dumps(c, encoding='utf-8', ensure_ascii=False)
        temp.write(jt)
    temp.close()

if __name__ == "__main__":
    main()



