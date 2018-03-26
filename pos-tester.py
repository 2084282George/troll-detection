import nltk
import io
import sys
from bllipparser import RerankingParser
from anytree import Node, RenderTree
from anytree.importer import DictImporter
import time
import zss
import editdistance
from zss import Node
#!/usr/bin/env python
from pprint import pprint
import numpy as np

start = time.time()

rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=False)

importer = DictImporter()



f1 = io.open(sys.argv[1], "r+").read().splitlines()
f2 = io.open(sys.argv[2], "r+").read().splitlines()

#print len(f1)
#print len(f2)

if len(f1) == 0 or len(f2)== 0:
    #print "at least one of the lists has no tweets, so quitting."
    quit()

def makePOS (f):
    trees = []
    for tweet in f:
        newTweet = tweet.encode('ascii', 'ignore').replace("@", "")
        if len(newTweet)!=0:
            newTree2 = nltk.pos_tag(nltk.word_tokenize(newTweet))

            trees.append([x[1] for x in newTree2])
    return trees

def parse_sexp(string):
    """
    >>> parse_sexp("(+ 5 (+ 3 5))")
    [['+', '5', ['+', '3', '5']]]
    
    """
    sexp = [[]]
    word = ''
    in_str = False
    for char in string:
        if char is '(' and not in_str:
            sexp.append([])
        elif char is ')' and not in_str:
            if word:
                sexp[-1].append(word)
                word = ''
            temp = sexp.pop()
            sexp[-1].append(temp)
        elif char in (' ', '\n', '\t') and not in_str:
            if word:
                sexp[-1].append(word)
                word = ''
        elif char is '\"':
            in_str = not in_str
        else:
            word += char
    return sexp[0]

#https://stackoverflow.com/questions/24547641/python-length-of-longest-common-subsequence-of-lists/24547864

def lcs_length(a, b):
    table = [[0] * (len(b) + 1) for _ in xrange(len(a) + 1)]
    for i, ca in enumerate(a, 1):
        for j, cb in enumerate(b, 1):
            table[i][j] = (
                table[i - 1][j - 1] + 1 if ca == cb else
                max(table[i][j - 1], table[i - 1][j]))
    return table[-1][-1]

trees1 = makePOS(f1)

#print len(trees1)
#print "\n***\n"
#pprint(trees1)
#print "\n***\n"

distancesWithin = []
length = []
lcsWithin = []

for x in trees1:
    length.append(len(x))
    for y in trees1:
        distance = editdistance.eval(x, y)
        distancesWithin.append(distance)
        lcs = lcs_length(x, y)
        lcsWithin.append(lcs)
        distancesWithin.append(distance)


mLength1 = np.mean(length)
mDist1 = np.mean(distancesWithin)
lcs1 = np.mean(lcsWithin)

trees2 = makePOS(f2)

#print len(trees1)
#print "\n***\n"
#pprint(trees1)
#print "\n***\n"

distancesWithin = []
length = []
lcsWithin = []

for x in trees2:
    length.append(len(x))
    for y in trees2:
        distance = editdistance.eval(x, y)
        distancesWithin.append(distance)
        lcs = lcs_length(x, y)
        lcsWithin.append(lcs)
        distancesWithin.append(distance)

mLength2 = np.mean(length)
mDist2 = np.mean(distancesWithin)
lcs2 = np.mean(lcsWithin)


trees1 = makePOS(f1)

#print len(trees1)
#print "\n***\n"
#pprint(trees1)
#print "\n***\n"

distancesWithin = []
lcsWithin = []

for x in trees1:
    for y in trees2:
        distance = editdistance.eval(x, y)
        distancesWithin.append(distance)
        lcs = lcs_length(x, y)
        lcsWithin.append(lcs)
        distancesWithin.append(distance)

mDist3 = np.mean(distancesWithin)
lcs3 = np.mean(lcsWithin)

runTime = time.time() - start

#arg1, arg2, len1, len2, dif1, lcs1, mlen1, dif2, lcs2, mlen2, dif3, lcs3, time

print sys.argv[1] + ", " +  sys.argv[2] + ", " + str(len(f1)) + ", " + str(len(f2)) + ", " + str(mDist1) + ", " + str(lcs1) + ", " + str(mLength1) + ", " +str(mDist2) + ", " + str(lcs2) + ", " + str(mLength2) + ", " + str(mDist3) + ", " + str(lcs3) + ", " + str(runTime)