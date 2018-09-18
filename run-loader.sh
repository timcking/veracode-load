#!/bin/sh
echo "This will load all files in the xml directory, press Enter to continue or Ctrl-C to cancel"
read varname
for i in `ls -1 xml/*.xml`
do
   echo $i
   python VcParse.py $i
done
