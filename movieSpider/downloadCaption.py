#! /usr/bin/python 
# -*- coding: utf-8 -*-
import re
import os
import urllib2
import httplib
import sys
import calcfilehash

type = sys.getfilesystemencoding()
urlPrefix = 'http://file0.shooter.cn'

def getDownloadId(url):
    content = urllib2.urlopen(url).read()
    global type
    content = content.decode('UTF-8').encode(type)
    matchName = re.findall(r'<span class="sublist_box_title_l"><a.*?title="(.*?)"',content)
    for i in range(len(matchName)):
        print matchName[i]

def getDownUrl(downId):
    conn = httplib.HTTPConnection("www.shooter.cn")
    conn.request("GET", "/files/file3.php?hash=duei7chy7gj59fjew73hdwh213f&fileid="+downId)
    r = conn.getresponse()
    content = r.read()
    retcontent = ""
    retcontent = calcfilehash.shtg_calcfilehash(content)
    conn.close()
    global urlPrefix
    return urlPrefix+retcontent

def downloadCaption(downloadId,outputFileName,outputDir):
    url = getDownUrl(downloadId)
    content = urllib2.urlopen(url).read()
    outputPath = os.path.join(outputDir, outputFileName+'.rar')
    fp = open(outputPath,'wb')
    fp.write(content)
    fp.close()

if __name__ == '__main__':
    url =  getDownUrl('248053')
    captionDir = './data/caption/'
    downloadCaption('248053', 'test' , captionDir)
