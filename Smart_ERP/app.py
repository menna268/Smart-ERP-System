from dashboard import Statistics, Profit, Report
from Inventory_Module import Inventory
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from User_Management import AuthManager, User
from flask import jsonify
from functools import wraps


app = Flask(__name__)
app.secret_key = "smart_erp_secret"


auth = AuthManager()

inventory_manager = Inventory()


# Load Employees

employees = []

for user in auth.users.values():

    if user.role == "Employee":

        employees.append(user)



# Load Sales

import os

base_dir = os.path.dirname(os.path.abspath(__file__))

sales_file = os.path.join(base_dir, "sales.json")


try:

    with open(sales_file, "r") as file:

        sales_data = json.load(file)


    print("Sales Loaded =", len(sales_data))


except Exception as e:

    print("Sales Error:", e)

    sales_data = []



# Create Statistics Object

statistics = Statistics(

    inventory_manager.products,

    sales_data,

    employees

)



# Create Profit Object

profit = Profit(

    sales_data

)



# Create Report Object

report_manager = Report(

    profit,

    statistics,

    sales_data,

    inventory_manager.products,

    employees

)



print("Employees =", len(employees))

print("Sales =", len(sales_data))

print("Products =", len(inventory_manager.products))


# =========================
# LOGIN
# =========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = auth.login(username, password)


        if user:

            session["username"] = user.get_username()
            session["role"] = user.role

            return redirect(url_for("dashboard"))


        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )


    return render_template("login.html")



# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))


    # Employee is not allowed to access Dashboard
    if session["role"] == "Employee":
        return redirect(url_for("sales"))



    statistics = Statistics(
        inventory_manager.products,
        sales_data,
        employees
    )


    profit = Profit(sales_data)



    return render_template(

        "dashboard.html",

        username=session["username"],

        role=session["role"],


        total_products=statistics.get_total_product(),

        total_sales=statistics.get_total_sale(),

        total_employees=statistics.get_total_employee(),


        total_revenue=profit.calculate_profit(),


        recent_sales=sales_data[-5:]

    )

# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "username" not in session:
            return redirect(url_for("login"))

        if session["role"] != "Admin":
            return redirect(url_for("inventory"))

        return function(*args, **kwargs)

    return wrapper

# =========================
# INVENTORY
# =========================

@app.route("/inventory")
def inventory():

    if "username" not in session:
        return redirect(url_for("login"))


    search = request.args.get("search")


    if search:

        products = inventory_manager.search_product(search)

    else:

        products = inventory_manager.products



    return render_template(

        "inventory.html",

        products=products,

        role=session["role"]

    )



# =========================
# ADD PRODUCT
# =========================

@app.route("/add_product", methods=["POST"])
@admin_required
def add_product():

    name = request.form["name"]

    price = float(request.form["price"])

    quantity = int(request.form["quantity"])

    limit = int(request.form["low_stock_limit"])


    inventory_manager.add_product(
        name,
        price,
        quantity,
        limit
    )


    return redirect(url_for("inventory"))



# =========================
# DELETE PRODUCT
# =========================

@app.route("/delete_product/<int:product_id>")
@admin_required
def delete_product(product_id):
        inventory_manager.delete_product(product_id)

        return redirect(url_for("inventory"))



# =========================
# EDIT PRODUCT
# =========================

@app.route("/update_product/<int:product_id>", methods=["POST"])
@admin_required
def update_product(product_id):

    name = request.form["name"]

    price = float(request.form["price"])

    quantity = int(request.form["quantity"])

    limit = int(request.form["low_stock_limit"])


    inventory_manager.update_product(
        product_id,
        name,
        price,
        quantity,
        limit
    )


    return redirect(url_for("inventory"))

@app.route("/sales")
def sales():

    if "username" not in session:
        return redirect(url_for("login"))

    invoice = session.pop("last_invoice", None)

    return render_template(
        "sales.html",
        sales=sales_data,
        products=inventory_manager.products,
        role=session["role"],
        total_sales=len(sales_data),
        total_revenue=sum(s["sale"]["total_price"] for s in sales_data),
        today_sales=len(sales_data),
        customers=len(sales_data),
        invoice=invoice
    )
@app.route("/add_sale", methods=["POST"])
def add_sale():

    if "username" not in session:
        return redirect(url_for("login"))

    product_id = int(request.form["product_id"])
    quantity = int(request.form["quantity"])

    product = inventory_manager.check_product(product_id)

    if product is None:
        return redirect(url_for("sales"))

    if quantity > product.quantity:
        return redirect(url_for("sales"))


    product.quantity -= quantity
    inventory_manager.save_products()


    invoice = {

        "invoice_id": len(sales_data) + 1,

        "sale": {

            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "products": [

                {
                    "product_id": product.product_id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": quantity,
                    "total price": product.price * quantity
                }

            ],

            "total_price": product.price * quantity

        }

    }

    sales_data.append(invoice)
    session["last_invoice"] = invoice

    with open("sales.json", "w") as file:
        json.dump(sales_data, file, indent=4)

    return redirect(url_for("sales"))

@app.route("/reports")
def reports():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "reports.html",
        role=session["role"]
    )
@app.route("/generate_report/<report_type>")
def generate_report(report_type):

    if report_type == "summary":

        report = report_manager.summary_report()

    elif report_type == "sales":

        report = report_manager.report_sale()

    elif report_type == "employee":

        report = report_manager.employee_report()

    else:

        report = "Report not found"


    return jsonify({
        "report": report
    })
@app.route("/add_user", methods=["POST"])
def add_user():

    if "username" not in session:
        return redirect(url_for("login"))


    if session["role"] != "Manager":

        return redirect(url_for("dashboard"))



    username = request.form["username"]

    password = request.form["password"]

    role = request.form["role"]



    user_id = len(auth.users) + 1



    new_user = User(
        username,
        password,
        user_id,
        role
    )

    auth.users[username] = new_user

    if role == "Employee":
        employees.append(new_user)
    if username in auth.users:
        return redirect(url_for("dashboard"))

    auth.save_users()

    return redirect(url_for("dashboard"))
if __name__ == "__main__":

    app.run(debug=True)