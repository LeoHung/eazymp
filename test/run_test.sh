#!/bin/bash

echo "grep-file test" > grep-file.log
echo "grep-files test" > grep-files.log
echo "wordcount test" > wordcount.log

for i in {2..32}
do
   echo "Output when i = $i" >> grep-file.log
   lazymp -p$i grep-file.py /tmp/jiajun/bigfile.txt test 409600 1>/dev/null 2>>grep-file.log

   echo "Output when i = $i" >> grep-files.log
   lazymp -p$i grep-files.py /tmp/jiajun/split/ test >/dev/null 2>>grep-files.log

   echo "Output when i = $i" >> wordcount.log
   lazymp -p$i wordcount.py /tmp/jiajun/split/ >/dev/null 2>>wordcount.log
done
