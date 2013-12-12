# -*- coding: utf-8 -*-
import codecs
import os
from lib.pymmseg import mmseg 
from logger import log

splitChars = '@@##'
wordSplitChars = '##'

class Inverter:

    def __init__(self):
        mmseg.dict_load_defaults()

    def segmentWord(self, sentence):
        words = mmseg.Algorithm(sentence.encode('utf-8'))
        return [word.text for word in words]

    def invertIndex(self, wordFile):
        wordIndex = dict()
        with codecs.open(wordFile, 'r', 'utf-8') as fp:  
            for line in fp.readlines():
                content = line.split(splitChars)
                print content
                if (len(content)) == 9:
                    index = content[0]
                    engSentence = content[7].strip()
                    chnSentence = content[8].strip()
                    words = self.segmentWord(engSentence) + self.segmentWord(chnSentence)    
                    for i in range(len(words)):
                        if not words[i] in wordIndex:
                            wordIndex[words[i]] = list()
                        wordIndex[words[i]].append(index)
        return wordIndex

    def saveWordIndexToFile(self, wordIndexDict, outputFile):
        with open(outputFile, 'a') as fp:
            for key in wordIndexDict.keys():
                fp.write('%s:%s\n' % (key, wordSplitChars.join(wordIndexDict[i])))
