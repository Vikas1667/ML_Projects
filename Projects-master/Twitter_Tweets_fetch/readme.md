## Twitter API Steps and Description
### To get starting with API:
1)Go to https://apps.twitter.com/ and apply for Developers account 
2) Fill up details and Note details Consumer key ,Consumer Secret and Access Token , Access Token secret from Keys and Access Tokens menu from your app.
3) Install Necessary Tweeter library  here I am using Tweepy
pip install tweepy 
#### Functions for Fetching tweets
To fetch tweets Tweeter has provided reference https://developer.twitter.com/en/docs/tweets/timelines/overview  from which I have used user_timeline but it has Limitation it can fetch max 200 recent tweets in one request but rather than user_timeline is able to fetch 3,200 of a user’s most recent Tweets,so  to get more tweets I have used Cursor http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html which allows pagination and make request more than 200 tweets. 
