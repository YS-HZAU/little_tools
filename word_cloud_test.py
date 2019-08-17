# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 19:06:59 2019

@author: huang
"""

import jieba
from pyecharts import options as opts
from pyecharts.charts import WordCloud
import re
import time
from string import punctuation

## 定义过滤集
add_punc='，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥…'
all_punc=punctuation+add_punc
test = "|".join(['\\'+x for x in list(all_punc)])
r = re.compile(test)

## 将内容拼接，这里提供了两种方法，join和+，目的是比较那种速度更快
text = ''
t = time.time()
with open(r"C:\Users\huang\Desktop\zetianji.txt",'r',encoding='utf-8') as fin:
    for line in fin:
        line = line.strip()
        line = re.sub(r, '', line)
        text = text+line
print(time.time()-t)

text_list = []
t = time.time()
with open(r"C:\Users\huang\Desktop\zetianji.txt",'r',encoding='utf-8') as fin:
    for line in fin:
        line = line.strip()
        line = re.sub(r, '', line)
        text_list.append(line)
text = ''.join(text_list)
print(time.time()-t)

## 过滤黑名单中的数据，并取topN的数据构建
word = {}
black = set(['的','他','了','在','她','很','都','你'])
for i in jieba.cut(text):
    if i not in word:
        word[i] = 0
    word[i] += 1
for i in black:
    if i in word:
        del(word[i])
top20 = sorted(word.items(),key=lambda x:x[1],reverse=True)[0:50]

# 也可以直接生成
# top20 = jieba.analyse.extract_tags(text, topK=100, withWeight=True,withFlag=True)

## 画图
WordCloud().add("", top20, word_size_range=[20, 100]).set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-基本示例")).render()
# 启动窗口       画图                                        数据标签的记录                                                       保存路径，默认render.html