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

grammar = r"""
  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
  PP: {<IN><NP>}               # Chunk prepositions followed by NP
  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
  CLAUSE: {<NP><VP>}           # Chunk NP, VP
"""
chunker = nltk.RegexpParser(grammar)


def pruneTree(tree):
    newT = ""
    sT = tree.split()
    for item in sT:
        if item[0] == "(":
            newT += item
        else:
            for char in item:
                if char == ")":
                    newT += char
    print newT
    return newT


def makeTrees (f):
    trees = []
    #x = 0
    for tweet in f:
        newTweet = tweet.encode('ascii', 'ignore').replace("@", "")
        if len(newTweet)!=0:
            newTree = rrp.simple_parse(newTweet)
            sTree = parse_sexp(newTree)
            #pprint(sTree)
            dTree = tMake(sTree[0])
            root = importer.import_(dTree)
            trees.append(root)
            #x+=1
            #print "done " + str(x) + " tweets"
    return trees

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

def lcs_length(a, b):
    table = [[0] * (len(b) + 1) for _ in xrange(len(a) + 1)]
    for i, ca in enumerate(a, 1):
        for j, cb in enumerate(b, 1):
            table[i][j] = (
                table[i - 1][j - 1] + 1 if ca == cb else
                max(table[i][j - 1], table[i - 1][j]))
    return table[-1][-1]

def tMake (item):
        d = {}
        #time.sleep(0.1)

        #print "***\nTHIS IS THE ITEM:"
        #pprint(item)
        #print "WITH LENGTH"
        #print len(item)

        if all(type(x)==list for x in item[1:]):

            #print "IT IS A LIST OF LISTS"
            d['label'] = item[0]

            y = item[1:]
            #print "SO WORKING ON:"
            d['children'] = [tMake(x) for x in y]
                
        elif all(type(x)==str for x in item) and  len(item)==2:

            #print "IT HAS 2 STRINGS\n***"
            d['label'] = item[0]
                
            d['b'] = item[1]
        else:
            print "THIS SHOULD NEVER HAPPEN, SOMETHING IS WRONG\n***"
            #print "***\nTHIS IS THE ITEM:"
            #pprint(item)
            #print "WITH LENGTH"
            #print len(item)
        return d
            


def nodeDist(A, B):
    if A==B:
        return 0
    else:
        return 1

trees1 = makeTrees(f1)

#print len(trees1)
#print "\n***\n"
#pprint(trees1)
#print "\n***\n"

distancesWithin = []
#length = []

done = 0

for x in trees1:
    #length.append(len(x))
    for y in trees1:
        distance = zss.simple_distance(x, y, label_dist= nodeDist)
        distancesWithin.append(distance)
        done+=1
        #print "Done %i comparisons", done

mDist1 = np.mean(distancesWithin)
#mL = np.mean(length)
#print "\nThe mean edit distance of Tree for " + sys.argv[1] + " is:\n"
#pprint (mDist1)
#pprint (mL)


trees2 = makeTrees(f2)

#print len(trees1)
#print "\n***\n"
#pprint(trees1)
#print "\n***\n"

distancesWithin = []
#length = []


for x in trees2:
    #length.append(len(x))
    for y in trees2:
        distance = zss.simple_distance(x, y)
        distancesWithin.append(distance)

mDist2 = np.mean(distancesWithin)
#mL = np.mean(length)
#print "\nThe mean edit distance of Tree for " + sys.argv[2] + " is:\n"
#pprint (mDist2)
#pprint (mL)

distancesWithin = []

for x in trees1:
    for y in trees2:
        distancesWithin.append(zss.simple_distance(x, y))
        
        

mDist3 = np.mean(distancesWithin)

stop = time.time()

runTime = stop - start

#print "\nThe mean edit distance of Tree between " + sys.argv[1] +  " and " + sys.argv[2] + " is:\n"
#pprint (mDist3)


#print len(trees2)
#print "\n***\n"
#pprint(trees2)
#print "\n***\n"

print sys.argv[1] + ", " +  sys.argv[2] + ", " + str(len(f1)) + ", " + str(len(f2)), ", " +  str(mDist1) + ", " +  str(mDist2),", ", str(mDist3) + ", "+ str(runTime)