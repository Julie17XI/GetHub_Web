from datetime import datetime, timedelta
from flask import Flask, request
from flask_cors import CORS #comment this on deployment
from flask_restful import Api
import json
import pymysql.cursors
import yaml

from web_scraper import get_body_content

app = Flask(__name__)
CORS(app) #comment this on deployment
api = Api(app)

# db configuration
db = yaml.safe_load(open('db.yaml'))
def connect_db():
    connection = pymysql.connect(host=db['mysql_host'],
                                user=db['mysql_user'],
                                password=db['mysql_password'],
                                database=db['mysql_db'],
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

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
    username = request.json['username']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    database_res = get_user_info_from_database(username, timestamp)
    # if user info is in the database, retrieve this data and send it in JSON format to frontend
    # else conduct a real-time web scraping for that user, save the data na data, send it in JSON
    # format to frontend
    if database_res:
        return database_res
    else:
        info = scrape_user_info_from_web(username)
        store_scraping_res_to_database(info, timestamp)
        return json.dumps(info)

def get_user_info_from_database(username, timestamp):
    """
    Check if the username exists in database, and if the data has been updated within the last 24h,
    If so, retrieve the data for that username and convert the data into JSON format

    :param username: string, the input value sent from search box in the frontend
    :param timestamp: string, the current time

    :return: None | JSON, if the username is found in database, return the data in
    JSON format, else return None
    """
    connection = connect_db()
    connection.ping()
    with connection:
        database_user_info, cur_time = get_user_basics_from_database(username, timestamp)
        if database_user_info:
            within_24h = check_time(database_user_info, cur_time)
            if within_24h:
                get_repo_info_from_database(database_user_info, username)
                database_res=json.dumps(database_user_info)
                return database_res

def get_user_basics_from_database(username, timestamp):
    """
    Check if Users table in the database contains data for the given username and Record
    the current time.

    :param username: string, the input value sent from search box in the frontend
    :param timestamp: string, the time when we look up the username in the database

    :return: dict, contains user info including username, the number of public repositories
    and the number of last year's total contributions. E.g. {"username": "Jane",
    "repo_number": "2", "one_yr_contribution_number": "21"}
    :return: datetime.datetime object, the time when we look up the username in the database
    """
    connection = connect_db()
    connection.ping()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE user_name = %s", username)
            database_user_info=cursor.fetchone()
            cur_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            return database_user_info, cur_time

def check_time(database_user_info, cur_time):
    """
    Check if last time the given username's data was updated is within 24hrs.

    :param database_user_info: dict, contains user basics including username, the number of public
    repositories and the number of last year's total contributions
    :param timestamp: datetime.datetime object, the time when we look up the username in the database

    :return: boolean, if last time the given username's data was updated is within 24hrs
    """
    time_elapsed=(cur_time - database_user_info["last_search"])
    del database_user_info["last_search"]
    return time_elapsed < timedelta(hours=24)

def get_repo_info_from_database(database_user_info, username):
    """
    Get a list of public repositories with the given username from the database, and store it in
    the database_user_info

    :param database_user_info: dict, contains user basics including username, the number of public
    repositories and the number of last year's total contributions
    :param username: string, the input value sent from search box in the frontend

    :return: None, update the database_user_info, nothing returned
    """
    connection = connect_db()
    connection.ping()
    with connection:
            with connection.cursor() as cursor:
                cursor.execute(("SELECT pr.repo_name, pr.repo_language, pr.repo_description \
                                 FROM Public_Repositories AS pr INNER JOIN Users AS u \
                                 ON pr.user_id = u.id WHERE u.user_name = %s", username))
                database_pr_info=cursor.fetchall()
                database_user_info["repos_info"] = database_pr_info

def scrape_user_info_from_web(username):
    """
    Conduct a real-time web scraping from github

    :param username: dict, contains user basics including username, the number of public
    repositories and the number of last year's total contributions

    :return: dict, contains user info including username, the number of public repositories
    and the number of last year's total contributions, and a list of public repositories
    with the given username
    """
    info = get_body_content(username)
    return info

def store_scraping_res_to_database(info, timestamp):
    """
    Store web-scraped user data to database

    :param info: dict, contains user basics including username, the number of public
    repositories and the number of last year's total contributions
    :param timestamp: string, the current time

    :return: None, updates the database, and nothing is returned
    """
    connection = connect_db()
    connection.ping()
    with connection:
        with connection.cursor() as cursor:
            user_basics = info["user_info"]
            sql = "INSERT INTO Users (user_name, last_search, repo_number, one_yr_contribution_number) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user_basics["user_name"], timestamp, user_basics["repo_number"], user_basics["one_yr_contribution_number"]))
            name = user_basics["user_name"]
            cursor.execute("SELECT id FROM Users WHERE user_name = %s", name)
            user_id=cursor.fetchone()['id']

            for repo_info in info["repos_info"]:
                sql = "INSERT INTO Public_Repositories (repo_name, repo_lang, repo_description, user_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (repo_info["repo_name"], repo_info["repo_lang"], repo_info["repo_description"], user_id))
        connection.commit()

if __name__ == '__main__':
    app.run(debug=True)
