from datetime import datetime
from flask import Flask, request
from flask_cors import CORS #comment this on deployment
from flask_restful import Api
import json

from create_db import create_db
from db import get_user_info_from_database, handle_scraping_res_to_database
from web_scraper import scrape_user_info_from_web

app = Flask(__name__)
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", methods = ['GET','POST'])
def index():
    """
    Send reponse back to frontend in accordance with HTTP request.

    :param username: None, no param needed

    :return: None | JSON, the data about the user and his/her list of public repositories
    """
    if request.method == "GET":
        return
    # Below handles request.method == "POST"
    create_db()
    username = request.json['username']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    database_res = get_user_info_from_database(username, timestamp)
    # if user info is in the database, retrieve this data and send it in JSON format to frontend
    # else conduct a real-time web scraping for that user, save the data, send it in JSON
    # format to frontend
    if database_res:
        return database_res
    else:
        info = scrape_user_info_from_web(username)
        handle_scraping_res_to_database(info, username, timestamp)
        return json.dumps(info)

if __name__ == '__main__':
    app.run(debug=True)
