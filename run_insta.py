from InstagramAPI import InstagramAPI
import requests,json
from time import sleep
from flask import Flask
from celery import Celery
import json
import sets
app = Flask(__name__)
celery = Celery(app.name, backend='amqp', broker='amqp://')
#log = logging.getLogger(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def get_unfollowers():
	followings = open('self_followings.json')
	loadAsJson = json.load(followings)
	followers = open('self_followers.json')
	secondJson = json.load(followers)
	first_arr = []
	second_arr = []
	for first_items in loadAsJson:
		first_arr.append(first_items['pk'])
	for second_items in secondJson:
		second_arr.append(second_items['pk'])

	set1 = set(first_arr)
	set2 = set(second_arr)
	unmatched = set1.symmetric_difference(set2)
	unmatch_arr = []
	for items in unmatched:
		unmatch_arr.append(items)

	print len(unmatch_arr)
	with open('unfollowers_assholes.json','wb') as outfile:
		json.dump(unmatch_arr,outfile,indent=4)

get_unfollowers()

@celery.task
def runProgram():
	arr_file = open('instagram_users.json')
	loadAsJson = json.load(arr_file)
	ig = InstagramAPI("jessicabloke", "123123123vb")
	ig.login()
	for items in loadAsJson[2000:]:
		pk_id = items['pk']
		follow_user = ig.follow(pk_id)
		print follow_user
		sleep(30)

@celery.task
def unfollow():
	unfollow_users = open('self_followers.json')
	loadAsJson = json.load(unfollow_users)
	ig = InstagramAPI("jessicabloke", "123123123vb")
	ig.login()
	#for items in loadAsJson:

@app.route("/")
def hello():
    execute = runProgram.delay()
    return "instagram following app deployed!"

# if __name__ == '__main__':
#     app.run()
