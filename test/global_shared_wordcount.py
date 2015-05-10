from sys import argv
from datetime import datetime
import os
import re

class SharedType:
   DICT = 0
   LIST = 1
   ELSE = 2

class SharedWrapper(object):
   def __init__(self, manager= None):
      self.__dict__['_types'] = {}
      self.__dict__['_origin'] = {}
      self.__dict__['_proxy'] = {}
      self.__dict__['_namespace'] = None

      if manager is None:
         from multiprocessing import Manager
         self.__dict__['_manager'] = Manager()
      else:
         self.__dict__['_manager'] = manager


   def register(self, var_name, var):
      if type(var) is dict:
         self.__dict__['_types'][var_name] = SharedType.DICT

         self.__dict__['_proxy'][var_name] = self.__dict__['_manager'].dict()
         for k, v in var.items():
            self.__dict__['_proxy'][var_name][k] = v

      elif type(var) is list:
         self.__dict__['_types'][var_name] = SharedType.LIST

         self.__dict__['_proxy'][var_name] = self.__dict__['_manager'].list()
         for e in self.var:
            self.__dict__['_proxy'][var_name].append(e)
      else:
         self._types[var_name] = SharedType.ELSE
         if self.__dict__['_namespace'] == None:
            self.__dict__['_namespace'] = self.__dict__['_manager'].NameSpace()

         setattr(var_name, self.__dict__['_namespace'], var)

   def __getattr__(self, var_name):
      # if var_name.startswith("_SharedWrapper__"):
      #    return

      shared_type = self.__dict__['_types'].get(var_name)
      if shared_type == None:
         return None
      elif shared_type == SharedType.DICT or shared_type == SharedType.LIST:
         return self.__dict__['_proxy'][var_name]
      elif shared_type == SharedType.ELSE:
         return getattr(var_name, self.__dict__['_namespace'], None)

   def __setattr__(self, var_name, value):
      # if var_name.startswith("_SharedWrapper__"):
      #    super(SharedWrapper, self).__setattr__(var_name, value)
      #    return

      shared_type = self.__dict__['_types'].get(var_name)
      if shared_type == None:
         return None
      elif shared_type == SharedType.DICT or shared_type == SharedType.LIST:
         self.__dict__['_proxy'][var_name] = value
      elif shared_type == SharedType.ELSE:
         setattr(var_name, self.__dict__['_namespace'], value)


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

   from multiprocessing import Manager

   manager = Manager()
   wrapper = manager.dict()
   for k, v in word_count_result.items():
      wrapper[k] = v

   # tmp['_wrapper'] = SharedWrapper()
   # tmp['_wrapper'].register("word_count_result", word_count_result)

   # for lists in os.listdir(dir_path): #pragma omp parallel for
   def core(lists):
      path = os.path.join(dir_path, lists)
      # print path
      # print tmp['_wrapper']
      # print tmp['_wrapper'].__dict__

      if os.path.isfile(path):
         file = open(path, "r")
         for line in file.xreadlines():
            for word in line.split(" "):
               # pass
               if word in wrapper:
                  wrapper[word] += 1
               else:
                  wrapper[word] = 1
         file.close()

   # print os.listdir(dir_path)

   from pathos.multiprocessing import ProcessingPool
   ProcessingPool(num_process).map(core, os.listdir(dir_path))

   for k, v in wrapper:
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
