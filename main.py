#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8

from products import Products



class Main:
    def __init__(self):
        self.prod = Products()


    def start(self, config):
        with open(config, "r") as cfile:
            categories = [cat.strip() for cat in cfile.read().split(",")]
        choices = categories + ["consulter les favoris", "quitter"]
        choice = self.input(choices, "Quel est votre choix ? ")
        self.display_products_de(choice)

    def input(self, elements, message):

        while True:
            for i, element in enumerate(elements):
                print(i+1, element)
            choice = input(message)
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice < i:
                    return elements[choice-1]

    def display_products_de(self, category):
        productsde = self.prod.get_DE_products_by_category(category)
        productsde = [f"{product['name'].decode('utf-8')} ({product['nutriscore'].decode('utf-8')})" for product in productsde.all(as_dict = True)] 
        choices = productsde + ["consulter les favoris", "quitter"]
        choice = self.input(choices, "Quel est votre choix ? ")
        print(choice)

    def display_products_abc(self):
        productsabc = self.productsabc

        for product in productsabc:
            print(f'{product["name"].decode("utf-8")}\n',
                f'Nutriscore: {product["nutriscore"].decode("utf-8")}\n')


    def display_product(self):
        """---"""
        stores = self.stores

        products = self.products
        for product in products:
            print(f'{product["name"].decode("utf-8")}\n',
            f'Nutriscore: {product["nutriscore"].decode("utf-8")}\n',
            f'URL: {product["url"].decode("utf-8")}\n',
            'Barcode: ', product['id'])

            for store in stores:
                if store["product_id"] == product["id"]:
                    print(f'{store["product_id"]}\n',
                        f'Magasin: {store["name"].decode("utf-8")}\n')
    
    def display_stores(self):
        """---"""
        stores = self.stores
        for store in stores:
            print(f'{store["product_id"]}\n',
                f'Magasin: {store["name"].decode("utf-8")}\n')

def main():
    """---"""
    inst = Main()
    inst.start('config.txt')
    #inst.display_product()
    #inst.display_stores()
    #inst.display_products_de()
    #inst.display_products_abc()


if __name__ == '__main__':
    main()







#def select():
#   user_search = ""
#   while user_search == "":
#        .