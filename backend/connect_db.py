import pymysql.cursors
import yaml

# db configuration
db = yaml.safe_load(open('db.yaml'))
def connect_db():
    """
    Connect to MYSQL database
    """
    connection = pymysql.connect(host=db['mysql_host'],
                                user=db['mysql_user'],
                                password=db['mysql_password'],
                                database=db['mysql_db'],
                                cursorclass=pymysql.cursors.DictCursor)
    return connection
