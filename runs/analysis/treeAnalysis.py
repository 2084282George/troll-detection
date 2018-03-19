import csv
import io
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

with open('../POSTest.csv', 'rb') as csvfile:
    results = csv.reader(csvfile, skipinitialspace=True)
    selfMeans = []
    otherMeans = []
    lenDict = {}
    for row in results:
        if row[0] != "NO TWEETS FOUND FOR USER":
            if not lenDict.has_key(row[0]):
                lenDict[row[0]] = int(row[2])
            if not lenDict.has_key(row[1]):
                lenDict[row[1]] = int(row[3])

with open('../TreeTest.csv', 'rb') as csvfile:
    results = csv.reader(csvfile, skipinitialspace=True)
    selfMeans = []
    otherMeans = []
    selfDict = {}
    for row in results:
        if row[0] != "NO TWEETS FOUND FOR USER":
            between = float(row[4]) #/ lenDict[row[0]] + lenDict[row[1]]
            within1 = float(row[3]) #/ lenDict[row[0]]
            within2 = float(row[2]) #/ lenDict[row[1]]
            selfDict[row[0]] = within1
            selfDict[row[1]] = within2
            diff = between - (within1 + within2)/2
            if row[0] == row[1][:-5]+'1.txt':
                selfMeans.append(diff)
            else:
                otherMeans.append(diff)
    

    print selfMeans

with open('../TreeTest2.csv', 'rb') as csvfile:
    results = csv.reader(csvfile, skipinitialspace=True)
    otherMeans = []
    for row in results:
        if row[0] != "NO TWEETS FOUND FOR USER":
            between = 2*float(row[2]) / lenDict[row[0]] + lenDict[row[1]]
            try:
                within1 = selfDict[row[0]] / lenDict[row[0]]
                within2 = selfDict[row[1]] / lenDict[row[1]]
            except KeyError as e:
                pass

            diff = between - (within1 + within2)/2
            if row[0] == row[1][:-5]+'1.txt':
                selfMeans.append(diff)
            else:
                otherMeans.append(diff)


    print len(selfMeans)
    print len(otherMeans)

    otherMean = np.mean(otherMeans)
    print otherMean

    n, bins, patches = plt.hist(otherMeans, 100, normed=True, facecolor='green', alpha=0.75)

    plt.xlabel('Tree Edit Distance')
    plt.ylabel('Accounts (Normalised)')
    plt.title('Mean Tree Edit Distance Between 2 Accounts')
    plt.axis([0, 500, 0, 0.02])
    plt.grid(True)

    plt.show()

    selfMean = np.mean(selfMeans)
    print selfMean

    t_stat, p_val = stats.ranksums(selfMeans, otherMeans)

    print "T:", t_stat
    print "P:", p_val