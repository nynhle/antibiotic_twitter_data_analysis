import tweepy
import json
from antibiotic_db_connection import database_connection

# Class extending the tweepy streamlistener. Customized to be able to 
# store the data in the mongodb database via the antibiotic_db_connection class.
class listener(tweepy.StreamListener):

	def __init__(self, topic):
		self.api = tweepy.API()
		self.con = database_connection(topic)
		self.shouldBeStreaming = True

	def on_data(self, data):
		if self.shouldBeStreaming:
			self.con.insert_tweet(data)
			return True
		else:
			return False

	def on_error(self, status):
		print status

	def exit(self):
		self.shouldBeStreaming = False