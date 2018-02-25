#!/usr/bin/env python
import io
import sys
import time

def run(file1, file2):
    start = time.time()

    f1 = set(io.open(file1, "r+").read().split())
    f2 = set(io.open(file2, "r+").read().split())

    i=0


    for item in f1:
        if item in f2:
            i+=1

    tTaken = time.time() - start

    return file1 + ", " + file2 + ", " + `len(f1)` + ", " + `len(f2)` + ", " + `i` + ", " + str(tTaken)

if __name__ == "main":
    run(sys.argv[1], sys.argv[2])
