#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8

import records

import requests

import pymysql


class Products:

    def __init__(self):
        try:
            self.dbconnection = records.Database('mysql+mysqlconnector://root@localhost/bdd_projet5?charset=utf8mb4')
        except:
            print("Error")

    def get_stores_from_api(self):
        return requests.get(
            'https://fr.openfoodfacts.org/stores.json').json()

    def get_products_from_api(self, criteria):
        return requests.get(
            'https://fr.openfoodfacts.org/cgi/search.pl',
            params=criteria).json()['products']

    def fill_stores(self, name):
        return self.dbconnection.query(
            """INSERT INTO stores (name)
            VALUES (:name)""",
            name=name)

    def fill_products(self, product):
        return self.dbconnection.query(
            """INSERT INTO products (id, name, nutriscore, url, category)
            VALUES (:id, :name, :nutriscore, :url, :category)
            ON DUPLICATE KEY
            UPDATE id = :id""",
            id=product['code'],
            name=product['product_name'],
            nutriscore=product['nutrition_grade_fr'],
            url=product['url'],
            category=product['category'])

    def get_store_id(self, store):
        return self.dbconnection.query(
            """SELECT id
            FROM stores
            WHERE LOWER(name) = :name
            LIMIT 1""",
            name=store).all()

    def fill_products_stores(self, store_id, product):
        return self.dbconnection.query(
            """INSERT INTO product_store (product_id, store_id)
            VALUES (:product_id, :store_id)""",
            product_id=product['code'],
            store_id=store_id)

    def get_stores_products(self):
        return self.dbconnection.query(
            """SELECT stores.* , products.*, product_store.*
            FROM product_store
            JOIN products
            ON products.id = product_store.product_id
            JOIN stores
            ON stores.id = product_store.store_id""")

    def get_de_products_by_category(self, category):
        return self.dbconnection.query(
            """SELECT name, nutriscore, id
            FROM products
            WHERE nutriscore
            IN ('d','e')
            AND category = :cat
            ORDER BY RAND()
            LIMIT 10""",
            cat=category)

    def get_abc_products_by_category(self, category):
        return self.dbconnection.query(
            """SELECT name, nutriscore, id
            FROM products
            WHERE nutriscore
            IN ('a','b','c')
            AND category = :cat
            ORDER BY RAND()
            LIMIT 5""",
            cat=category)

    def get_favorites(self):
        return self.dbconnection.query(
            """SELECT f.product_id,
            products.name,
            products.nutriscore,
            f.substitute_id AS sid,
            p.name AS sname,
            p.nutriscore AS sscore,
            p.url AS surl
            FROM favorites AS f
            INNER JOIN products
            ON products.id = f.product_id
            INNER JOIN products AS p
            ON p.id = f.substitute_id""")

    def get_product(self, productid):
        return self.dbconnection.query(
            """SELECT *
            FROM products
            WHERE id = :id""",
            id=productid)

    def fill_favorites(self, product_id, substitute_id):
        return self.dbconnection.query(
            """INSERT INTO favorites (product_id, substitute_id)
            VALUES (:product_id, :substitute_id)""",
            product_id=product_id,
            substitute_id=substitute_id)
