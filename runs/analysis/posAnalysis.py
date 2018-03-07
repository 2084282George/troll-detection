import csv
import io
import numpy as np
import scipy.stats as stats

with open('../POSTest.csv', 'rb') as csvfile:
    results = csv.reader(csvfile, skipinitialspace=True)
    selfMeans = []
    otherMeans = []
    for row in results:
        if row[0] != "NO TWEETS FOUND FOR USER":
            between = float(row[11]) #/ int(row[2]) + int(row[3])
            within1 = float(row[5]) #/ int(row[2])
            within2 = float(row[8]) #/ int(row[3])
            diff = between - (within1 + within2)/2
            if row[0] == row[1][:-5]+'1.txt':
                selfMeans.append(diff)
            else:
                otherMeans.append(diff)

    selfMean = np.mean(selfMeans)
    print selfMean
    otherMean = np.mean(otherMeans[:100000])
    print otherMean

    t_stat, p_val = stats.ranksums(selfMeans, otherMeans)

    print "T:", t_stat
    print "P:", p_val