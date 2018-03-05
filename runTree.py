import treeTester
import glob
import io
import random
from bllipparser import RerankingParser
from randomdict import RandomDict
import time
import cPickle as pickle

rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=False)

allUsers1 = glob.glob('./newSamples/*_1.txt')[:100]

allUsers2 = glob.glob('./newSamples/*_2.txt')

fNaive = io.open("./runs/TreeTest.csv",'w')

totalComparisons = len(allUsers1)*10

print "Got",totalComparisons,"comparisons to do"

onePercent = totalComparisons/100

percentDone = 0

done = 0

singleRunResults = RandomDict()

firstPhaseTime = time.time()

for x in allUsers1:
    t = time.time()
    newTrees = treeTester.runSingle(x, rrp)
    if newTrees != "NO TWEETS, EXITING":
        singleRunResults[x] = newTrees
        oHalf = x[:-5]+'2.txt'
        newTrees = treeTester.runSingle(oHalf, rrp)
        if newTrees != "NO TWEETS, EXITING":
            singleRunResults[oHalf] = newTrees
            selfCheck = treeTester.runDouble(singleRunResults[x][2], singleRunResults[oHalf][2])
            t = time.time() - t
            output = x + ", " + oHalf + ", " + str(singleRunResults[x][0]) + ", " + str(singleRunResults[oHalf][0]) + ", " + str(selfCheck) + ", " + str(t) + "\n"
            print output
            done += 1
            print done
            fNaive.write(unicode(output))

firstPhaseTime = time.time() - firstPhaseTime

print "********"
print "FIRST PHASE COMPLETE IN" + str(firstPhaseTime) + ", THERE ARE NO MORE TREES TO BUILD"
print "********"




for x in allUsers1:
    doneComp = [x, x[:-5]+'2.txt']
    for y in range(0,10):
        t = time.time()
        z = x
        while not z in doneComp:
            z = singleRunResults.random_key()
        doneComp.append(z)
        comp = treeTester.runDouble(singleRunResults[x][2], singleRunResults[z][2])
        t = time.time() - t
        output = x + ", " + z + ", " + str(singleRunResults[x][0]) + ", " + str(singleRunResults[z][0]) + ", " + str(selfCheck) + ", " + str(t) + "\n"
        print output
        done += 1
        print done
        fNaive.write(unicode(output))




"""for x in allUsers1:
    fNaive.write(unicode(treeTester.run(x, x[:-5]+'2.txt', rrp)))
    fNaive.write(u'\n')
    for y in range(0,10):
        z = random.randint(0, len(allUsers2)-1)
        fNaive.write(unicode(treeTester.run(x, allUsers2[z], rrp)))
        fNaive.write(u'\n')   
        done +=1

        if done%onePercent == 0:
            print str(percentDone+1) + "% done, " + str(done) + " comparisons"
            percentDone += 1
        
        elif done%5 == 0:
            print str(done) + " comparisons done"
"""