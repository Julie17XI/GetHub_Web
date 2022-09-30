from flask import Flask, request, redirect, url_for
from flask_restful import Api
from flask_cors import CORS #comment this on deployment
from web_scraper import user_info
from datetime import datetime
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
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = request.json['username']

    info = user_info(username)
    res = json.dumps(info)

    connection.ping()
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Users (user_name, last_search, repo_number, one_yr_contribution_number) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (info["user"], timestamp, info["repo_nums"], info["last_yr_contribution"]))
            name = info["user"]
            cursor.execute("SELECT id FROM Users WHERE user_name = %s", name)
            user_id=cursor.fetchone()['id']

            for repo_info in info["repos_info"]:
                print(repo_info)
                sql = "INSERT INTO Public_Repositories (repo_name, repo_lang, repo_description, user_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (repo_info["repo_name"], repo_info["repo_lang"], repo_info["repo_description"], user_id))
        connection.commit()
    return res

if __name__ == '__main__':
    app.run(debug=True)
