from flask import Flask, request, redirect, url_for
from flask_restful import Api
from flask_cors import CORS #comment this on deployment
from web_scraper import user_info
import pymysql.cursors
import json
import yaml

app = Flask(__name__)
CORS(app) #comment this on deployment
api = Api(app)

# db configuration
db = yaml.safe_load(open('db.yaml'))
connection = pymysql.connect(host=db['mysql_host'],
                             user=db['mysql_user'],
                             password=db['mysql_password'],
                             database=db['mysql_db'],
                             cursorclass=pymysql.cursors.DictCursor)

@app.route("/", methods = ['GET','POST'])
def index():
    # display ABOUT as BODY
    if request.method == "GET":
        return

    username = request.json['username']
    info = user_info(username)
    return json.dumps(info)

if __name__ == '__main__':
    app.run(debug=True)
