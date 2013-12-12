#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os
import re
import urllib2
import sys
from downloadCaption import downloadCaption

splitChars = '@@##'

def formatMovieName(movieName):
    return movieName.replace(' ','_')

def readMovieInfo(movieNamesFile):
    infoList = list()
    fp = codecs.open(movieNamesFile, 'r', 'utf-8')
    try:
        for line in fp.readlines():
            infoList.append(line)
        fp.close()
    except IOError:
        print 'read file error'
    return infoList

def captionCrawler(captionInfoFile, outputDir):
    captionInfoList = readMovieInfo(captionInfoFile)
    
    for i in range(len(captionInfoList)):
        global splitChars
        print captionInfoList[i]
        infos = captionInfoList[i].split(splitChars)
        print infos
        downloadId = infos[0].strip()
        movieName = formatMovieName(infos[1].strip())
        season = infos[3].strip()
        sets = infos[4].strip()
        captionFileName = '%s____%s____%s____%s' %(downloadId, movieName, season, sets)
        print captionFileName
        downloadCaption(downloadId, captionFileName, outputDir)

def run():
    movieInfoFile = './data/movieInfo.txt'
    outputDir = './data/caption'
    captionCrawler(movieInfoFile, outputDir)    

if __name__ == '__main__':
    run()

