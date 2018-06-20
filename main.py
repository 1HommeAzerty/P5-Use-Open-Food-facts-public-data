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
        
        if 0 <= choice < len(categories) :
            self.display_products_de(choices[choice])
        elif choice == len(categories):
            self.display_favorites()
        else:
            self.quit()      

    def input(self, elements, message):
        """---"""
        while True:
            for i, element in enumerate(elements):
                print(i+1, element)
            choice = input(message)
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= i+1:
                    return choice-1


    def display_products_de(self, category):
        productsde = self.prod.get_DE_products_by_category(category)
        productchoices = [f"{product['name'].decode('utf-8')} ({product['nutriscore'].decode('utf-8')})" for product in productsde.all(as_dict = True)] 
        choices = productchoices + ["consulter les favoris", "quitter"]
        choice = self.input(choices, "Quel est votre choix ? ")

        if 0 <= choice < len(productsde) :
            self.display_products_abc(category, productsde[choice]['id'])
        elif choice == len(productsde):
            self.display_favorites()
        else:
            self.quit()

    def display_products_abc(self, category, productid):
        productsabc = self.prod.get_ABC_products_by_category(category)
        productchoices = [f"{product['name'].decode('utf-8')} ({product['nutriscore'].decode('utf-8')})" for product in productsabc.all(as_dict = True)]
        choices = productchoices + ["consulter les favoris", "quitter"]
        choice = self.input(choices, "Quel est votre choix ? ")
        
        if 0 <= choice < len(productsabc) :
            self.display_product(productid, productsabc[choice]['id'])
        elif choice == len(productsabc):
            self.display_favorites()
        else:
            self.quit()


    def display_product(self, productid, substituteid):
        """---"""
        stores = self.prod.get_stores_products()

        products = self.prod.get_product(substituteid)
        for product in products:
            print(f'{product["name"].decode("utf-8")}\n',
            f'Nutriscore: {product["nutriscore"].decode("utf-8")}\n',
            f'URL: {product["url"].decode("utf-8")}\n',
            'Barcode: ', product['id'])

            for store in stores:
                if store["product_id"] == product["id"]:
                    print(f'Magasin: {store["name"].decode("utf-8")}\n')
    

    def display_favorites(self):
        pass
    def quit(self):
        pass

def main():
    """---"""
    inst = Main()
    inst.start('config.txt')


if __name__ == '__main__':
    main()
