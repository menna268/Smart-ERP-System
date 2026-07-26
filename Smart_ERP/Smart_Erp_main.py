import json
from User_Management import AuthManager
from Inventory_Module import Inventory
from sales import sale, invoice
from dashboard import Dashboard, Statistics, Profit, Report

auth = AuthManager()
print("=" * 40)
print("          SMART ERP LOGIN")
print("=" * 40)
username = input("Username: ")
password = input("Password: ")

current_user = auth.login(username, password)

if current_user is None:
    print("Invalid username or password.")

else:
    print(f"\nWelcome {current_user.get_username()}!")
    print(f"Role: {current_user.role}")

    inventory = Inventory()

    try:
        with open("sales.json", "r") as file:
            sales_data = json.load(file)
    except FileNotFoundError:
        sales_data = []

    employees = []

    for user in auth.users.values():
        if user.role == "Employee":
            employees.append(user)

    while True:
        print("\n")
        print("=" * 40)
        print("             MAIN MENU")
        print("=" * 40)

        if current_user.role in ["Admin", "Manager"]:
            print("1. Dashboard")
            print("2. Inventory")
            print("3. Sales")
            print("4. Reports")
            print("5. Add Employee")
            print("6. Logout")

        elif current_user.role == "Employee":
            print("1. Inventory")
            print("2. Sales")
            print("3. Logout")

        choice = input("Choose: ")

        # Dashboard Admin and Manager
        if current_user.role in ["Admin", "Manager"] and choice == "1":

            statistics = Statistics(inventory.products, sales_data, employees)
            profit = Profit(sales_data)

            report = Report(profit, statistics, sales_data, inventory.products, employees)
            dashboard = Dashboard(statistics, profit, report)
            dashboard.show_dashboard()

            dashboard_choice = int(input("Choose: "))
            dashboard.show_menu(dashboard_choice)

        # Inventory Admin and Manager
        elif current_user.role in ["Admin", "Manager"] and choice == "2":

            while True:
                print("\n===== INVENTORY =====")

                if current_user.role == "Admin":
                    print("1. Add Product")
                    print("2. Delete Product")
                    print("3. Update Product")
                    print("4. Search Product")
                    print("5. Low Stock")
                    print("6. Back")

                elif current_user.role == "Manager":
                    print("1. Search Product")
                    print("2. Low Stock")
                    print("3. Back")

                inventory_choice = input("Choose: ")

                # Admin Inventory
                if current_user.role == "Admin":

                    if inventory_choice == "1":
                        name = input("Product Name: ")
                        price = float(input("Price: "))
                        quantity = int(input("Quantity: "))
                        limit = int(input("Low Stock Limit: "))

                        inventory.add_product(name, price, quantity, limit)

                    elif inventory_choice == "2":
                        product_id = int(input("Product ID: "))
                        inventory.delete_product(product_id)

                    elif inventory_choice == "3":
                        product_id = int(input("Product ID: "))
                        check_id = inventory.check_product(product_id)
                        if check_id is None:
                            print("Product Not Found!")
                        else:
                            name = input("New Name: ")
                            price = float(input("New Price: "))
                            quantity = int(input("New Quantity: "))
                            limit = int(input("New Low Stock Limit: "))

                            inventory.update_product(product_id, name, price, quantity, limit)

                    elif inventory_choice == "4":
                        key = input("Search: ")
                        result = inventory.search_product(key)

                        if len(result) == 0:
                            print("Product not found.")
                        else:
                            for product in result:
                                print(product.dict())

                    elif inventory_choice == "5":
                        result = inventory.low_stock()

                        for product in result:
                            print(product.dict())

                    elif inventory_choice == "6":
                        break

                    else:
                        print("Invalid choice.")

                # Manager Inventory
                elif current_user.role == "Manager":

                    if inventory_choice == "1":
                        key = input("Search: ")
                        result = inventory.search_product(key)

                        if len(result) == 0:
                            print("Product not found.")
                        else:
                            for product in result:
                                print(product.dict())

                    elif inventory_choice == "2":
                        result = inventory.low_stock()

                        for product in result:
                            print(product.dict())

                    elif inventory_choice == "3":
                        break

                    else:
                        print("Invalid choice.")

        # Employee Inventory
        elif current_user.role == "Employee" and choice == "1":

            while True:
                print("\n===== INVENTORY =====")
                print("1. Search Product")
                print("2. Back")

                inventory_choice = input("Choose: ")

                if inventory_choice == "1":
                    key = input("Search: ")
                    result = inventory.search_product(key)

                    if len(result) == 0:
                        print("Product not found.")
                    else:
                        for product in result:
                            print(product.dict())

                elif inventory_choice == "2":
                    break

                else:
                    print("Invalid choice.")

        # Sales Admin, Manager and Employee
        elif (current_user.role in ["Admin", "Manager"] and choice == "3") or (current_user.role == "Employee" and choice == "2"):

            new_sale = sale(inventory.products)
            print("\n===== NEW SALE =====")

            while True:
                product_name = input("Enter product name or ID (or done): ")

                if product_name.lower() == "done":
                    break

                product = new_sale.search_product(product_name)

                if product is None:
                    print("Product not found.")
                    continue

                quantity = int(input("Quantity: "))
                new_sale.add_product(product, quantity)

            if len(new_sale.result) > 0:
                new_sale.save_products()

                invoice_id = len(sales_data) + 1
                new_invoice = invoice(invoice_id, new_sale)

                new_invoice.print_invoice()
                new_invoice.save_invoice()

                with open("sales.json", "r") as file:
                    sales_data = json.load(file)

            else:
                print("No products added.")

        # Reports Admin and Manager
        elif current_user.role in ["Admin", "Manager"] and choice == "4":

            statistics = Statistics(inventory.products, sales_data, employees)
            profit = Profit(sales_data)

            report = Report(profit, statistics, sales_data, inventory.products, employees)
            report.show_report()

        #Add User
        elif current_user.role in ["Admin", "Manager"] and choice == "5":

            print("\n===== ADD USER =====")

            username = input("Username: ")
            password = input("Password: ")

            if current_user.role == "Admin":
                role = input("Role (Admin / Manager / Employee): ").strip().capitalize()

            else:
                role = "Employee"

            auth.add_user(username, password, role)

        # Logout Admin and Manager
        elif current_user.role in ["Admin", "Manager"] and choice == "6":

            print("Logged out successfully.")
            break

        # Logout Employee
        elif current_user.role == "Employee" and choice == "3":

            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")