import csv
import io
import numpy as np


def openAndReadTime(file1, timeLoc):
    times = []
    with open(file1, 'rb') as csvfile:
        results = csv.reader(csvfile, skipinitialspace=True)
        for row in results:
            if row[0] != "NO TWEETS FOUND FOR USER":
                times.append(float(row[timeLoc]))
    return times

naive = openAndReadTime('../NaiveTest.csv', 5)

meanN = np.mean(naive)

print "NAIVE MEAN TIME:", meanN

pos = openAndReadTime('../POSTest.csv', -1)

meanP = np.mean(pos)

print "POS MEAN TIME:", meanP

tree1 = openAndReadTime('../TreeTest.csv', 5)

meanT1 = np.mean(tree1)

print "TREE1 MEAN TIME:", meanT1

tree2 = openAndReadTime('../TreeTest2.csv', 3)

meanT2 = np.mean(tree2)

print "TREE2 MEAN TIME:", meanT2
