from datetime import datetime, timedelta
import json

from connect_db import connect_db

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
        if database_user_info and database_user_info["user_info"]:
            within_24h = check_time(database_user_info, cur_time)
            if within_24h:
                print("it is new enough")
                get_repo_info_from_database(database_user_info, username)
                print("get repo info")

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
        database_user_info = {}
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE user_name = %s", username)
            database_user_info["user_info"]=cursor.fetchone()
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
    time_elapsed=(cur_time - database_user_info["user_info"]["last_search"])
    del database_user_info["user_info"]["last_search"]
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
                cursor.execute("SELECT pr.repo_name, pr.repo_lang, pr.repo_description \
                                 FROM Public_Repositories AS pr INNER JOIN Users AS u \
                                 ON pr.user_id = u.id WHERE u.user_name = %s", username)
                database_pr_info=cursor.fetchall()
                database_user_info["repos_info"] = database_pr_info

def handle_scraping_res_to_database(info, username, timestamp):
    """
    Store web-scraped user data to database if the given user does not exist in the database;
    If the user exists in the database, but last update was conduted before 24hrs, update the
    data for that user in database.

    :param info: dict, contains user basics including username, the number of public
    repositories and the number of last year's total contributions
    :param timestamp: string, the current time

    :return: None, updates the database, and nothing is returned
    """
    connection = connect_db()
    connection.ping()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM Users WHERE user_name = %s", username)
            user=cursor.fetchone()
            if user:
                user_id = user["id"]
                update_scraping_res_to_database(info, timestamp, user_id)
            else:
                insert_scraping_res_to_database(info, timestamp)

def update_scraping_res_to_database(info, timestamp, user_id):
    """
    Update the data for that user in database if the user exists in the database, but last update
    was conduted before 24hrs.

    :param info: dict, contains user basics including username, the number of public
    repositories and the number of last year's total contributions
    :param timestamp: string, the current time
    :param user_id: string, the user_id in Users table

    :return: None, updates the database, and nothing is returned
    """
    connection = connect_db()
    connection.ping()
    with connection:
        with connection.cursor() as cursor:
            user_basics = info["user_info"]
            sql = "UPDATE Users SET last_search = %s, repo_number = %s, one_yr_contribution_number = %s\
                   WHERE id = %s;"
            cursor.execute(sql, (timestamp, user_basics["repo_number"], user_basics["one_yr_contribution_number"], user_id))
            for repo_info in info["repos_info"]:
                sql = "DELETE FROM Public_Repositories WHERE user_id = %s;"
                cursor.execute(sql, user_id)
                for repo_info in info["repos_info"]:
                    sql = "INSERT INTO Public_Repositories (repo_name, repo_lang, repo_description, user_id) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (repo_info["repo_name"], repo_info["repo_lang"], repo_info["repo_description"], user_id))
            connection.commit()

def insert_scraping_res_to_database(info, timestamp):
    """
    Store web-scraped user data to database if the given user does not exist in the database.

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
