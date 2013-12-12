#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import urllib2
from BeautifulSoup import *
import simplejson

splitChar = '@@$$'
outputFileName = './data/mtimeName.txt'
type = sys.getfilesystemencoding()  

def getUrl(i):
    urlPrefix = 'http://service.channel.mtime.com/service/search.mcs?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Channel.Pages.SearchService&Ajax_CallBackMethod=SearchMovieByCategory&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2Fmovie%2Fsearch%2Fsection%2F%23pageIndex%3D'
    urlMiddle = '%26nation%3D275&t=20131210104517346&Ajax_CallBackArgument0=&Ajax_CallBackArgument1=0&Ajax_CallBackArgument2=275&Ajax_CallBackArgument3=0&Ajax_CallBackArgument4=0&Ajax_CallBackArgument5=0&Ajax_CallBackArgument6=0&Ajax_CallBackArgument7=0&Ajax_CallBackArgument8=&Ajax_CallBackArgument9=0&Ajax_CallBackArgument10=0&Ajax_CallBackArgument11=0&Ajax_CallBackArgument12=0&Ajax_CallBackArgument13=0&Ajax_CallBackArgument14=1&Ajax_CallBackArgument15=0&Ajax_CallBackArgument16=1&Ajax_CallBackArgument17=4&Ajax_CallBackArgument18='
    urlSuffix = '&Ajax_CallBackArgument19=0'
    return '%s%d%s%d%s' % (urlPrefix, i, urlMiddle, i, urlSuffix)
    

def parseUrl(url,movieList):
    content = urllib2.urlopen(url).read()
    global type
    content = content.decode('UTF-8').encode(type)
    html = content[content.find('{'): content.rfind('}')+1]
    html =  simplejson.loads(html.decode('utf-8'),encoding='utf-8')
    print 'value' in html.keys()
    print html
    print  'listHTML' in html['value'].keys()
    if not 'value' in html.keys():
        return
    if not 'listHTML' in html['value'].keys():
        return
    soup = BeautifulSoup(html['value']['listHTML'])
    movieItems = soup.findAll('div', attrs={'class':'t_r'})
    print len(movieItems)
    for i in range(len(movieItems)):
        names = movieItems[i].find('a', attrs={'target':'_blank'})
        names = names['title'].strip()
        engName = names[names.find('/')+1 : len(names)].strip()
        chnName = names[0: names.find('/')].strip()
        year = movieItems[i].find('span', attrs={'class':'c_666'}).text.strip().strip('()')
        global splitChar
        movieList.append('%s%s%s%s%s' % (engName, splitChar, chnName,splitChar, year))
    

def saveMovieName(movieList):
    global outputFileName
    fp = codecs.open(outputFileName, 'w','utf-8')
    for i in range(len(movieList)):
        fp.write(movieList[i]+u'\n')
    fp.close()
    

def run():
    movieList = list()
    for i in range(1,2):
        url = getUrl(i)
        parseUrl(url, movieList)
    saveMovieName(movieList)

if __name__ == '__main__':
    run()


 
