import nltk
import io
import sys
from bllipparser import RerankingParser
from anytree import Node, RenderTree

rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)

f1 = io.open(sys.argv[1], "r+").read().splitlines()
f2 = io.open(sys.argv[2], "r+").read().splitlines()

trees1 = []
trees2 = []

def treeParse(tString):
    return []


for tweet in f1:
    newTweet = tweet.encode('ascii', 'ignore')
    print newTweet
    if len(newTweet)!=0:
        newTree = rrp.simple_parse(newTweet)
        trees1.append(newTree)

print trees1

for tweet in f2:
    newTweet = tweet.encode('ascii', 'ignore')
    print newTweet
    if len(newTweet)!=0:
        newTree = rrp.simple_parse(newTweet)
        trees2.append(newTree)

print trees2

