from connect_db import connect_db

def create_db():
    """
    Create Users and Public_Repositories tables in MYSQL database if they don't exist
    """
    connection = connect_db()
    connection.ping()
    with connection:
            with connection.cursor() as cursor:
                create_users_table = "CREATE TABLE IF NOT EXISTS Users(\
                                id INT(32) NOT NULL AUTO_INCREMENT,\
                                user_name VARCHAR(20) NOT NULL ,\
                                last_search TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,\
                                repo_number VARCHAR(20) NOT NULL ,\
                                one_yr_contribution_number VARCHAR(20) NOT NULL ,\
                                PRIMARY KEY (id));"
                create_public_repositories_table = "CREATE TABLE IF NOT EXISTS Public_Repositories(\
                                repo_id INT(32) NOT NULL AUTO_INCREMENT ,\
                                repo_name VARCHAR(100) NOT NULL ,\
                                repo_lang VARCHAR(20) ,\
                                repo_description TEXT ,\
                                user_id INT(32) NOT NULL ,\
                                FOREIGN KEY (user_id) REFERENCES Users(id) , PRIMARY KEY (repo_id));\
                                "
                cursor.execute(create_users_table)
                cursor.execute(create_public_repositories_table)
                connection.commit()
