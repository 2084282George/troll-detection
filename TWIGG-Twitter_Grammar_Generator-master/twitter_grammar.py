import tweet_dumper
import nltk
import csv
import sys

from nltk.corpus import stopwords
s=set(stopwords.words('english'))

class Grammar: 
    def __init__(self, tweetList, nounList, verbList, adjList, advList, prepList):
        
        newNouns = []
        for word in nounList:
            if len(word) > 2 and not word in s: newNouns.append(word)

        newVerbs = []
        for word in verbList:
            if len(word) > 2 and not word in s: newVerbs.append(word)

        newAdj = []
        for word in adjList:
            if len(word) > 2 and not word in s: newAdj.append(word)
        
        newAdv = []
        for word in advList:
            if len(word) > 2 and not word in s: newAdv.append(word)

        newPre = []
        for word in prepList:
            if len(word) > 2 and not word in s: newPre.append(word)

        #self.Tweet = tweetList
        #self.Noun = newNouns
        #self.Verb = newVerbs
        #self.Adj = newAdj
        #self.Adv = newAdv
        #self.Preposition = newPre

        self.Tweet = tweetList
        self.Noun = nounList
        self.Verb = verbList
        self.Adj = adjList
        self.Adv = advList
        self.Preposition = prepList
    
    def nouns(self):
        return self.Noun

    def verbs(self):
        return self.Verb

    def adjectives(self):
        return self.Adj

    def adverbs(self):
        return self.Adv

    def prepositions(self):
        return self.Preposition

    def tweets(self):
        return self.Tweet

    def mostUsed(self):
        words = ""
        for tweet in self.Tweet:
            words = words + tweet
        
        nounCount = ('',0)
        for noun in self.Noun:
            if words.count(noun) > nounCount[1]:
                nounCount = (noun, words.count(noun))

        verbCount = ('',0)
        for verb in self.Verb:
            if words.count(verb) > verbCount[1]:
                verbCount = (verb, words.count(verb))

        adjCount = ('',0)
        for adj in self.Adj:
            if words.count(adj) > adjCount[1]:
                adjCount = (adj, words.count(adj))

        advCount = ('',0)
        for adv in self.Adv:
            if words.count(adv) > advCount[1]:
                advCount = (adv, words.count(adv))

        prepCount = ('',0)
        for prep in self.Preposition:
            if words.count(prep) > prepCount[1]:
                prepCount = (prep, words.count(prep))

        result = [nounCount, verbCount, adjCount, advCount, prepCount]
        return result

    def __repr__(self):
        print "=======================GRAMMAR======================="
        print "\n nouns: \n"
        print self.Noun
        print "\n verbs: \n"
        print self.Verb
        print "\n adjectives: \n"
        print self.Adj
        print "\n adverbs: \n"
        print self.Adv
        print "\n prepositions: \n"
        print self.Preposition
        print "=======================STATS========================== \n"
        temp = self.mostUsed()
        print temp[0][0] + " is the most used noun, used a total of " + str(temp[0][1]) + " times \n"
        print temp[1][0] + " is the most used verb, used a total of " + str(temp[1][1]) + " times \n"
        print temp[2][0] + " is the most used adjective, used a total of " + str(temp[2][1]) + " times \n"
        print temp[3][0] + " is the most used adverb, used a total of " + str(temp[3][1]) + " times \n"
        print temp[4][0] + " is the most used preposition, used a total of " + str(temp[4][1]) + " times \n"
        print "====================================================== \n"
        print"\n stopwords: \n"
        print s

        
twitter_acc = sys.argv[1]
#x = tweet_dumper.get_all_tweets(twitter_acc)

def gleanTweets(screenName):
    #reads twitter posts from csv file and appends them to list,
    #then tags each with nltk POS tagger
    file1 = open(screenName + '_tweets.csv')
    reader = csv.reader(file1)
    allTweets = []
    for row in reader:
        allTweets.append(row[2])
    allTweets = allTweets[0:(len(allTweets)/2)] #too much data for idle to handle at times
    taggedTweets = []
    for tweet in allTweets:
        text = tweet.split()
        textTagged = nltk.pos_tag(text)
        taggedTweets.append(textTagged)
    return taggedTweets

def puncRemover(word):
    #removes various punctuation from an input string word
    puncList = [".", ",",":","?","!"]
    if word[-1] in puncList:
        return word[:-1]
    else:
        return word
    

def sortTweet(taggedTweetList, POStag):
    #sorts through each tagged word in each tweet and returns list of words
    #tagged with input POStag
    result = []
    for tweet in taggedTweetList:
        for taggedWord in tweet:
            if POStag in taggedWord[1]:
                #print taggedWord[0]
                #b = taggedWord[0].encode('ascii','ignore')
                if "&" in taggedWord[0]: #removing &amp and urls
                    pass
                elif "/" in taggedWord[0]:
                    pass
                elif len(taggedWord[0]) == 1:
                    pass
                else:
                    if taggedWord[0] in result:
                        pass
                    else:
                        result.append(puncRemover(taggedWord[0]))
    return result

def createGrammar(screenName):
    #creates Grammar of twitter account screenName based on accounts
    #last 50 tweets
    #tweet_dumper.get_all_tweets(screenName)
    file1 = open(screenName + '_tweets.csv')
    reader = csv.reader(file1)
    allTweets = []
    for row in reader:
        allTweets.append(row[2])
    taggedTweets = gleanTweets(screenName)
    g = Grammar(allTweets, sortTweet(taggedTweets, "NN"), sortTweet(taggedTweets, "V"),
                            sortTweet(taggedTweets, "JJ"), sortTweet(taggedTweets, "RB"),
                            sortTweet(taggedTweets, "IN") + sortTweet(taggedTweets, "TO"))
    return g


createGrammar(sys.argv[1]).__repr__()
