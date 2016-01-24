from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import StreamListener
from credentials import credentials

consumer_key = credentials().consumer_key
consumer_secret = credentials().consumer_secret
access_token = credentials().access_token
access_token_secret = credentials().access_token_secret

class listener(StreamListener):
	def on_data(self, data):
		print data
		return True

	def on_error(self, status):
		print status


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterstream = Stream(auth, listener())
twitterstream.filter(track=['antibiotic'])
