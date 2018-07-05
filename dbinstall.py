#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8


"""This module is in charge of the database creation."""

import records

import requests

import dbconfig


class Dbinstaller:
    """Gets a connection to the database with informations
    provided by the user in dbconfig.py.
    Creates the tables required for the program to work properly.
    """

    def __init__(self):
        """Gets a connection to the database with informations
        provided by the user in dbconfig.py.
        Drops the tables if necessary.
        """
        self.dbconnection = records.Database(dbconfig.DB_URL)
        self.dbconnection.query("""DROP TABLE IF EXISTS products""")
        self.dbconnection.query("""DROP TABLE IF EXISTS favorites""")
        self.dbconnection.query("""DROP TABLE IF EXISTS product_store""")
        self.dbconnection.query("""DROP TABLE IF EXISTS stores""")

    def create_products(self):
        """Creates the table products"""
        self.dbconnection.query(
            """CREATE TABLE IF NOT EXISTS products (
            id bigint(20) NOT NULL,
            name varchar(300) NOT NULL,
            nutriscore varchar(1) NOT NULL,
            url varchar(2000) NOT NULL,
            category varchar(100) NOT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY id (id))""")

    def create_stores(self):
        """Creates the table stores"""
        self.dbconnection.query(
            """CREATE TABLE IF NOT EXISTS stores (
            id int(10) NOT NULL AUTO_INCREMENT,
            name varchar(100) NOT NULL,
            PRIMARY KEY (id))""")

    def create_product_store(self):
        """Creates the table product_store"""
        self.dbconnection.query(
            """CREATE TABLE IF NOT EXISTS product_store (
            product_id bigint(20) NOT NULL REFERENCES products(id),
            store_id int(10) NOT NULL REFERENCES stores(id))""")

    def create_favorites(self):
        """Creates the table favorites"""
        self.dbconnection.query(
            """CREATE TABLE IF NOT EXISTS favorites (
            product_id bigint(20) NOT NULL REFERENCES products(id),
            substitute_id bigint(20) NOT NULL REFERENCES products(id),
            PRIMARY KEY (product_id))""")


def main():
    """Instantiates Dbinstaller and starts tables creation"""
    dbinst = Dbinstaller()
    dbinst.create_products()
    dbinst.create_stores()
    dbinst.create_product_store()
    dbinst.create_favorites()


if __name__ == '__main__':
    main()
