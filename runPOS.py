import naiveBagOfWords
import posTester
import glob
import io
import random

allUsers1 = glob.glob('./newSamples/*_1.txt')

allUsers2 = glob.glob('./newSamples/*_2.txt')

fNaive = io.open("./runs/SecondTest.csv",'w')

totalComparisons = len(allUsers1)*100

print "Got",totalComparisons,"comparisons to do"

onePercent = totalComparisons/100

percentDone = 0

done = 0

for x in allUsers1:
    fNaive.write(unicode(posTester.run(x, x[:-5]+'2.txt')))
    fNaive.write(u'\n')
    for y in range(0,100):
        z = random.randint(0, len(allUsers2)-1)
        fNaive.write(unicode(posTester.run(x, allUsers2[z])))
        fNaive.write(u'\n')    
        
        done +=1

        if done%onePercent == 0:
            print str(percentDone+1) + "% done, " + str(done) + " comparisons"
            percentDone += 1