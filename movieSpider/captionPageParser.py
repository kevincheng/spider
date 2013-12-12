#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import re
import urllib2
import sys
from BeautifulSoup import *

splitChars = '@@##'
type = sys.getfilesystemencoding()
urlPrefix = 'http://www.shooter.cn/search2/'

def getSeason(movieName):
    # match english season
    season = None
    sets = None
    match = re.compile(r'S\d+E\d*').findall(movieName)
    if len(match) > 0:
        result = match[0]
        season = result[result.find('S') :  result.find('E')]
        sets = result[result.find('E') : len(result)]
        return (season, sets)
    else:
        return ('0', '0')
        

def fetchDownloadId(idStr):
    index = idStr.find(',')
    return idStr[index+1 : len(idStr)-2]

def parseMovieInfo(captionInfoFile, engName, chnName):
    global urlPrefix
    url = urlPrefix.encode('utf-8')+engName.encode('utf-8')
    content = urllib2.urlopen(url).read()
    global type
    content = content.decode('UTF-8').encode(type)
    soup = BeautifulSoup(content)
    captionList = list()
    movieItems = soup.findAll('div', attrs={'class':'subitem'})
    idList = list()
    for i in range(len(movieItems)):
        movieTag = list()
        movieInfo = dict()
        movieId = movieItems[i].find('a', attrs={'id':'downsubbtn'})
        movieInfo['id'] = fetchDownloadId(movieId['onclick'].strip())
        if not movieInfo['id'] in idList:
            idList.append(movieInfo['id'])
            movieName = movieItems[i].find('a', attrs={'class':'introtitle'})
            movieInfo['name'] = movieName.text.strip()
            movieAttr = movieItems[i].findAll('li')
            for j in range(len(movieAttr)):
                attr = movieAttr[j].text.strip()
                #attrList = attr.split(u'\uff1a')  
                attrList = attr.split(u'：')  
                movieInfo[attrList[0].strip()] = attrList[1].strip()
            movieTag.append(movieInfo['id'])
            movieTag.append(engName)
            season = getSeason(movieInfo['name'])
            movieTag.append(chnName)
            movieTag.append(season[0])
            movieTag.append(season[1])
            #movieTag.append(movieInfo.get(u'\u8bed\u8a00', ''))
            #movieTag.append(movieInfo.get(u'\u65e5\u671f', ''))
            #movieTag.append(movieInfo.get(u'\u6765\u6e90', ''))
            movieTag.append(movieInfo.get(u'语言', '0'))
            movieTag.append(movieInfo.get(u'格式', '0'))
            movieTag.append(movieInfo.get(u'日期', '0'))
            movieTag.append(movieInfo.get(u'来源', '0'))
            movieTag.append(movieInfo.get(u'下载次数', '0'))

            # 获取score和评价人数
            scoreItem = movieAttr[len(movieAttr)-1]
            score = scoreItem.img['src']
            score = score[score.rfind('/')+1 : score.find('.gif')].strip()
            evalNum = scoreItem.em.text.strip().strip('()')
            
            movieTag.append(score)
            movieTag.append(evalNum)
            global splitChars
            captionList.append(splitChars.join(movieTag))
    saveMovieInfo(captionList,captionInfoFile)
    return captionList


def fetchOneMovieInfo(captionInfoFile, engName, chnName='0'):
    return parseMovieInfo(captionInfoFile, engName, chnName)

def saveMovieInfo(movieList, captionInfoFile):
     fp = codecs.open(captionInfoFile, 'a','utf-8')
     for i in range(len(movieList)):
         fp.write(movieList[i])
         fp.write(u'\n')
     fp.close()
     print len(movieList)


if __name__ == '__main__':
    parseMovieInfo('./data/movieList.txt', u'云图')

