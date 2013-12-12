#!/bin/sh

dirName='./data/caption'
for file in `ls $dirName ` 
do
    `unrar x $dirName'/'$file`
done
#for file_a in ${FOLDER_A}/*; do
