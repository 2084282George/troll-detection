import nltk
import io
import sys
from bllipparser import RerankingParser
from anytree import Node, RenderTree
import time
import zss
import editdistance
from zss import Node
from pprint import pprint
import numpy as np

rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)



f1 = io.open(sys.argv[1], "r+").read().splitlines()
#f1 = ["Here's a test sentence for Erin to show her what I'm working with."]
f2 = io.open(sys.argv[2], "r+").read().splitlines()

print len(f1)
print len(f2)

grammar = r"""
  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
  PP: {<IN><NP>}               # Chunk prepositions followed by NP
  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
  CLAUSE: {<NP><VP>}           # Chunk NP, VP
"""
chunker = nltk.RegexpParser(grammar)



class WeirdNode(object):

    def __init__(self, label):
        self.my_label = label
        self.my_children = list()

    @staticmethod
    def get_children(node):
        return node.my_children

    @staticmethod
    def get_label(node):
        return node.my_label

    def addkid(self, node, before=False):
        if before:  self.my_children.insert(0, node)
        else:   self.my_children.append(node)
        return self

def findChildren (lNodes, parent):
    if isinstance(lNodes, list):
        label = lNodes[0]

        children = lNodes[1:]
        if not(isinstance(children, str)):
            for child in children:
                child = findChildren(child, WeirdNode(lNodes))
        else:
            parent.addkid(children)
        parent.addkid(WeirdNode(label))
        printNTree(parent)
    return parent

def printNTree (parent):
    print "This is the label: " + str(WeirdNode.get_label(parent)) + "\n\n"
    x = WeirdNode.get_children(parent)
    print "These are the children: " + str(x) + "\n\n"
    for item in x:
        printNTree( item )



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
    for tweet in f:
        newTweet = tweet.encode('ascii', 'ignore').replace("@", "")
        if len(newTweet)!=0:
            newTree = rrp.simple_parse(newTweet)
            #pTree = pruneTree(newTree)
            sTree = parse_sexp(newTree)
            pprint(sTree)
            A = WeirdNode("root")
            A = findChildren(sTree[0], A)
            printNTree(A)
            trees.append(A)
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



trees1 = makePOS(f1)

#print len(trees1)
#print "\n***\n"
#pprint(trees1)
#print "\n***\n"

distancesWithin = []
length = []
lcs = []

for x in trees1:
    length.append(len(x))
    for y in trees1:
        distancesWithin.append(editdistance.eval(x, y))
        lcs.append(lcs_length(x, y))

mDist1 = np.mean(distancesWithin)
mL = np.mean(length)
mLcs = np.mean(lcs)
print "\nThe mean edit distance of PoS for " + sys.argv[1] + " is:\n"
pprint (mDist1)
pprint (mL)
pprint (mLcs)

trees2 = makePOS(f2)

distancesWithin = []
length = []

for x in trees2:
    length.append(len(x))
    for y in trees2:
        distancesWithin.append(editdistance.eval(x, y))

mDist2 = np.mean(distancesWithin)
mL = np.mean(length)

print "\nThe mean edit distance of PoS for " + sys.argv[2] + " is:\n"
pprint (mDist2)
pprint (mL)

distancesWithin = []

for x in trees1:
    for y in trees2:
        distancesWithin.append(editdistance.eval(x, y))

mDist3 = np.mean(distancesWithin)

print "\nThe mean edit distance of PoS between " + sys.argv[1] +  " and " + sys.argv[2] + " is:\n"
pprint (mDist3)

#print len(trees2)
#print "\n***\n"
#pprint(trees2)
#print "\n***\n"


