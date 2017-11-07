#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:05:53 2017

@author: blue
"""

import urllib
import re
from bs4 import BeautifulSoup
import csv

def getLinks(html, maxlinks=40):
    url = []
    cursor = 0
    nlinks = 0
    while(cursor>=0 and maxlinks>nlinks):
        start_link = html.find('a href', cursor)
        if start_link == -1:
            return url
        start_quote = html.find('"',start_link)
        end_quote = html.find('"',start_quote+1)
        url.append(html[start_quote+1:end_quote])
        cursor = end_quote+1
        nlinks=nlinks+1
    return url

url = "http://barcelonaapi.marcpous.com/"
raw = urllib.request.urlopen(url).read()
linkis = getLinks(str(raw))

flinks = []
for l in linkis:
    if bool(re.match(r'.*stations$',l)):
        flinks.append(l)

#for i in range(flinks):
for i in range(len(flinks)):
    name = flinks[i].split('/')[1]
    with open(name + '.csv', 'w', newline = '\n', encoding = 'UTF-8') as csvfile:
        out =csv.writer(csvfile, delimiter = ',')
        text = urllib.request.urlopen(url +flinks[i]).read()
        soup = BeautifulSoup(text)
        l = []
        counter = 0
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            lk = []
            for i in range(len(tds)):
                lk.append(tds[i].text) 
            l.append(lk)
        out.writerows(l)


        