#!/bin/sh
for i in `ls -1 xml/*.xml`
do
   echo $i
   python VcParse.py $i
done
