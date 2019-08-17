# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:38:39 2018

@author: xyhuang
"""

from urllib import request
from bs4 import BeautifulSoup
import time

def chapter(url,fout):
    content = ''
    req = request.Request(url)
    response = request.urlopen(req)
    html = response.read()
    
    soup = BeautifulSoup(html,'lxml')
    soup_text = soup.find('div',id = 'main_body')
    content = content+soup_text.h1.string+"\n"
    zhengwen = soup_text.find('div',id = 'content')
    for i in zhengwen('p'):
        content = content+i.text+"\n"
    fout.write(content)

def geturl(url,fout):
    req = request.Request(url)
    response = request.urlopen(req)
    html = response.read()
    
    soup = BeautifulSoup(html,'lxml')
    for i in soup.find_all('div',id = 'book_detail'):
        if i.h3:
            continue
        for j in i('li'):
            chapter(j.a.get('href'),fout)
            time.sleep(0.2)
    

if __name__ == '__main__':
    url = r'http://www.136book.com/zetianji/'
    fout = open("zetianji.txt",'w',encoding='utf-8')
    geturl(url,fout)
    fout.close()