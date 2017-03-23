[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]()
---


##摘要
该项目的训练数据为：聊天语句文本。
该项目的目标为：找出目标类型的聊天语句，以快捷回复。
* 知识语句分类器：一个二分类器，输入聊天语句，输出所有目标聊天语句。
* 知识语句聚类去重：输入由商品知识语句，有很多条，但是聊天快捷语栏目能展示的内容有限，所以需要聚类，每一类选出一个代表来代表该类。

##代码结构

```
- /sample 代码文件夹
  - /dataProcess/ 数据处理文件夹
    - /__init__.py
    - /__data_load.py 从数据库读取文件
    - /__data_mark.py 手动标记数据
    - /tmp/ 临时文件
      - /answer 训练数据
      
  - /train/ 功能模块文件夹 
    - __init__.py
    - commodity_knowledge.py 聚类去重程序
    - train_classification_model.py 二分类程序
    - /tmp/ 临时文件夹
```




