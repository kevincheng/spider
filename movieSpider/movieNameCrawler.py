#!/usr/bin/python

import sys
import os
import re
import urllib2


outputFileName='nameAll.txt'
type = sys.getfilesystemencoding()  

def getUrl(i):
    urlPrefix = "http://movie.douban.com/tag/%E7%BE%8E%E5%9B%BD%E7%94%B5%E5%BD%B1?"
    urlSuffix = "start=%d&type=T"% i
    return urlPrefix+urlSuffix

def parseUrl(url,movieList):
    page = urllib2.urlopen(url)
    content = page.read()
    global type
    content = content.decode("UTF-8").encode(type)  
    match =  re.findall(r' <a class="nbg".*?title=(.*?)>', content)  
    for i in range(0, len(match)):
        movieList.append(match[i])

def saveMovieName(movieList):
    global outputFileName
    fp = open(outputFileName, 'w')
    for i in range(len(movieList)):
        fp.write(movieList[i]+'\n')
    fp.close()
    

def run():
    movieList = list()
    for i in range(303):
        url = getUrl(i)
        parseUrl(url, movieList)
        saveMovieName(movieList)

if __name__ == '__main__':
    run()


 
