import csv
import io
import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

with open('../POSTest.csv', 'rb') as csvfile:
    results = csv.reader(csvfile, skipinitialspace=True)
    selfMeans = []
    otherMeans = []
    for row in results:
        if row[0] != "NO TWEETS FOUND FOR USER":
            between = float(row[11]) #/ int(row[2]) + int(row[3])
            within1 = float(row[5]) #/ int(row[2])
            within2 = float(row[8]) #/ int(row[3])

            diff1 = between - within1
            diff2 = between - within2
            diff  = abs(0.5 * (diff1 + diff2))

            if row[0] == row[1][:-5]+'1.txt':
                selfMeans.append(between)
            else:
                otherMeans.append(between)

    selfMean = np.mean(selfMeans)
    print selfMean
    otherMean = np.mean(otherMeans[:100000])
    print otherMean

    t_stat, p_val = stats.ranksums(selfMeans, otherMeans)

    print "T:", t_stat
    print "P:", p_val


    n, bins, patches = plt.hist(selfMeans, 100, normed=True, facecolor='green', alpha=1)

    n2, bins2, patches2 = plt.hist(otherMeans[:100000], 300, normed=True,  facecolor='blue', alpha=0.5)

    
    selfAbove = []

    otherAbove = []

    for item in selfMeans:
        if item > 6:
            selfAbove.append(item)

    for item in otherMeans[:100000]:
        if item > 6:
            otherAbove.append(item)

    
    print "***SELF ABOVE 0.5"
    
    selfC = 1.0 * len(selfAbove) / len(selfMeans)

    print selfC

    print "***OTHER ABOVE 0.5***"

    otherC = 1.0 * len(otherAbove) / len(otherMeans)

    print otherC

    print 100 - ((otherC/selfC) *100)


    plt.xlabel('Mean LCS Difference')
    plt.ylabel('(Normalised) Number of Comparisons')
    plt.title('Combined Histogram for PoS LCS')
    plt.axis([0, 15, 0, 0.5])
    plt.grid(True)

    plt.show()