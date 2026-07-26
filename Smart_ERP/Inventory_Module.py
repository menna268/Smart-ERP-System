import json
import os
class Product:
    def __init__(self, product_id, name, price, quantity, low_stock_limit):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.low_stock_limit = low_stock_limit

    def dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "low_stock_limit": self.low_stock_limit
        }

class Inventory:
    def __init__(self, file_p="product.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.file_p = os.path.join(base_dir, file_p)

        self.products = []

        self.load_products()

    def load_products(self):

        self.products = []
        print(self.file_p)

        try:

            print("Reading from:", self.file_p)

            with open(self.file_p, "r") as file:
                products_data = json.load(file)

            print("JSON =", products_data)

            for prod in products_data:
                product = Product(
                    prod["product_id"],
                    prod["name"],
                    prod["price"],
                    prod["quantity"],
                    prod["low_stock_limit"]
                )

                self.products.append(product)

            print("Loaded =", len(self.products))

        except Exception as e:
            print("ERROR:", e)

    def save_products(self):
        data = []

        for product in self.products:
            data.append(product.dict())

        with open(self.file_p, "w") as file:
            json.dump(data, file, indent=4)

    # add product
    def add_product(self, name, price, quantity, low_stock_limit):

        if len(self.products) > 0:
            last_product = self.products[-1]
            new_id = last_product.product_id + 1
        else:
            new_id = 1

        new_product = Product(
            new_id,
            name,
            price,
            quantity,
            low_stock_limit
        )

        self.products.append(new_product)
        self.save_products()

        print("ADD PRODUCT SUCCESSFULLY!")

    # delete product
    def delete_product(self, product_id):

        for product in self.products:
            if product.product_id == product_id:

                self.products.remove(product)
                self.save_products()

                print("DONE DELETE PRODUCT")
                return

        print("PRODUCT NOT FOUND")

    def check_product(self , product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    # update product
    def update_product(self, product_id, new_name, new_price, new_quantity, new_limit):

        for product in self.products:
            if product.product_id == product_id:

                product.name = new_name
                product.price = new_price
                product.quantity = new_quantity
                product.low_stock_limit = new_limit

                self.save_products()

                print("DONE UPDATED PRODUCT")
                return

        print("PRODUCT NOT FOUND")

    # search product
    def search_product(self, key):

        result = []

        for product in self.products:
            if key.lower() in product.name.lower() or str(key) == str(product.product_id):
                result.append(product)

        return result

    # low stock
    def low_stock(self):

        warning = []

        for product in self.products:
            if product.quantity <= product.low_stock_limit:
                warning.append(product)

        return warning