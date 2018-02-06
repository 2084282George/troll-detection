import nltk
import io
import sys
from bllipparser import RerankingParser
from anytree import Node, RenderTree
import time

rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)

f1 = io.open(sys.argv[1], "r+").read().splitlines()
f2 = io.open(sys.argv[2], "r+").read().splitlines()

print len(f1)
print len(f2)

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
    return newT
 
def makeTrees (f):
    trees = []
    for tweet in f:
        newTweet = tweet.encode('ascii', 'ignore').replace("@", "")
        if len(newTweet)!=0:
            newTree = rrp.simple_parse(newTweet)
            pTree = pruneTree(newTree)
            trees.append(pTree)
    return trees



trees1 = makeTrees(f1)
trees2 = makeTrees(f2)

print len(trees1)
print len(trees2)
