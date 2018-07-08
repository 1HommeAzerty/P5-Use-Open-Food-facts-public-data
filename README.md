# P5 Use OpenFood facts public data

This program was created for academic
purposes, produced for [OpenClassrooms.com](https://openclassrooms.com/). All images and names are trademarks
of their respective owners.

The objective was to create a Python program to 
get data from the [Open Food Facts](https://world.openfoodfacts.org/) API,
store it in a database,
allow the user to choose a product, a substitute and have some basic informations about it.

How to install:
- Install Python 3.6.3
- to install the virtual environement in command line enter: pip install virtualenv 
- then source env/bin/activate
- install the required libraries using the line:  pip install -r requirements.txt
- create a new MySQL database, no need to create any tables, be sure to have a user that has all privileges on it
- open the dbconfig.py file in a text editor
- modify the fields in DB_CONFIG accordingly to your database and user infos like in the exemple below :
```python
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'MyDatabase',
    'user': 'MyUsername',
    'password': 'MySecretPassw0rd',
    'port': 3306,
    'charset': 'utf8mb4'
}
```
- you can now execute the dbinstall.py file to install the tables
- you can now execute the install.py file to fill the tables
- you can now execute main.py to start

NOTE: before using install.py you can change to the categories you want in the config.txt file. A list of categories is available [here](https://fr.openfoodfacts.org/categories)
