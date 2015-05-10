from sys import argv
from datetime import datetime
import os
import re
import sys
from lazymp.atomic import Atomic

def word_count(dir_path):
   word_count_result = {}
   for lists in os.listdir(dir_path):
      local_word_count = {}
      path = os.path.join(dir_path, lists)
      if os.path.isfile(path):
         file = open(path, "r")
         for line in file.xreadlines():
            for word in line.split():
               if word in local_word_count:
                  local_word_count[word] += 1
               else:
                  local_word_count[word] = 1
         file.close()
      for k, v in local_word_count.items():
         if k not in word_count_result:
            word_count_result[k] = v
         else:
            word_count_result[k] += v
   return word_count_result

def word_count_mp(dir_path):
   word_count_result = {} #pragma shared dict
   for lists in os.listdir(dir_path): #pragma omp parallel for
      local_word_count = {}
      path = os.path.join(dir_path, lists)
      if os.path.isfile(path):
         file = open(path, "r")
         for line in file.xreadlines():
            for word in line.split():
               if word in local_word_count:
                  local_word_count[word] += 1
               else:
                  local_word_count[word] = 1
         file.close()
      with Atomic():
         for k, v in local_word_count.items():
            if k not in word_count_result:
               word_count_result[k] = v
            else:
               word_count_result[k] += v
   return word_count_result

if __name__ == "__main__":
   dir_path = argv[1]

   # original version
   start = datetime.now()
   resultA = word_count(dir_path)
   end = datetime.now()
   slow_time = (end - start).total_seconds()

   # multi-process version
   start = datetime.now()
   resultB = word_count_mp(dir_path)
   end = datetime.now()
   fast_time = (end - start).total_seconds()

   # check if result is correct
   if len(resultA) != len(resultB):
      print "ERROR: results do not match!"
      exit(0)
   for key in resultA:
      if (key not in resultB or resultA[key] != resultB[key]):
         print "ERROR: results do not match!"
         exit(0)

   sys.stderr.write("slow runtime: %s, result count %d\n" % (str(slow_time), len(resultA)))
   sys.stderr.write("fast runtime: %s, result count %d\n" % (str(fast_time), len(resultB)))
   sys.stderr.write("speed up: %f\n" % (slow_time / fast_time))
