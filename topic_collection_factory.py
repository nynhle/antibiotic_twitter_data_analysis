import pymongo
import twitter_data_grabber as grabber
import json

class collection_factory():
	def return_collection_list(self):
		client = pymongo.MongoClient()
		db = client.topics

		if db.names_and_keywords.count() < 1:
			db.names_and_keywords.insert_one(json.dumps({"Name": "antibiotics", "Topic":"antibiotics"}))

		collection_list = []

		for data in db.names_and_keywords.find():
			collection_list.append(grabber.twitter_data_grabber(data['Topic'], data['Name']))

		return collection_list
