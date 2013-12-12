# -*- coding: utf-8 -*-
import codecs
import os
import re
import urllib2
import sys
import commands
import subprocess
from lib.chardet.universaldetector import UniversalDetector
from logger import log

class Decompresser:
    def __init__(self, rarDir, decompressDir):
        self.rarDir = rarDir
        self.decompressDir = decompressDir

    def decompress(self,rarPath, outputDir):
        print rarPath
        print outputDir
        print 'unrar x %s %s' % (rarPath,outputDir)
        try:
            subprocess.Popen(['unrar', 'x', rarPath, outputDir])
            #subprocess.call(r' unrar x %s %s' % (rarPath,outputDir))
        except CalledProcessError, e:
            log(Decompress, e)

    def decompressCaption(self,compressDir, rarName):
        outputDir = rarName[0: rarName.find('.rar')]
        outputDir = os.path.join(self.decompressDir,outputDir)
        if not os.path.exists(outputDir):
            os.mkdir(os.path.join(outputDir))
        self.decompress(os.path.join(compressDir, rarName), outputDir) 

    def decompressAllCaption(self):
        for parent, dirnames, files in os.walk(self.rarDir):
            self.decompressCaption(parent, files[0])


class CaptionParser:
    def __init__(self, captionPath, resultFile ):
        self.captionPath = captionPath
        self.resultFile  = resultFile
        self.tmpFile = resultFile + '.tmp'

    def parseCaption(self):
        for parent, dirnames, files in os.walk(self.captionPath):
            for i in range(len(files)):
                if os.path.isfile(os.path.join(parent, files[i])):
                    if files[i].lower().endswith('srt'):
                        print parent, files[i]
                        self.parseSrtCaption(parent, files[i])
                    elif files[i].lower().endswith('ass'):
                        print parent, files[i]
                        self.parseAssCaption(parent, files[i])

    def detectFileEncode(self, filePath):
        detector = UniversalDetector()
        with open(filePath, 'r') as fp:
            for line in fp.readlines():
                detector.feed(line)
                if detector.done: break
            detector.close()
        print detector.result
        return detector.result['encoding']
    
    def isEngSentence(self, sentence):
        for i in range(len(sentence)):
            if ord(sentence[i]) > 127:
                return False
        return True

    def fetchCaptionInfo(self, fileDir, fileName):
        parentDir = re.findall(r'(/\d+____.*?/)',os.path.join(fileDir, fileName))[0]
        captionInfo = parentDir[1 : len(parentDir)-1]
        infos = captionInfo.split('____')
        captionId = infos[0]
        captionName = infos[1]
        captionSeason = infos[2]
        captionSets = infos[3]
        match = re.compile(r'S\d+E\d*').findall(captionName)
        if (len(match)) > 0:
            match = match[0]
            if captionSeason == '0' or captionSeason == '':
                captionSeason = match[match.find('S'):match.find('E')]
            if captionSets == '0' or captionSets == '':
                captionSets = match[match.find('E'): len(match)]
        return (captionId, captionName, captionSeason, captionSets)

    def parseSrtCaption(self, fileDir, fileName):
        captionId, captionName, captionSeason, captionSets = self.fetchCaptionInfo(fileDir, fileName)
        # the result format       
        # (startTime, endTime,  engSentence, chnSentence)
        # detect file coding
        fileEncode = self.detectFileEncode(os.path.join(fileDir, fileName))
        sentenceList = list()
        sentenceItem = list()
        with codecs.open(os.path.join(fileDir, fileName), 'r', fileEncode, 'ignore') as fp:  
            for line in fp.readlines():
                line = line.encode('utf-8').strip()
                if line == '':
                    sentenceList.append(sentenceItem)
                    sentenceItem = list()
                else:
                    sentenceItem.append(line)
        resultList = list()
        for i in range(len(sentenceList)):
            if len(sentenceList[i]) > 2:
                index =sentenceList[i][0]
                startTime, endTime = sentenceList[i][1].split('-->')
                chnList = list()
                engList = list()
                for j in range(2, len(sentenceList[i])):
                    if self.isEngSentence(sentenceList[i][j]):
                        engList.append(sentenceList[i][j])
                    else:
                        chnList.append(sentenceList[i][j])
            resultList.append((captionId, captionName, captionSeason, captionSets, startTime, endTime,  '$$$$'.join(engList), '$$$$'.join(chnList)))
        self.saveSentenceList(resultList)
    
    def parseAssCaption(self, fileDir, fileName):
        captionId, captionName, captionSeason, captionSets = self.fetchCaptionInfo(fileDir, fileName)
        # detect file coding
        fileEncode = self.detectFileEncode(os.path.join(fileDir, fileName))
        sentenceList = list()
        with codecs.open(os.path.join(fileDir, fileName), 'r', fileEncode) as fp :
            for line in fp.readlines():
                line = line.encode('utf-8').strip()
                if line.startswith('Dialogue:'):
                    items = line.split(',',9)
                    if (len(items) == 10):
                        text = re.sub(r'{.*?}','',items[9]) 
                        sentences = text.split('\N')
                        chnList = list()
                        engList = list()
                        for i in range(len(sentences)):
                            if isEngSentence(sentences[i]):
                                engList.append(sentences[i])
                            else:
                                chnList.append(sentences[i])
                    sentenceList.append(captionId, captionName, captionSeason, captionSets, items[1], items[2], '$$$$'.join(engList), '$$$$'.join(chnList))
                else:
                    pass
        self.saveSentenceList(sentenceList)
        
    def saveSentenceList(self, sentenceList):
        with codecs.open(self.tmpFile , 'a') as fp:  
            for i in range(len(sentenceList)):
                line = '@@##'.join(sentenceList[i])
                fp.write(line+'\n')

    def addIndexToSentence(self):
        with open(self.resultFile, 'a') as fp:
            with open(self.tmpFile, 'r') as fr:
                content = fr.readlines()
                for i in range(len(content)):
                    fp.write('%d%s%s' % (i, '@@##', content[i]))

if  __name__ == '__main__':
    decompressAllCaption('./data/caption', './data/decompress')
    #decompressCaption('246858____The_Big_Bang_Theory____S07____E09.rar')
    #parseCaption(r'./data/decompress/', './sentence.txt')

