#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, os.path
import zipfile
import codecs
import re
import urllib2
import sys


def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir):
         os.mkdir(unziptodir, 0777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\','/')
        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:   
            ext_filename = os.path.join(unziptodir, name)
            ext_dir= os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir) :
                 os.mkdir(ext_dir,0777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()





if __name__ == '__main__':
    unzip_file('./data/caption/238574@@$$Cloud Atlas 2012.rar','./data/caption')
