import nltk
import io
import sys
from bllipparser import RerankingParser
from anytree import Node, RenderTree
import time

rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)

f1 = io.open(sys.argv[1], "r+").read().splitlines()
f2 = io.open(sys.argv[2], "r+").read().splitlines()

def pruneTree(tree):
    newT = ""
    pc = ""
    for c in tree:
        #do thing to strip tree
        newT+= c
 

newTree = rrp.simple_parse("Here's a more simple sentence. This second part might be harder.")



for tweet in f1:
    newTweet = tweet.encode('ascii', 'ignore')
    if len(newTweet)!=0:
        newTree = rrp.simple_parse(newTweet)
        print newTree
        time.sleep(0.1)

print trees1

for tweet in f2:
    newTweet = tweet.encode('ascii', 'ignore')
    if len(newTweet)!=0:
        newTree = rrp.simple_parse(newTweet)
        trees2.append(newTree)

print trees2

