import tweepy
from pymongo import MongoClient
import json
from credentials import credentials # Class containing credentials for OAuth on twitter. Secret.

# Getting the credentials to get authenticated.
consumer_key = credentials().consumer_key
consumer_secret = credentials().consumer_secret
access_token = credentials().access_token
access_token_secret = credentials().access_token_secret

# Connecting to local mongodb instance
client = MongoClient()
db = client.antibiotic_tweets
tweets = db.tweets

class listener(tweepy.StreamListener):
	def on_data(self, data):
		tweets.insert_one(json.loads(data))
		print "Tweet recorded..."
		return True

	def on_error(self, status):
		print status


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterstream = tweepy.Stream(auth, listener())
twitterstream.filter(track=['antibiotic'])

class twitter_data_grabber():
	
	def load_user_data():
		self.consumer_key = credentials().consumer_key
		self.consumer_secret = credentials().consumer_secret
		self.access_token = credentials().access_token
		self.access_token_secret = credentials().access_token_secret

	def set_user_data():
		self.auth =tweepy.OAuthHandler(consumer_key, consumer_secret)
		self.auth.set_access_token(access_token, access_token_secret)

	def open_stream():
		self.twitterstream = tweepy.Stream(self.auth, listener())
		twitterstream.filter(track=['antibiotic'])

	def start():
		self.load_user_data()
		self.set_user_data()
		self.open_stream()

	
	




