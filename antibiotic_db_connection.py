from pymongo import MongoClient
import json

class database_connection():

	def __init__(self, topic):
		self.client = MongoClient()
		self.db = self.client.antibiotic_tweets
		self.tweets = self.db[topic]

	def insert_tweet(self, tweet):
		print tweet
		self.tweets.insert_one(json.loads(tweet))