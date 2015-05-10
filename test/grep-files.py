from sys import argv
from datetime import datetime
import os
import re
import sys

"""
   Print the lines in file if pattern appears in the string
"""
def grep(pattern, file_path):
   file = open(file_path, "r")
   for line in file.xreadlines():
      if pattern in line:
         print line
   file.close()

def traverse_dir(pattern, dir_path):
   for lists in os.listdir(dir_path): 
      path = os.path.join(dir_path, lists) 
      if os.path.isdir(path): 
         traverse_dir(pattern, path)
      elif os.path.isfile(path):
         grep(pattern, path)

def traverse_dir_mp(pattern, dir_path):
   for lists in os.listdir(dir_path): #pragma omp parallel for
      path = os.path.join(dir_path, lists) 
      if os.path.isdir(path): 
         traverse_dir_mp(pattern, path)
      elif os.path.isfile(path):
         grep(pattern, path)

if __name__ == "__main__":
   dir_path = argv[1]
   pattern = argv[2]

   # original version
   start = datetime.now()
   traverse_dir(pattern, dir_path)
   end = datetime.now()
   slow_time = (end - start).total_seconds()

   # multi-process version
   start = datetime.now()
   traverse_dir_mp(pattern, dir_path)
   end = datetime.now()
   fast_time = (end - start).total_seconds()

   sys.stderr.write("slow runtime: %s\n" % str(slow_time))
   sys.stderr.write("fast runtime: %s\n" % str(fast_time))
   sys.stderr.write("speed up: %f\n" % (slow_time / fast_time))
