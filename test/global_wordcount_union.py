from lazymp.helpers import join_dict
from lazymp.helpers import join_shared, join_add_shared
from sys import argv
from datetime import datetime
import os
import re

def word_count(dir_path):
   word_count_result = {}
   for lists in os.listdir(dir_path):
      path = os.path.join(dir_path, lists)
      if os.path.isfile(path):
         file = open(path, "r")
         for line in file.xreadlines():
            for word in line.split(" "):
               if word in word_count_result:
                  word_count_result[word] += 1
               else:
                  word_count_result[word] = 1
         file.close()

   return word_count_result

def word_count_mp(dir_path, num_process):
   word_count_result = {} #pragma shared
   def core(lists):
      __shared__ = {}
      import copy
      __shared__['word_count_result'] = copy.deepcopy(word_count_result)
      path = os.path.join(dir_path, lists)
      if os.path.isfile(path):
         file = open(path, "r")
         for line in file.xreadlines():
            for word in line.split(" "):
               if word in __shared__['word_count_result']:
                  __shared__['word_count_result'][word] += 1
               else:
                  __shared__['word_count_result'][word] = 1
         file.close()
      return __shared__
   from pathos.multiprocessing import ProcessingPool
   __shared__ = ProcessingPool(num_process).map(core, os.listdir(dir_path))
   join_add_shared(__shared__, { 'word_count_result': word_count_result })

   return word_count_result


if __name__ == "__main__":
   dir_path = argv[1]
   num_process = int(argv[2])

   # original version
   start = datetime.now()
   resultA = word_count(dir_path)
   end = datetime.now()
   slow_time = (end - start).total_seconds()

   # multi-process version
   start = datetime.now()
   resultB = word_count_mp(dir_path, num_process)
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

   print "slow runtime: %s, result count %d" % (str(slow_time), len(resultA))
   print "fast runtime: %s, result count %d" % (str(fast_time), len(resultB))
   print "speed up: %f" % (slow_time / fast_time)
