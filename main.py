#! F:\OC_tp\Python\P5\env\Scripts\python
# coding: utf-8


"""This module is the main interaface, it allows the user to
interact with the db and choose their products.
"""

from products import ProductsManager


class Main:
    """Gets infos from the database and allows the user to choose
    products and save it to their favorites.
    """

    def __init__(self):
        """Creates an instance of ProductsManager to
        get access to the requests to the database.
        """
        self.prod = ProductsManager()

    def start(self, config):
        """Allows the user to choose a category or display favorites.
        Returns a list of products from the chosen category with D or E
        Nutirscore.
        """
        with open(config, "r") as cfile:
            categories = [cat.strip() for cat in cfile.read().split(",")]
        choices = categories + ["Consulter les favoris", "Quitter"]
        choice = self.input(choices, "\n Quel est votre choix ? ")

        if 0 <= choice < len(categories):
            self.display_products_de(choices[choice])
        elif choice == len(categories):
            self.display_favorites()
        else:
            self.quit()

    def input(self, elements, message):
        """Initiates the loop and gets user's input"""
        while True:
            for i, element in enumerate(elements):
                print(i+1, element)
            choice = input(message)
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= i+1:
                    return choice-1

    def display_products_de(self, category):
        """Displays a random list of products with D or E nutriscore
        from the category chosen by the user.
        The user can choose to get a new list or choose a product
        to replace.
        """
        productsde = self.prod.get_de_products_by_category(category)
        productchoices = [
            f"""{product['name']} ({product['nutriscore']})"""
            for product in productsde]

        choices = productchoices + [
            "Consulter les favoris",
            "Obtenir une nouvelle liste",
            "Menu principal",
            "Quitter"]
        choice = self.input(choices, "\n Quel est votre choix ? ")

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
        """Displays a random list of products with A, B or C nutriscore
        from the category chosen by the user.
        The user can choose to get a new list of products.
        """
        productsabc = self.prod.get_abc_products_by_category(category)
        productchoices = [
            f"""{product['name']} ({product['nutriscore']})"""
            for product in productsabc]
        choices = productchoices + [
            "Consulter les favoris",
            "Obtenir une nouvelle liste",
            "Menu principal",
            "Quitter"]
        choice = self.input(choices, "\n Quel est votre choix ? ")

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
        """Displays details about the product selected.
        The user has the choice to add it to the favorites table.
        """
        stores = self.prod.get_stores_products()
        products = self.prod.get_product(substituteid)

        for product in products:
            print(f'{product["name"]}\n',
                  f'Nutriscore: {product["nutriscore"]}\n',
                  f'URL: {product["url"]}\n',
                  'Barcode: ', product['id'])
            for store in stores:
                if store["product_id"] == product["id"]:
                    print(f'Magasin: {store["name"]}\n')
        choices = [
            "Ajouter aux favoris",
            "Consulter les favoris",
            "Menu principal",
            "Quitter"]
        choice = self.input(choices, "\n Quel est votre choix ? ")

        if choice == 0:
            self.prod.fill_favorites(productid, substituteid)
            self.start("config.txt")
        elif choice == 1:
            self.display_favorites()
        elif choice == 2:
            self.start("config.txt")
        else:
            self.quit()

    def display_favorites(self):
        """Displays the products entered previously as favorites
        in the database.
        """
        favorites = self.prod.get_favorites()
        stores = self.prod.get_stores_products()

        for favorite in favorites:
            print(f'{favorite["name"]}\n',
                  f'Nutriscore: {favorite["nutriscore"]}\n',
                  f'{favorite["sname"]}\n',
                  f'Nutriscore: {favorite["sscore"]}\n'
                  f'URL: {favorite["surl"]}\n',
                  'Barcode: ', favorite['sid'])
            for store in stores:
                if store["product_id"] == favorite["sid"]:
                    print(f'Magasin: {store["name"]}\n')
        choices = ["Menu principal", "Quitter"]
        choice = self.input(choices, "\n Quel est votre choix ? ")

        if choice == 0:
            self.start("config.txt")
        else:
            self.quit()

    def quit(self):
        """Ends the loop and quits the program"""
        pass


def main():
    """Instantiates the class and starts the loop"""
    inst = Main()
    inst.start('config.txt')


if __name__ == '__main__':
    main()
