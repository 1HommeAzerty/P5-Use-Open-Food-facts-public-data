#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8

import json

from products import Products


class Installer:
    """---"""
    def __init__(self):

        self.prod = Products()

    def get_stores(self):
        response = self.prod.get_stores_from_api()
        return response

    def get_products(self, categories, number=1000):
        with open("config.txt", "r") as cfile:
            categories = [cat.strip() for cat in cfile.read().split(",")]
        products_list = []
        for category in categories:
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
        data = self.get_stores()
        #print(data['tags']['id'])
        for dt in data['tags']:
            if dt['products'] >= 10:
                self.prod.fill_stores(dt['name'])
                print('Table Stores remplie')
            else:
                pass

    def fill_products(self):
        products = self.get_products("config.txt", 1000)

        for product in products:
            if 'stores' in product and product['stores'] != "":
                if 'nutrition_grade_fr' in product:
                    if product['nutrition_grade_fr'] != "":
                        self.prod.fill_products(product)

                        for store in product['stores_tags']:
                            store_id = self.prod.get_store_id(store)

                            if len(store_id):
                                # print(product['product_name'],store, store_id)
                                self.prod.fill_products_stores(
                                    store_id[0]['id'], product)
            else:
                pass


def main():
    """---"""
    inst = Installer()
    inst.fill_stores()
    inst.fill_products()


if __name__ == '__main__':
    main()
