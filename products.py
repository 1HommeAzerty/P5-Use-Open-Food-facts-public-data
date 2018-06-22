#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8

import records



class Products:

    def __init__(self):
        self.dbconnection = records.Database('mysql+mysqlconnector://root@localhost/bdd_projet5?charset=utf8mb4')

    def get_products(self):
        return self.dbconnection.query("SELECT * FROM products LIMIT 1")

    def get_DE_products(self):
        return self.dbconnection.query("SELECT name, nutriscore FROM products WHERE nutriscore = 'd' OR nutriscore = 'e'")

    def get_ABC_products(self):
        return self.dbconnection.query(
            """SELECT name, nutriscore 
            FROM products 
            WHERE nutriscore = 'a' 
            OR nutriscore = 'b' 
            OR nutriscore = 'c'""")

    def get_stores_products(self):
        return self.dbconnection.query(
            """SELECT stores.* , products.*, product_store.* 
            FROM product_store 
            JOIN products 
            ON products.id = product_store.product_id 
            JOIN stores 
            ON stores.id = product_store.store_id""")


    def get_DE_products_by_category(self, category):
        return self.dbconnection.query(
            """SELECT name, nutriscore, id 
            FROM products 
            WHERE nutriscore 
            IN ('d','e') 
            AND category = :cat 
            ORDER BY RAND() 
            LIMIT 10""", 
            cat = category)


    def get_ABC_products_by_category(self, category):
        return self.dbconnection.query(
            """SELECT name, nutriscore, id 
            FROM products 
            WHERE nutriscore 
            IN ('a','b','c') 
            AND category = :cat 
            ORDER BY RAND() 
            LIMIT 5""", 
            cat = category)

    def get_favorites(self):            
        return self.dbconnection.query(
            """SELECT f.product_id, 
            products.name, 
            products.nutriscore,
            f.substitute_id, 
            p.name AS sname, 
            p.nutriscore AS sscore 
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
            id = productid)

    def fill_favorites(self, product_id, substitute_id):
        return self.dbconnection.query(
            """INSERT INTO favorites (product_id, substitute_id) 
            VALUES (:product_id, :substitute_id)""", 
            product_id = product_id, 
            substitute_id = substitute_id)
