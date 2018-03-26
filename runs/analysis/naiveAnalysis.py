import csv
import io
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

with open('../NaiveTest.csv', 'rb') as csvfile:
    results = csv.reader(csvfile, skipinitialspace=True)
    selfRatio = []
    otherRatio = []
    for row in results:
        if int(row[2]) == 0 or int(row[3]) == 0:
            ratio = 0 
        else:
            ratio = (2.0 * int(row[4])) / (int(row[2]) + int(row[3]))
            if row[0] == row[1][:-5]+'1.txt':
                selfRatio.append(ratio)
            else:
                otherRatio.append(ratio)
    
    n, bins, patches = plt.hist(selfRatio, 200,normed=True, facecolor='green', alpha=0.75)

    n2, bins2, patches2 = plt.hist(otherRatio, 200, normed=True,  facecolor='blue', alpha=0.75)
    
    plt.xlabel('Ratio of Words in Each Set to Words in Both')
    plt.ylabel('Number of Accounts (Normalised)')
    plt.title('Histogram for Bag of Words')
    plt.axis([0,1, 0, 8])
    plt.grid(True)

    plt.show()

    selfAbove = []

    otherAbove = []

    for item in selfRatio:
        if item > 0.25:
            selfAbove.append(item)

    for item in otherRatio:
        if item > 0.25:
            otherAbove.append(item)

    print "***SELF ABOVE 0.25***"

    print len(selfRatio)
    print len(selfAbove)

    selfC = 1.0 * len(selfAbove) / len(selfRatio)

    print selfC

    print "***OTHER ABOVE 0.25***"

    print len(otherRatio)
    print len(otherAbove)

    otherC = 1.0 * len(otherAbove) / len(otherRatio)

    print otherC

    print 100 - ((otherC/selfC) *100)


    selfMean = np.mean(selfRatio)
    print selfMean
    otherMean = np.mean(otherRatio)
    print otherMean

    k2, p = stats.normaltest(otherRatio)

    print "p = {:g}".format(p)


    t_stat, p_val = stats.ranksums(selfRatio, otherRatio)

    print "T:", t_stat
    print "P:", p_val