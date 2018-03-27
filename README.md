# troll-detection-twitter-2084282

Instructions For Use:

To collect data from Twitter:

Firstly add your tokens in where it says "ADD TOKENS HERE" in testbed.py.
Then move this file to the folder you wish to store your data in.
It then takes a single command line argument, which should be the username of the account you want the harvesting to begin from.


To test an approach on two single sets:

Run the appropriate file (naiveBagOfWords.py, posTester.py or treeTester.py) with the path to each file as the two arguments.


To test an approach across all data collected:

Run the appropriate file (runNaive.py, runPOS.py or runTree.py) with no arguments.
runTree.py currently crashes after performing the first phase of its operation, but once this happens running 
readAndCompareTrees.py can complete the second phase.
These files all place their results in /runs/ in a CSV file as described


To analyse the results from each experiment:

Run the appropriate file in /runs/analysis.
These files were changed to perform all the various permutations of result-finding, and so they may require more editing to be used in the desired manny
