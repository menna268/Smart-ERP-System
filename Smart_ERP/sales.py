import json
from datetime import datetime

class sale:
    def __init__(self, products, file_p="product.json"):
        self.products = products
        self.file_p = file_p
        self.total = 0
        self.result = []
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Search Product
    def search_product(self, name):
        for x in self.products:
            if str(name).lower() in x.name.lower() or str(name).lower() == str(x.product_id):
                return x
        return None

    # Add Product
    def add_product(self, product, quantity):
        if product.quantity >= quantity:
            total_price = product.price * quantity
            self.total += total_price

            self.result.append({
                "product_id": product.product_id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
                "total price": total_price
            })

            product.quantity -= quantity

            print("product added successfully")

        else:
            print("Not enough stock")

    # Update inventory
    def save_products(self):
        data = []

        for n in self.products:
            data.append(n.dict())

        with open(self.file_p, "w") as file:
            json.dump(data, file, indent=4)

    # Send sale data to invoice
    def get_sale_data(self):

        return {
            "date": self.date,
            "products": self.result,
            "total_price": self.total
        }


class invoice:
    def __init__(self, invoice_id, sales):

        self.invoice_id = invoice_id
        self.sales = sales
        self.date = sales.date

    def print_invoice(self):
        print("******** Invoice ********")
        print(f"Invoice ID: {self.invoice_id}")
        print(f"Date: {self.date}")

        print("------------------------")

        for item in self.sales.result:
            print(f"Product: {item['name']}")
            print(f"Quantity: {item['quantity']}")
            print(f"Price: {item['price']}")
            print(f"Total: {item['total price']}")

            print("------------------------")

        print(f"Total Price: {self.sales.total}")

    def save_invoice(self, file_name="sales.json"):

        invoice_data = {
            "invoice_id": self.invoice_id,
            "sale": self.sales.get_sale_data()
        }

        try:
            with open(file_name, "r") as file:
                sales = json.load(file)

        except FileNotFoundError:
            sales = []

        sales.append(invoice_data)
        with open(file_name, "w") as file:
            json.dump(sales, file, indent=4)