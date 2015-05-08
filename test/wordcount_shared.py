from lazymp.helpers import join_dict
from lazymp.helpers import join_shared
from sys import argv
from datetime import datetime
import os
import re

def word_count(dir_path):
   word_count_result = {}
   for lists in os.listdir(dir_path):
      local_word_count = {}
      path = os.path.join(dir_path, lists)
      if os.path.isfile(path):
         file = open(path, "r")
         for line in file.xreadlines():
            for word in line.split(" "):
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

def word_count_mp(dir_path, num_process):
   word_count_result = {} #pragma shared

   from multiprocessing import Manager
   __manager = Manager()
   __lock = __manager.Lock()

   shared_word_count_result = __manager.dict()

   def core(lists):
      local_word_count = {}
      path = os.path.join(dir_path, lists)
      if os.path.isfile(path):
         file = open(path, "r")
         for line in file.xreadlines():
            for word in line.split(" "):
               if word in local_word_count:
                  local_word_count[word] += 1
               else:
                  local_word_count[word] = 1
         file.close()

      for k, v in local_word_count.items():
         with __lock:
            if k not in shared_word_count_result:
               shared_word_count_result[k] = v
            else:
               shared_word_count_result[k] += v

   from pathos.multiprocessing import ProcessingPool
   ProcessingPool(num_process).map(core, os.listdir(dir_path))

   for k, v in shared_word_count_result.items():
      word_count_result[k] = v

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
