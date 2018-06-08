#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8

import records


dbconnection = records.Database('mysql+mysqlconnector://root@localhost/bdd_projet5?charset=utf8mb4')

def print_categories(config):
    cat = []
    with open(config, "r") as cfile:
        categories = [cat.strip() for cat in cfile.read().split(",")]
        for i, category in enumerate(categories):
            print(i+1, category)

def display_product():
    products = dbconnection.query("SELECT * FROM products LIMIT 1") #ORDER BY nutriscore")

    for product in products:
        print(f'{product["name"].decode("utf-8")}\n',
        f'Nutriscore: {product["nutriscore"].decode("utf-8")}\n',
        f'URL: {product["url"].decode("utf-8")}\n',
        'Barcode: ', product['id'])

display_product()
print_categories('config.txt')


#def select():
#   user_search = ""
#   while user_search == "":
#        .