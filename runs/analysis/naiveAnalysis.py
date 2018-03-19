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
    
    n, bins, patches = plt.hist(selfRatio, 200, facecolor='green', alpha=0.75)
    
    plt.xlabel('Ratio of Words in Each Set to Words in Both')
    plt.ylabel('Number of Accounts')
    plt.title('Histogram Within a Single Account')
    plt.axis([0,1, 0, 60])
    plt.grid(True)

    plt.show()

    selfMean = np.mean(selfRatio)
    print selfMean
    otherMean = np.mean(otherRatio)
    print otherMean

    k2, p = stats.normaltest(otherRatio)

    print "p = {:g}".format(p)


    t_stat, p_val = stats.ranksums(selfRatio, otherRatio)

    print "T:", t_stat
    print "P:", p_val