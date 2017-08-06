import os
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect

class TwitterClient(object):
    '''
    Generic Twitter Class for the App
    '''

    def __init__(self, query, retweets_only=False, with_sentiment=False, **kwargs):
        self.sia = SentimentIntensityAnalyzer()
        # keys and tokens from the Twitter Dev Console
        consumer_key = kwargs["consumer_key"]
        consumer_secret = kwargs["consumer_secret"]
        access_token = kwargs["access_token"]
        access_token_secret = kwargs["access_token_secret"]
        # Attempt authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.query = query
            self.retweets_only = retweets_only
            self.with_sentiment = with_sentiment
            self.api = tweepy.API(self.auth)
            self.tweet_count_max = 100  # To prevent Rate Limiting
        except:
            print("Error: Authentication Failed")

    def set_query(self, query=''):
        self.query = query

    def set_retweet_checking(self, retweets_only='false'):
        self.retweets_only = retweets_only

    def set_with_sentiment(self, with_sentiment='false'):
        self.with_sentiment = with_sentiment

    def set_tweetcount(self, count=100):
        self.tweetcount = count

    def clean_tweet(self, tweet):
        return ' '.join(re.sub(
            r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweet_sentiment_vader(self, tweet):
        analysis = self.sia.polarity_scores(tweet)["compound"]
        if analysis > 0:
            return 'positive'
        elif analysis == 0:
            return 'neutral'
        
        return 'negative'

    def get_tweets(self):
        tweets = []
        unique_tweets = set()

        try:
            # how many groups of `tweet_count_max` tweets
            no_of_100tweets = self.tweetcount // self.tweet_count_max
            # how many do not belong in a `tweet_count_max` group
            no_of_remaining_tweets = self.tweetcount - \
                self.tweet_count_max * no_of_100tweets

            if no_of_remaining_tweets:
                recd_tweets = self.api.search(
                    q=self.query, count=no_of_remaining_tweets)
            else:
                recd_tweets = []

            maxId = recd_tweets[-1].id if recd_tweets else 0

            for _ in range(no_of_100tweets):
                nxtpg_recd_tweets = self.api.search(
                    q=self.query,
                    count=self.tweet_count_max,
                    max_id=str(maxId - 1))
                recd_tweets.extend(nxtpg_recd_tweets)
                maxId = nxtpg_recd_tweets[-1].id

            if not recd_tweets:
                pass

            for tweet in recd_tweets:
                try:
                    if detect(tweet.text) != 'en':
                        continue
                except:
                    continue

                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text
                parsed_tweet['user'] = tweet.user.screen_name

                if self.with_sentiment == 1:
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(
                        tweet.text)
                    parsed_tweet['sentiment_vader'] = self.get_tweet_sentiment_vader(tweet.text)
                else:
                    parsed_tweet['sentiment'] = 'unavailable'
                    parsed_tweet['sentiment_vader'] = 'unavailable'

                if tweet.retweet_count > 0 and self.retweets_only == 1:
                    if parsed_tweet['text'] not in unique_tweets:
                        tweets.append(parsed_tweet)
                        unique_tweets.add(parsed_tweet['text'].lower())
                elif not self.retweets_only:
                    if parsed_tweet['text'] not in unique_tweets:
                        tweets.append(parsed_tweet)
                        unique_tweets.add(parsed_tweet['text'].lower())

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))
