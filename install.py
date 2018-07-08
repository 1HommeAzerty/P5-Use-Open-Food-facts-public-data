#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8


"""This module gets the data from the API and fills the database"""

from products import ProductsManager


class Installer:
    """Gets the data from the API and fills the database."""

    def __init__(self):
        """Creates an instance of the ProductsManager class to
        get access to the requests to the API and database.
        """
        self.prod = ProductsManager()

    def get_products(self, categories, number=1000):
        """Gets list of products from the API
        for the categories in config.txt.
        """
        with open("config.txt", "r") as cfile:
            # Gets the categories from the config file
            categories = [cat.strip() for cat in cfile.read().split(",")]
        products_list = []
        for category in categories:
            # For each category, criteria completes the url in the API request.
            criteria = {
                'action': 'process',
                'json': 1,
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': category,
                'page_size': number}
            products = self.prod.get_products_from_api(criteria)

            for product in products:
                product['category'] = category
                products_list.append(product)
        return products_list

    def fill_stores(self):
        """Get a list of stores from the API.
        Fills the stores table with that list.
        """
        stores = self.prod.get_stores_from_api()
        for store in stores['tags']:
            # Checks if the store has more than 10 products in db.
            if store['products'] >= 10:
                self.prod.fill_stores(store['name'])
                print(store['name'])
            else:
                pass

    def fill_products(self):
        """Gets the list of products from get_products()
        Fills the products and product_store tables.
        """
        products = self.get_products("config.txt", 1000)

        for product in products:
            # Checks if the product data has stores.
            if 'stores' in product and product['stores'] != "":
                # Checks if the product data has a nutrition grade.
                if 'nutrition_grade_fr' in product:
                    if product['nutrition_grade_fr'] != "":
                        self.prod.fill_products(product)

                        for store in product['stores_tags']:
                            store_id = self.prod.get_store_id(store)

                            if len(store_id):
                                print(product['product_name'])
                                self.prod.fill_products_stores(
                                    store_id[0]['id'], product)
            else:
                pass


def main():
    """Instantiates Installer and starts filling the tables"""
    inst = Installer()
    inst.fill_stores()
    inst.fill_products()


if __name__ == '__main__':
    main()
