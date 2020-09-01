#!/usr/bin/env python
import tweepy
from datetime import datetime
import random
import string

"""
Bot.py: Classes for creating computational agents or bots
Author: Hunter Priniski and Chaewon Bak
Contact: priniski@ucla.edu
"""

class Bot:
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret

    @property
    def credentials(self):
        return {'consumer_key': self.consumer_key, 'consumer_secret': self.consumer_secret, 'access_token': self.access_token, 'access_secret': self.access_secret}

    #add read Bot from JSON



class RedditBot(Bot):

    platform = 'Reddit'

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        super().__init__(consumer_key, consumer_secret, access_token, access_secret)


class TwitterBot(Bot):

    platform = 'Twitter'

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        super().__init__(consumer_key, consumer_secret, access_token, access_secret)

    @property
    def authenitcation(self):
        consumer_key = self.credentials['consumer_key']
        consumer_secret = self.credentials['consumer_secret']

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)

        return auth

    @property
    def connection(self, wait_on_rate_limit = True, wait_on_rate_limit_notify = True):
        connection = tweepy.API(self.authenitcation, wait_on_rate_limit = wait_on_rate_limit, wait_on_rate_limit_notify = wait_on_rate_limit_notify)

        return connection

    @property
    def information(self):
        return self.connection.me()._json

    """
    A run command instructs bots on the basis of a string command
    """
    def run(self, cmd_str):
        command, arg_str = cmd_str.split(":")
        args = arg_str.split(',')

        method = getattr(self, command)

        return method(args)

    """
    Action methods.
    """
    def tweet(self, args):
        text = args[0]
        self.connection.update_status(text)

        time = datetime.now().strftime("%D:%H:%M:%S")
        return {time:{'tweet':text}}

    def retweet(self, args):
        tweet_id = args[0]
        self.connection.retweet(tweet_id)

        time = datetime.now().strftime("%D:%H:%M:%S")
        return {time:{'retweet':tweet_id}}

    def favorite(self, args):
        tweet_id = args[0]
        self.connection.create_favorite(tweet_id)

        time = datetime.now().strftime("%D:%H:%M:%S")
        return {time:{'favorite':tweet_id}}

    #can we create a seperate follow method that follows based on screen_name?it would be called follow_screen_name
    def follow(self, args):
        user_id = args[0]
        id_ = self.connection.get_user(user_id).id
        self.connection.create_friendship(id_)

        time = datetime.now().strftime("%D:%H:%M:%S")
        return {time:{'follow':user_id}}

    def reply(self, args, auto_populate_reply_metadata = True):
        text, tweet_id = args
        self.connection.update_status(status=text, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=auto_populate_reply_metadata)

        time = datetime.now().strftime("%D:%H:%M:%S")
        return {time:{'reply':(tweet_id, text)}}

    """
    Information collection methods.
    """
    #change this code so we can get tweets based on a user id.
    def get_userid_tweets(self, args):
        user_id = args[0]
        tweets = []
        for tweet in tweepy.Cursor(self.connection.user_timeline,  user_id=user_id, tweet_mode="extended").items():
            tweets.append(tweet)
        return tweets

    def get_username_tweets(self, args, tweet_mode = 'extended'):
        user_name = args[0]
        tweets = []
        for tweet in tweepy.Cursor(self.connection.user_timeline, screen_name=user_name, tweet_mode = tweet_mode).items():
            tweets.append(tweet)
        return tweets
