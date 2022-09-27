from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS #comment this on deployment
import pymysql.cursors
from web_scraper import user_info
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
        return "Hello"

    username = request.json['username']

    # cur.execute('SELECT * FROM users WHERE user_name = %s', (username))
    # data = cur.fetchall()
    # cur.close()
    # if data:
    #     print(data)
    #     return data

    info = user_info(username)
    print(info)
    if not info:
        return {}

    user_name = info["user"]
    repo_number = info["repo_nums"]
    one_yr_contribution_number = info["last_yr_contribution"]
    repos_info = info["repos_info"]

    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO users (id, user_name, repo_number, one_yr_contribution_number) VALUES (%s,%s,%s,%s)", ("",user_name, repo_number, one_yr_contribution_number))
    # mysql.connection.commit()
    # cur.execute('SELECT * FROM users WHERE user_name = %s', (user_name))
    # data = cur.fetchall()
    # user_id = data[0][id]
    for repo_info in repos_info:
        if "repo_name" in repo_info:
            repo_name = repo_info["repo_name"]
        else:
            repo_name = None
        if "repo_lang" in repo_info:
            repo_language = repo_info["repo_lang"]
        else:
            repo_language = None
        if "repo_description" in repo_info:
            repo_description = repo_info["repo_description"]
        else:
            repo_description = None
    #     cur.execute("INSERT INTO public_repositories (id, repo_name, repo_language, repo_description, user_id) VALUES (%s,%s,%s,%s)", ("",repo_name, repo_language, repo_description, user_id))
    #     mysql.connection.commit()
    # flash('Record Added successfully')

    return json.dumps(info)


if __name__ == '__main__':
    app.run(debug=True)
