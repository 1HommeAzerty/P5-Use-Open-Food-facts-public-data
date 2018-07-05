#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8


"""This module is in charge of the requests to the API and database"""

import json

import records

import requests

import dbconfig


class ProductsManager:
    """Gets a connection to the database with informations
    provided by the user in dbconfig.py.
    Makes requests to the API to get the data.
    Makes requests to fill the tables.
    Makes requests to the db to access the stored data.
    """

    def __init__(self):
        """Gets a connection to the database"""
        try:
            self.dbconnection = records.Database(dbconfig.DB_URL)
        except NameError:
            print(dbconfig.DB_URL)

    def get_stores_from_api(self):
        """Fetches the stores data from the API"""
        return requests.get(
            'https://fr.openfoodfacts.org/stores.json').json()

    def get_products_from_api(self, criteria):
        """Fetches the products data from the API"""
        return requests.get(
            'https://fr.openfoodfacts.org/cgi/search.pl',
            params=criteria).json()['products']

    def fill_stores(self, name):
        """Inserts stores name in the stores table"""
        return self.dbconnection.query(
            """INSERT INTO stores (name)
            VALUES (:name)""",
            name=name)

    def fill_products(self, product):
        """Inserts the products data in the products table"""
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
        """Gets the store's id from the store table"""
        return self.dbconnection.query(
            """SELECT id
            FROM stores
            WHERE LOWER(name) = :name
            LIMIT 1""",
            name=store).all()

    def fill_products_stores(self, store_id, product):
        """Fills the product_store table with products and stores ids"""
        return self.dbconnection.query(
            """INSERT INTO product_store (product_id, store_id)
            VALUES (:product_id, :store_id)""",
            product_id=product['code'],
            store_id=store_id)

    def get_stores_products(self):
        """Fetches stores and products detalis joining 3 tables"""
        return self.dbconnection.query(
            """SELECT stores.* , products.*, product_store.*
            FROM product_store
            JOIN products
            ON products.id = product_store.product_id
            JOIN stores
            ON stores.id = product_store.store_id""")

    def get_de_products_by_category(self, category):
        """Fetches a random list of 10 products with D or E score"""
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
        """Fetches a random list of 5 products with A, B or C score"""
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
        """Fetches favorites products data by joining the two tables"""
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
        """Fetches all data for a product for a given id"""
        return self.dbconnection.query(
            """SELECT *
            FROM products
            WHERE id = :id""",
            id=productid)

    def fill_favorites(self, product_id, substitute_id):
        """Insert the ids of the selected products into favorites"""
        return self.dbconnection.query(
            """INSERT INTO favorites (product_id, substitute_id)
            VALUES (:product_id, :substitute_id)""",
            product_id=product_id,
            substitute_id=substitute_id)
