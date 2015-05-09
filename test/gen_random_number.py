from random import randint
import sys

l = int(sys.argv[1])
for _ in xrange(l):
    print randint(-10000000, 10000000)
