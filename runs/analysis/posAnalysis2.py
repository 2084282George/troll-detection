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
            between = 2 * float(row[10]) / (int(row[2]) + int(row[3]))
            within1 = float(row[4]) #/ int(row[2])
            within2 = float(row[7]) #/ int(row[3])

            if row[0] == row[1][:-5]+'1.txt':
                selfMeans.append(between)
            else:
                otherMeans.append(between)
            #selfMeans.append(within1)
            #selfMeans.append(within2)

    selfMean = np.mean(selfMeans)
    print selfMean
    otherMean = np.mean(otherMeans[:100000])
    print otherMean

    t_stat, p_val = stats.ranksums(selfMeans, otherMeans)

    print "T:", t_stat
    print "P:", p_val


    n, bins, patches = plt.hist(selfMeans, 100, normed=True, facecolor='green', alpha=1)

    n2, bins2, patches2 = plt.hist(otherMeans[:100000], 100, normed=True,  facecolor='blue', alpha=0.75)


    plt.xlabel('Mean ED / Mean Length')
    plt.ylabel('(Normalised) Number of Comparisons')
    plt.title('Combined Histogram for PoS ED - Length Adjusted')
    plt.axis([0, 8, 0, 3])
    plt.grid(True)

    plt.show()