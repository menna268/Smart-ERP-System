# Dashboard Class

class Dashboard:

    def __init__(self, statistics, profit, report):

        self.statistics = statistics
        self.profit = profit
        self.report = report


    def get_dashboard_data(self):

        return {

            "total_products": self.statistics.get_total_product(),

            "total_sales": self.statistics.get_total_sale(),

            "total_employees": self.statistics.get_total_employee(),

            "profit": self.profit.calculate_profit()

        }


# Statistics Class

class Statistics:

    def __init__(self, t_product, t_sale, t_employee):

        self.t_product = t_product
        self.t_sale = t_sale
        self.t_employee = t_employee


    def get_total_product(self):

        return len(self.t_product)



    def get_total_sale(self):

        return len(self.t_sale)



    def get_total_employee(self):

        return len(self.t_employee)



# Profit Class

class Profit:

    def __init__(self, sale):

        self.sale = sale



    def calculate_profit(self):

        total = 0

        for sale_data in self.sale:

            total += sale_data["sale"]["total_price"]


        return total




# Report Class

class Report:


    def __init__(self, profit, statistics, sales, products, employees):

        self.profit = profit
        self.statistics = statistics
        self.sales = sales
        self.products = products
        self.employees = employees



    # Summary Report

    def summary_report(self):

        return {

            "total_products":
                self.statistics.get_total_product(),


            "total_sales":
                self.statistics.get_total_sale(),


            "total_employees":
                self.statistics.get_total_employee(),


            "profit":
                self.profit.calculate_profit()

        }




    # Sales Report

    def report_sale(self):

        sales_report = []


        for sale_data in self.sales:

            sales_report.append({

                "invoice_id":
                    sale_data["invoice_id"],


                "date":
                    sale_data["sale"]["date"],


                "total_price":
                    sale_data["sale"]["total_price"]

            })


        return sales_report





    # Employee Report

    def employee_report(self):

        employee_report = []


        for emp in self.employees:

            employee_report.append({

                "name":
                    emp.get_username(),


                "position":
                    emp.role,


                "salary":
                    emp.user_id

            })


        return employee_report