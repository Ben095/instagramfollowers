from InstagramAPI import InstagramAPI
import requests,json
from time import sleep
from flask import Flask

app = Flask(__name__)
celery = Celery(app.name, backend='amqp', broker='amqp://')
log = logging.getLogger(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@celery.task
def runProgram():
	arr_file = open('instagram_users.json')
	loadAsJson = json.load(arr_file)
	ig = InstagramAPI("jessicabloke", "123123123vb")
	ig.login()
	for items in loadAsJson[:5000]:
		pk_id = items['pk']
		follow_user = ig.follow(pk_id)
		print follow_user
		sleep(80)

@app.route("/")
def hello():
    execute = runProgram.delay()
    return "instagram following app deployed!"

if __name__ == '__main__':
    app.run()
