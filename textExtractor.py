#!/usr/bin/env python
import json

tweets_data_path = "twitter_data.json"

tweets_file = open(tweets_data_path).read()

tweets_data = json.loads(tweets_file[5])

print tweets_data
