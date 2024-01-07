import os

import pymysql
from dotenv import load_dotenv

load_dotenv()

global_connection = None


# Since logger should not use our database package (to avoid cyclic dependency) we are using the database directly
def get_connection() -> pymysql.connections.Connection:
    global global_connection
    if global_connection:
        return global_connection
    else:  # create, set and return global_connection
        global_connection = pymysql.connect(
            host=os.getenv('RDS_HOSTNAME'),
            user=os.getenv('RDS_USERNAME'),
            password=os.getenv('RDS_PASSWORD'),
        )
        return global_connection
