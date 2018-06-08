#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8

import json

import requests

import records

import pymysql

dbconnection = records.Database('mysql+mysqlconnector://root@localhost/bdd_projet5?charset=utf8mb4')

categories = ['desserts', 'boissons sans alcool', 'confiseries', 'chips']


def get_stores():
    response = requests.get('https://fr.openfoodfacts.org/stores.json')
    res =  response.json()
    return res

def get_products(categories, number=1000):
    products = []
    for category in categories:
        criteria = {
            'action':'process',
            'json':1,
            'tagtype_0':'categories',
            'tag_contains_0':'contains',
            'tag_0': category,
            'page_size': number}
        response = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=criteria)
        res =  response.json()
        for product in res['products']:
            product['category'] = category
        products.extend(res['products'])
    return products


def fill_stores():
    data = get_stores()

    for dt in data['tags']:
        if dt['products'] >= 10:
            dbconnection.query("INSERT INTO stores (name)"\
                       "VALUES (:name)", name = dt['name'])
            print(dt['name'])
        else:
            pass

def fill_products():
    products = get_products(categories)


    for product in products:
        if 'stores' in product and product['stores'] != "" :
            if 'nutrition_grade_fr' in product and product['nutrition_grade_fr'] != "":
                dbconnection.query("INSERT INTO products (id, name, nutriscore, url, category)"\
                           "VALUES (:id, :name, :nutriscore, :url, :category) ON DUPLICATE KEY UPDATE id = :id", id = product['code'], name = product['product_name'], nutriscore = product['nutrition_grade_fr'], url = product['url'], category = product['category'])
                #print(product['product_name'], product['nutrition_grade_fr'], product['stores_tags'])
                
                #product_id = dbconnection.query("SELECT id FROM products WHERE name = :name LIMIT 1", name = product['product_name'])



                for store in product['stores_tags']:
                    store_id = dbconnection.query("SELECT id FROM stores WHERE LOWER(name) = :name LIMIT 1" , name = store).all()

                    if len(store_id):
                        print(product['product_name'],store, store_id)
                        dbconnection.query("INSERT INTO product_store (product_id, store_id)"\
                                    "VALUES (:product_id, :store_id)", product_id = product['code'], store_id = store_id[0]['id'])
                        
        else:
            pass

fill_products()
