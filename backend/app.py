from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS #comment this on deployment
from web_scraper import user_info
from datetime import datetime, timedelta
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
    if request.method == "GET":
        return
    # get search input and current time
    username = request.json['username']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # check if username is in database and the data has been updated within 24 hours
    # if so, retrieve data from database
    connection.ping()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE user_name = %s", username)
            database_info=cursor.fetchone()
            if database_info:
                database_user_id = database_info["id"]
                cursor.execute("SELECT * FROM Public_Repositories WHERE user_id = %d" %database_user_id)
                database_pr_info=cursor.fetchall()
                cur_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                time_elapsed=(cur_time - database_info["last_search"])
                if time_elapsed < timedelta(hours=24):
                    del database_info["last_search"]
                    database_info["repos_info"] = database_pr_info
                    database_res=json.dumps(database_info)
                    return database_res

    # if not, conduct a real-time web scraping from github
    # return real-time data to React app
    info = user_info(username)
    res = json.dumps(info)

    # save web scraping result to database
    connection.ping()
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Users (user_name, last_search, repo_number, one_yr_contribution_number) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (info["user_name"], timestamp, info["repo_number"], info["one_yr_contribution_number"]))
            name = info["user_name"]
            cursor.execute("SELECT id FROM Users WHERE user_name = %s", name)
            user_id=cursor.fetchone()['id']

            for repo_info in info["repos_info"]:
                sql = "INSERT INTO Public_Repositories (repo_name, repo_lang, repo_description, user_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (repo_info["repo_name"], repo_info["repo_lang"], repo_info["repo_description"], user_id))
        connection.commit()
    return res

if __name__ == '__main__':
    app.run(debug=True)
