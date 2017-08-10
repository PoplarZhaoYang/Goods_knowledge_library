[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]()
---

## Outline

### structure 
 - sample/
    - dataProcess/
        - data_load.py(load chat logs text from MongoDB)
        - data_mark.py(a data mark program)
        - temp/ (temp file)
    - train/
        - train_classification_model.py(train model based on SVM)
        - goods_libaray.py(cluster and show answer)
        - temp/ (temp file)



- Learning Taobao customer service chat logs by text classification, clustering. Independent completion including data cleaning, feature extraction(tfidf), modeling(SVM), model evaluation(CV), adjustment of the whole process of parameters.

- To achieve according to the past customer service chat logs to learn the statements which are about commodity property. And them are presented to the customer service staff in the form of fast reply to enhance the efficiency of customer service staff.




