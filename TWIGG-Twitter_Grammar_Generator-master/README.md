TWIGG: Twitter Grammar Generator
--------------------------------
SYNOPSIS
----------------
This is a script that pulls the most recent 50 tweets from a person’s Twitter account and then uses those tweets to generate a grammar unique to that user and provides brief statistical analysis of data.
---------------------
INSTALLATION
---------------------
Download the file to a directory on your computer. Open the file and change the “screenName” variable to the user screen name of your choice. Then, run as you would run any other python script (e.g. python /path/to/file/script.py).
--------------------
DESIGN
--------------------
First, our script gathers the most recent 50 tweets from a user’s timeline via the tweet_dumper.py script written by GitHub user yanofsky. We also make use of the Twitter API through the python package, python-twitter. A CSV file is opened in the directory of the script and the tweets are written to that CSV file. Next, we read through the CSV and build a list of tweets, each tweet represented as a string. Those strings are split and then tagged using NLTK’s POS tagger. Finally, we sort the POS tags and build lists of words with the same tag. Analysis of the grammar shows the sorted lists as well as the most used word in each part of speech.
---------------
AUTHORS
---------------
Coded by Alex Snow, Derek Roth, and Chris Bobbe
----------------------------------
ACKNOWLEDGEMENTS
----------------------------------
Thanks to GitHub user yanofsky.
