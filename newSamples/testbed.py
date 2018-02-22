#!/usr/bin/python
# -*- coding: utf-8 -*-
#Import the necessary methods from tweepy library
import tweepy
import io
import time


import sys

#Variables that contains the user credentials to access Twitter API
access_token = "1154478061-irvRElFnzbyktMD5LtUgY6KJ2cfKhV6qBJwuyhO"
access_token_secret = "65jHAVRDxFTu0ArfWpnHy8pD17VBMgcgvW4NjhSE0MJcs"
consumer_key = "glpgm50xNmf08m9t0EzZtEdwL"
consumer_secret = "6uXDpXeu9a48aA0Wz504fD9ywrdj4dXFL82Zab88WQJvtJdnm7"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterUser = sys.argv[1]



if __name__ == '__main__':

    api = tweepy.API(auth)

    users = tweepy.Cursor(api.followers, screen_name=twitterUser).items()
    print users

    while True:
        try:
            user = next(users)
        except tweepy.TweepError:
            time.sleep(60*15)
            user = next(users)
        except StopIteration:
            break
        print "@" + user.screen_name
        twitterUser = user.screen_name
        try:
            stuff = api.user_timeline(screen_name = twitterUser, count = 3000, include_rts = False)
        except tweepy.TweepError:
            
        f1 = io.open(twitterUser+ "_1.txt", "w+")
        f2 = io.open(twitterUser+ "_2.txt", "w+")
        split = 0
        for status in stuff:
            if (split%2==0):
                f1.write(status.text + '\n')
            else:
                f2.write(status.text + '\n')
            split+=1
        f1.close()
        f2.close()
