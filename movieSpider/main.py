#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os
import re
import urllib2
import sys
from captionPageParser import fetchOneMovieInfo
from captionCrawler import captionCrawler


splitChars = '@@$$'

def readMovieNames(movieNamesFile):
    nameList = list()
    fp = codecs.open(movieNamesFile, 'r', 'utf-8')
    try:
        for line in fp.readlines():
            line = line.split(splitChars)[0]
            nameList.append(line)
        fp.close()
    except IOError:
        print 'read file error'
    return nameList

def fetchAllCaptionInfo(movieNamesFile, captionInfoFile):
    nameList = readMovieNames(movieNamesFile)
    print nameList
    for i in range(len(nameList)):
        captionInfo = fetchOneMovieInfo(captionInfoFile, nameList[i])

def crawCaption(captionInfoFile, outputDir):
    captionCrawler(captionInfoFile, outputDir)
    
    

def run():
    movieNamesFile = './data/teleplayNames.txt'
    captionInfoFile = './data/movieInfo.txt'
    captionStoreDir = './data/caption/' 
    #fetchAllCaptionInfo(movieNamesFile, captionInfoFile) 
    
    crawCaption(captionInfoFile, captionStoreDir)

if __name__ == '__main__':
    run() 

