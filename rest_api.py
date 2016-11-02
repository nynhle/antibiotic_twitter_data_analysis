from flask import Flask, send_from_directory, redirect, url_for, jsonify, request
from twitter_data_grabber import twitter_data_grabber
import json
import pymongo
import topic_collection_factory as f

app = Flask(__name__)


factory = f.collection_factory()
grabber_list = factory.return_collection_list()


# Endpoint for the main page..
@app.route('/')
def index():
	return send_from_directory('.', 'index.html')

@app.route('/create_dataset')
def create_dataset_view():
	return send_from_directory('.', 'create_dataset.html')

@app.route('/dashboard')
def render_dashboard():
	return send_from_directory('.', 'dashboard.html')

@app.route('/statistics')
def render_statistics():
	return send_from_directory('.', 'statistics.html')

@app.route('/post_new_dataset', methods=['POST'])
def post_new_dataset():

	collection_name = request.form['new_keyword_name']
	keyword = request.form['new_keyword']
	client = pymongo.MongoClient()
	db = client.topics

	for db_post in db.names_and_keywords.find():
		if db_post['Name'] == collection_name:
			return send_from_directory('.', 'create_dataset_fail.html')

	new_grabber = twitter_data_grabber(keyword, collection_name)
	grabber_list.append(new_grabber)
	try:
		new_grabber.start()
		db.names_and_keywords.insert_one(
			{
			"Topic": keyword,
			"Name": collection_name
			})
		return send_from_directory('.', 'create_dataset_success.html')
	except Exception, e:
		print e
		return send_from_directory('.', 'create_dataset_fail.html')

@app.route('/change_topic_status/<topic>')
def change_status(topic):
	for grabber in grabber_list:
		if topic == grabber.name:
			if grabber.isStreaming:
				grabber.stop()
			else:
				grabber.start()
			break
	return redirect('/dashboard')


@app.route('/get_topics')
def return_topics():
	json_grabbers = []

	for grabber in grabber_list:
		json_grabbers.append({
			"Name": grabber.name,
			"Keyword": grabber.topic,
			"Active": grabber.isStreaming
			})

	return json.dumps({
		"Datasets": json_grabbers
		})



if __name__ == '__main__':
	app.run()
