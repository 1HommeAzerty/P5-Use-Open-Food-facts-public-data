
"""This module allows the user to enter their database informations"""

DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'your_database_name',
    'user': 'your_user_name',
    'password': 'your_password',
    'port': 3306,
    'charset': 'utf8mb4'
}

DB_URL = """mysql+mysqlconnector://
        {user}:{password}@{host}:{port}/{dbname}?charset={charset}
        """.format(**DB_CONFIG)
