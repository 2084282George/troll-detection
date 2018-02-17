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

rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)

importer = DictImporter()



f1 = io.open(sys.argv[1], "r+").read().splitlines()
f2 = io.open(sys.argv[2], "r+").read().splitlines()

print len(f1)
print len(f2)

if len(f1) == 0 or len(f2)== 0:
    print "at least one of the lists has no tweets, so quitting."
    quit()

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
            sTree = parse_sexp(newTree)
            pprint(sTree)
            d = {}
            dTree = tMake(sTree[0])
            root = importer.import_(dTree)
            print(RenderTree(root))
            trees.append(root)
            d = {}
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



def treeMake(listOfLists, d):
    if len(listOfLists) is 1:
        print "***\nThis only has one element:"
        pprint(listOfLists)
        return treeMake(listOfLists[0], d)
    else:
        print "***\nWorking On:"
        pprint(listOfLists)
        for item in listOfLists:
            d['a'] = item[0]
            if isinstance(item[1], list):
                d['children'] = treeMake(item[1], {}) 
            else:
                d['b'] = item[1]
        return d

def tMake (item):
        d = {}
        #time.sleep(0.1)

        #print "***\nTHIS IS THE ITEM:"
        #pprint(item)
        #print "WITH LENGTH"
        #print len(item)

        if all(type(x)==list for x in item[1:]):

            #print "IT IS A LIST OF LISTS"
            d['a'] = item[0]

            y = item[1:]
            #print "SO WORKING ON:"
            pprint(y)
            d['children'] = [tMake(x) for x in y]
                
        elif all(type(x)==str for x in item) and  len(item)==2:

            #print "IT HAS 2 STRINGS\n***"
            d['a'] = item[0]
                
            d['b'] = item[1]
        else:
            print "THIS SHOULD NEVER HAPPEN, SOMETHING IS WRONG\n***"
            print "***\nTHIS IS THE ITEM:"
            pprint(item)
            print "WITH LENGTH"
            print len(item)
            exit()
        return d
            

































trees1 = makeTrees(f1)

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
lcs = []

for x in trees2:
    length.append(len(x))
    for y in trees2:
        distancesWithin.append(editdistance.eval(x, y))
        lcs.append(lcs_length(x, y))

mDist2 = np.mean(distancesWithin)
mL = np.mean(length)
mLcs = np.mean(lcs)
print "\nThe mean edit distance of PoS for " + sys.argv[2] + " is:\n"
pprint (mDist2)
pprint (mL)
pprint (mLcs)

distancesWithin = []
lcs = []

for x in trees1:
    for y in trees2:
        distancesWithin.append(editdistance.eval(x, y))
        lcs.append(lcs_length(x, y))
        

mDist3 = np.mean(distancesWithin)
mLcs = np.mean(lcs)
print "\nThe mean edit distance of PoS between " + sys.argv[1] +  " and " + sys.argv[2] + " is:\n"
pprint (mDist3)
pprint (mLcs)

#print len(trees2)
#print "\n***\n"
#pprint(trees2)
#print "\n***\n"


