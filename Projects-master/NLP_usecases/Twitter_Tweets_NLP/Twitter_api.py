import tweepy
from twitter import Api,TwitterError
import os
import json
import oauth2 as oauth
from tweepy import OAuthHandler
from dotenv import load_dotenv
import pandas as pd
import csv

load_dotenv()

def get_keys(path):
    with open(path) as f:
        return json.load(f)

keys = get_keys(".secret/twitter_api_key.json")
print(keys['API Key'])
# CONSUMER_KEY
CONSUMER_KEY = os.getenv('API Key')
print(CONSUMER_KEY)
# CONSUMER_SECRET
 
CONSUMER_SECRET = ''
# ACCESS_TOKEN 
ACCESS_TOKEN = ''
# ACCESS_TOKEN_SECRET 
ACCESS_TOKEN_SECRET = ''

USER= ''            ##username for which you want to fetch tweets
LANGUAGES = ['en']  #Language preference as I am using English
list_of_tweets=[]
    
def get_tweets(username): 
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET) 
    
    # Access to user's access key and access secret 
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
  
    # Calling api 
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 
    
    for tweets in tweepy.Cursor(api.user_timeline,screen_name=username,count=1000).items():
        tweet=tweets._json['text']
        list_of_tweets.append(tweet)
        
    print(len(list_of_tweets))
    return list_of_tweets 
    
       
    
