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
            between = float(row[4]) #/ (lenDict[row[0]] + lenDict[row[1]])
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
            between = float(row[2]) #/ (lenDict[row[0]] + lenDict[row[1]])
            try:
                within1 = selfDict[row[0]] #/ lenDict[row[0]]
                within2 = selfDict[row[1]] #/ lenDict[row[1]]
            except KeyError as e:
                print "Oh no"
                pass

            diff = between - (within1 + within2)/2
            if row[0] == row[1][:-5]+'1.txt':
                selfMeans.append(diff)
            else:
                otherMeans.append(diff)


    print len(selfMeans)
    print len(otherMeans)

    selfMean = np.mean(selfMeans)
    print selfMean

    otherMean = np.mean(otherMeans)
    print otherMean

    n, bins, patches = plt.hist(selfMeans, 20, normed=True, facecolor='green', alpha=1)
    n2, bins2, patches2 = plt.hist(otherMeans, 100, normed=True, facecolor='blue', alpha=0.5)

    plt.xlabel('Tree Edit Distance Difference')
    plt.ylabel('Accounts (Normalised)')
    plt.title('Mean Tree Edit Distance Difference')
    plt.axis([0,20, 0, 0.6])
    plt.grid(True)

    plt.show()



    t_stat, p_val = stats.ranksums(selfMeans, otherMeans)

    print "T:", t_stat
    print "P:", p_val

    selfAbove = []

    otherAbove = []

    for item in selfMeans:
        if item < 1:
            selfAbove.append(item)

    for item in otherMeans:
        if item < 1:
            otherAbove.append(item)

    
    print "***SELF ABOVE 0.5"
    
    selfC = 1.0 * len(selfAbove) / len(selfMeans)

    print selfC

    print "***OTHER ABOVE 0.5***"

    otherC = 1.0 * len(otherAbove) / len(otherMeans)

    print otherC

    print 100 - ((otherC/selfC) *100)