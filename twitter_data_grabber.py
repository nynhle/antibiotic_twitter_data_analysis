import tweepy
from twitter_listener import listener
from credentials import credentials
import threading

# Class containing the connection to the twitter stream and the tool to filter data.
# Responsible to connect to twitter, filter data and pass relevant data to the DB-connection class.
class twitter_data_grabber():

	def __init__(self, topic, name):
		self.isStreaming = False
		self.topic = topic
		self.name = name
		self.load_user_data()
		self.set_user_data()
		self.twitterstream = tweepy.Stream(self.auth, listener(self.name))

	
	# App linked to one account. Loading the credentials from a separate file. The information is secret.
	def load_user_data(self):
		self.consumer_key = credentials().consumer_key
		self.consumer_secret = credentials().consumer_secret
		self.access_token = credentials().access_token
		self.access_token_secret = credentials().access_token_secret

	# Passing in the credentials into the auth object. 
	def set_user_data(self):
		self.auth =tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)


	def start(self):
		self.twitterstream.filter(track=[self.topic], async = True)
		self.isStreaming = True


	def stop(self):
		if self.isStreaming:
			self.twitterstream.listener.exit()
			self.isStreaming = False
