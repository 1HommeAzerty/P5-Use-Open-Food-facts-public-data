#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8

from products import Products


class Main:
    def __init__(self):
        self.prod = Products()

    def start(self, config):
        with open(config, "r") as cfile:
            categories = [cat.strip() for cat in cfile.read().split(",")]
        choices = categories + ["Consulter les favoris", "Quitter"]
        choice = self.input(choices, "Quel est votre choix ? ")

        if 0 <= choice < len(categories):
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
        productsde = self.prod.get_de_products_by_category(category)
        productchoices = [
            f"""{product['name']
            .decode('utf-8')} ({product['nutriscore']
            .decode('utf-8')})"""
            for product in productsde.all(as_dict=True)]

        choices = productchoices + [
            "Consulter les favoris",
            "Obtenir une nouvelle liste",
            "Menu principal",
            "Quitter"]
        choice = self.input(choices, "Quel est votre choix ? ")

        if 0 <= choice < len(productsde):
            self.display_products_abc(category, productsde[choice]['id'])
        elif choice == len(productsde):
            self.display_favorites()
        elif choice == (len(productsde)+1):
            self.display_products_de(category)
        elif choice == (len(productsde)+2):
            self.start("config.txt")
        else:
            self.quit()

    def display_products_abc(self, category, productid):
        productsabc = self.prod.get_abc_products_by_category(category)
        productchoices = [
            f"""{product['name']
            .decode('utf-8')} ({product['nutriscore']
            .decode('utf-8')})"""
            for product in productsabc.all(as_dict=True)]
        choices = productchoices + [
            "Consulter les favoris",
            "Obtenir une nouvelle liste",
            "Menu principal",
            "Quitter"]
        choice = self.input(choices, "Quel est votre choix ? ")

        if 0 <= choice < len(productsabc):
            self.display_product(productid, productsabc[choice]['id'])
        elif choice == len(productsabc):
            self.display_favorites()
        elif choice == (len(productsabc)+1):
            self.display_products_abc(category, productid)
        elif choice == (len(productsabc)+2):
            self.start("config.txt")
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
        choices = ["Ajouter aux favoris", "Consulter les favoris", "Quitter"]
        choice = self.input(choices, "Quel est votre choix ? ")

        if choice == 0:
            self.prod.fill_favorites(productid, substituteid)

            self.start("config.txt")
        else:
            self.quit()

    def display_favorites(self):
        favorites = self.prod.get_favorites()
        stores = self.prod.get_stores_products()
        for favorite in favorites:

            print(f'{favorite["name"].decode("utf-8")}\n',
                  f'Nutriscore: {favorite["nutriscore"].decode("utf-8")}\n',
                  f'{favorite["sname"].decode("utf-8")}\n',
                  f'Nutriscore: {favorite["sscore"].decode("utf-8")}\n'
                  f'URL: {favorite["surl"].decode("utf-8")}\n',
                  'Barcode: ', favorite['sid'])
            for store in stores:
                if store["product_id"] == favorite["sid"]:
                    print(f'Magasin: {store["name"].decode("utf-8")}\n')
        choices = ["Menu principal", "Quitter"]
        choice = self.input(choices, "Quel est votre choix ? ")

        if choice == 0:
            self.start("config.txt")
        else:
            self.quit()

    def quit(self):
        pass


def main():
    """---"""
    inst = Main()
    inst.start('config.txt')

if __name__ == '__main__':
    main()
