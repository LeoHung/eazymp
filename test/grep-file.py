from sys import argv
from datetime import datetime
import os
import re

"""
   Print the lines in file if pattern appears in the string
"""
def grep(pattern, file_path, offset, size):
   file = open(file_path, "r")
   if (offset != 0):
      file.seek(offset)
      # if not the very first line in the file, skip the first input string
      file.readline()
   for line in file.xreadlines():
      #if pattern in line:
      #   print line
      size -= len(line) + 1
      if(size <= 0):
         break
   file.close()

def grep_file(pattern, file_path, size):
   file_size = os.stat(file_path).st_size
   split_number = file_size / size

   for split_no in range(split_number + 1):
      offset = 0
      """
         Use a trick here for avoid overlap between different loops.
         The offset is set to be one char higher. So the first line in grep()
         would not need to be read. grep() start to read from the second line,
         which will not overlap with the last line in previous loop.
      """
      if (split_no != 0):
         offset = split_no * size - 1
      grep(pattern, file_path, offset, size)

def grep_file_mp(pattern, file_path, size):
   file_size = os.stat(file_path).st_size
   split_number = file_size / size

   for split_no in range(split_number + 1):  #pragma omp parallel for
      offset = 0
      if (split_no != 0):
         offset = split_no * size - 1
      grep(pattern, file_path, offset, size)

if __name__ == "__main__":
   filename = argv[1]
   pattern = argv[2]
   if(len(argv) < 4):
      size = 4096
   else:
      size = int(argv[3])

   # original version
   start = datetime.now()
   grep_file(pattern, filename, size)
   end = datetime.now()
   slow_time = (end - start).total_seconds()

   # multi-process version
   start = datetime.now()
   grep_file_mp(pattern, filename, size)
   end = datetime.now()
   fast_time = (end - start).total_seconds()

   print "slow runtime: %s" % str(slow_time)
   print "fast runtime: %s" % str(fast_time)
   print "speed up: %f" % (slow_time / fast_time)
