#!/usr/local/python2.7/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs

from indexInverter import Inverter
from captionParser import Decompresser
from captionParser import CaptionParser


def testInvert():
    inverter = Inverter() 
    print inverter.segmentWord(u'今天的天气真好啊，我们一起出去玩一下吧'.encode('utf-8'))

    wordDict = inverter.invertIndex('./data/result.txt')
    inverter.saveWordIndexToFile(wordDict, './data/word.txt')

def testCaptionParser():
    #decompresser = Decompresser('./data/caption', './data/decompress')
    #decompresser.decompressAllCaption()
    captionParser = CaptionParser('./data/decompress','./data/result.txt')
    captionParser.parseCaption()
    captionParser.addIndexToSentence()
    


if __name__ == '__main__':
    testInvert()
    #testCaptionParser()
