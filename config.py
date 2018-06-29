DB_CONFIG = {
    'host': 'host',
    'dbname': 'Database name',
    'user': 'username',
    'password': 'your password',
    'port': 3306
}

DB_URL = """mysql+mysqlconnector://
        {user}:{password}@{host}/{dbname}?charset=utf8mb4""".format(**DB_CONFIG)
