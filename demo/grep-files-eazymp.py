from sys import argv
from datetime import datetime
import os
import re
import sys

"""
   Print the lines in file if word appears in the string
"""
def grep(word, file_path):
   file = open(file_path, "r")
   for line in file.xreadlines():
      if word in line:
         print line
   file.close()

def traverse_dir_mp(word, dir_path):
   for lists in os.listdir(dir_path): #pragma omp parallel for
      path = os.path.join(dir_path, lists) 
      if os.path.isdir(path): 
         traverse_dir_mp(word, path)
      elif os.path.isfile(path):
         grep(word, path)

if __name__ == "__main__":
   dir_path = argv[1]
   word = argv[2]

   # multi-process version
   start = datetime.now()
   traverse_dir_mp(word, dir_path)
   end = datetime.now()
   fast_time = (end - start).total_seconds()

   sys.stderr.write("runtime: %s\n" % str(fast_time))
