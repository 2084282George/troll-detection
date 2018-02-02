import io
import sys

f1 = set(io.open(sys.argv[1], "r+").read().split())
f2 = set(io.open(sys.argv[2], "r+").read().split())

i=0


for item in f1:
    if item in f2:
        i+=1

print sys.argv[1] + "," + sys.argv[2] + "," + `len(f1)` + "," + `len(f2)` + "," + `i`
