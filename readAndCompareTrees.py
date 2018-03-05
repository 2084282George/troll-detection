from anytree import Node, RenderTree
from anytree.importer import DictImporter
import treeTester
from randomdict import RandomDict
import io
import time

importer = DictImporter()

fNaive = io.open("./runs/TreeTest2.csv",'a')

fTrees = io.open("./DictStore.pkl", 'r').read().splitlines()

singleRunResults = RandomDict()

key = "DEFAULT, SHOULD NEVER BE SEEN"

for line in fTrees:
    if line[0] == '.':
        key  = line
        singleRunResults[key] = []
    else:
        tDict = eval(line)
        root = importer.import_(tDict)
        singleRunResults[key].append(root)

done = 0

for x in singleRunResults.keys:
    for y in range(0,10):
        t = time.time()
        z = singleRunResults.random_key()
        while (z == x or z == x[:-5]+'2.txt'):
            z = singleRunResults.random_key()
        comp = treeTester.runDouble(singleRunResults[x], singleRunResults[z])
        t = time.time() - t
        output = x + ", " + z + ", " + str(comp) + ", " + str(t) + "\n"
        print output
        done += 1
        print done
        fNaive.write(unicode(output))