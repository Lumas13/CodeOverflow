# ACCOUNT MANAGEMENT IMPORT
from models.auth.authforms import SignupForm, LoginForm, UpdateProfileForm, ChangePasswordForm, CreateCreditCardForm
from models.auth.user import User
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import time
import calendar
from PIL import Image
import secrets
# TRANSACTION PROCESSING INNIT
from Forms import CreateInventoryForm
import Inventory, Cart, Sales, Card
# GRAPH STUFF
import pandas as pd
import json
import plotly
import plotly.graph_objects as go
# CUSTOMER SUPPORT STUFF
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from Forms import CreateFeedbackForm, CreateReportForm
import shelve, FeedbackForm, ReportForm
from chat import get_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hyenen_kekrb'
login_manager = LoginManager()
login_manager.init_app(app)

app.config['UPLOAD_FOLDER'] = '/static/Images/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['SESSION_TYPE'] = 'filesystem'

# test



# ACCOUNT MANAGEMENT INNIT
# Load the database of user into login_manager
@login_manager.user_loader
def load_user(user_id):
    db = shelve.open("db/customer/users")
    user_dict = {}
    user_dict = db['customer']
    db.close()
    for objects in user_dict.values():
        if objects.get_id() == user_id:
            return objects


# Direct to home
@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutus.html')


# Gets the user data from the signup form and enter it into the user_dict database
@app.route("/Signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()
    if request.method == "POST":
        # Retrieve the user data from the signup form
        username = signup_form.username.data
        email = signup_form.email.data
        password = signup_form.password1.data
        password2 = signup_form.password2.data
        current_gmt = time.gmtime()
        id = calendar.timegm(current_gmt)
        user_dict = {}
        error = 'none'
        try:
            db = shelve.open('db/customer/users')
            if 'customer' in db:
                user_dict = db['customer']
            else:
                db['customer'] = user_dict

            substring = '@staff'
            if substring in email:
                user = User(username, email, password, id)
                user.setrole('admin')
                user_dict[id] = user
                db['customer'] = user_dict
                db.close()
                return redirect(url_for('login'))

            # Check if username/email has been taken
            username_list = []
            email_list = []
            for objects in user_dict.values():
                username_list.append(objects.getusername())
                email_list.append(objects.getemail())
            if username in username_list and email in email_list:
                error = "Both username and email are already taken"
                return render_template('Signup.html', form=signup_form, error=error)
            elif email in email_list:
                error = "Email is already taken"
                return render_template('Signup.html', form=signup_form, error=error)
            elif username in username_list:
                error = "Username is already taken"
                return render_template('Signup.html', form=signup_form, error=error)
            elif password != password2:
                error = 'Password does not match'
                return render_template('Signup.html', form=signup_form, error=error)
            else:
                user = User(username, email, password, id)
                user.setrole('customer')
                user_dict[id] = user
                db['customer'] = user_dict
                db.close()
                return redirect(url_for('login'))
        except IOError:
            print("IO Error")
        except Exception as ex:
            print(f"Unknown error occurred as {ex}")
    return render_template('Signup.html', form=signup_form)


@app.route('/Login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        # Retrieve login data from login form
        username = login_form.username.data
        password = login_form.password.data

        db = shelve.open('db/customer/users', "c")
        user_dict = {}
        try:
            if 'customer' in db:
                user_dict = db['customer']
            else:
                db['customer'] = user_dict
        except Exception as ex:
            print(f"Unknown error occurred as {ex}")

        # Checks if current is admin role, if yes check if username is in db, if yes check if username matches password
        for user in user_dict.values():
            if user.getrole() == 'admin':
                if user.getusername() == username:
                    if user.getpassword() == password:
                        login_user(user)
                        flash(f"{user.getusername()} has logged in successfully")

                    print(user.getusername(), " has logged in")
                    return redirect(url_for("update"))

        # Checks if current is customer role, if yes check if username is in db, if yes check if username matches password
        for user in user_dict.values():
            if user.getrole() == 'customer':
                if user.getusername() == username:
                    if user.getpassword() == password:
                        login_user(user)
                        flash(f"{user.getusername()} has logged in successfully")

                    print(user.getusername(), " has logged in")
                    return redirect(url_for("home"))

    return render_template('Login.html', form=login_form)


# Log-outs the user
@app.route('/Logout', methods=['GET'])
def logout():
    try:
        print(current_user.getusername(), " has logged out.")
        flash("User has been logged out.")
        logout_user()
        return redirect(url_for('home'))
    except Exception as ex:
        print(f"Unknown error occurred as {ex}")


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    update_form = UpdateProfileForm()
    db2 = shelve.open('db/Card/card', 'c')
    card_dict = {}

    try:
        if 'Card' in db2:
            card_dict = db2['Card']
        else:
            db2['Card'] = card_dict
    except:
        print("Error in opening storage.db")
    db2.close()
    card_list = []
    for i in card_dict:
        card = card_dict.get(i)
        if card.get_user_id() == current_user.get_id():
            card_list.append(card)

    if request.method == "POST":
        db = shelve.open('db/customer/users')
        user_dict = {}
        user_dict = db['customer']

        for users in user_dict.values():
            if users.get_id() == current_user.get_id():
                users.setusername(update_form.username.data)
                users.setemail(update_form.email.data)
                users.setfirst_name(update_form.first_name.data)
                users.setlast_name(update_form.last_name.data)
                users.setphone_number(update_form.phone_number.data)
                users.setaddress(update_form.address.data)
                users.setcredit_number(update_form.credit_number.data)
                users.setcredit_cvv(update_form.credit_cvv.data)
                users.setcredit_date(update_form.credit_date.data)
                print(update_form.profile_picture.data)
                # Upload user profile picture
                if update_form.profile_picture.data:
                    image = Image.open(update_form.profile_picture.data)
                    random_hex = secrets.token_hex(8)
                    random_hex = "static/profilePicture/" + random_hex + ".jpg"
                    image.save(random_hex)
                    users.setprofile_picture(random_hex)

                db['customer'] = user_dict
                db.close()
                flash("Account updated.")
                return redirect(url_for("update"))
            else:
                print('error')
    else:
        update_form.username.data = current_user.getusername()
        update_form.email.data = current_user.getemail()
        update_form.first_name.data = current_user.getfirst_name()
        update_form.last_name.data = current_user.getlast_name()
        update_form.phone_number.data = current_user.getphone_number()
        update_form.address.data = current_user.getaddress()
        update_form.credit_number.data = current_user.getcredit_number()
        update_form.credit_cvv.data = current_user.getcredit_cvv()
        update_form.credit_date.data = current_user.getcredit_date()
        update_form.profile_picture.data = current_user.getprofile_picture()
    return render_template('updateprofile.html', form=update_form, card_list=card_list)


@app.route('/editPassword', methods=['GET', 'POST'])
def editPassword():
    change_password_form = ChangePasswordForm()
    if request.method == "POST":
        db = shelve.open('db/customer/users')
        user_dict = {}
        user_dict = db['customer']
        for users in user_dict.values():
            if users.get_id() == current_user.get_id():
                users.setpassword(change_password_form.password.data)
                db['customer'] = user_dict
                db.close()
            else:
                print('error')
    else:
        change_password_form.password.data = current_user.getpassword()
    return render_template('Account Management/editPassword.html', form=change_password_form)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        db = shelve.open('db/customer/users', 'w')
        user_dict = {}
        user_dict = db['customer']
        if 'customer' in db:
            user_dict = db['customer']
        else:
            db['customer'] = user_dict

        user_dict.pop(id)

        db['customer'] = user_dict
        db.close()
        return redirect(url_for('home'))
    except IOError:
        print("Error IO Error")
    except Exception as ex:
        print(f"unknown error occurred as {ex}")

    return render_template('home.html')


@app.route('/Staff', methods=['GET', 'POST'])
def staff():
    return render_template('Staffpage.html')


@app.route('/Management', methods=['GET', 'POST'])
def management():
    user_dict = {}
    db = shelve.open('db/customer/users', 'r')
    user_dict = db['customer']
    db.close()
    user_list = []

    for key in user_dict:
        user = user_dict.get(key)
        user_list.append(user)

    return render_template('customerAccounts.html', count=len(user_list), users_list=user_list)


@app.route('/Purchase', methods=['POST', 'GET'])
def purchaseHistory():
    sales_dict = {}
    db = shelve.open('db/Sales/sales.db', 'c')
    try:
        if 'Sales' in db:
            sales_dict = db['Sales']
        else:
            db['Sales'] = sales_dict
    except:
        print("Error in opening storage.db")
    db.close()
    sales_list = []

    # var1 = []
    # var2 = []
    for key in sales_dict:
        sales = sales_dict.get(key)
        sales_list.append(sales)

    return render_template('purchaseHistory.html', count=len(sales_list), sales_list=sales_list)


# TRANSACTION PROCESSING INNIT
@app.route('/<int:id>')
def productPage(id):
    inventory_dict = {}
    db = shelve.open('db/Inventory/inventory.db', 'r')
    inventory_dict = db['Inventory']
    db.close()

    inventory_product = []
    for key in inventory_dict:  # {1:object(lucas,3,4), 2:object(edwdq,5,6)
        if key == id:
            inventory = inventory_dict.get(key)
            inventory_product = inventory
        else:
            continue
    return render_template('productPage.html', inventory=inventory_product)


@app.route('/shop', methods=['POST', 'GET'])
def shop():
    count_search = 0
    search_list = 0
    inventory_dict = {}
    db = shelve.open('db/Inventory/inventory.db', 'c')
    try:
        if 'Inventory' in db:
            inventory_dict = db['Inventory']
        else:
            db['Inventory'] = inventory_dict
    except:
        print("Error in opeing storage.db")
    db.close()

    inventory_list = []  # {1:object(lucas,2,4), 2:object(weqdwq,4,5)
    for key in inventory_dict:
        inventory = inventory_dict.get(key)
        inventory_list.append(inventory)

    search = request.form.get("search")

    if search != None:
        search_list = []
        for i in inventory_dict.values():  # {1:apple, 2:banana}
            product_split = []
            search_split = []
            for letter in i.get_product_name().upper():
                product_split.append(letter)
            for letter in search.upper():
                search_split.append(letter)

            print(search_split) # B a n a n a
            print(product_split) # A p p l e #B a n a n a # B r o c o l i
            wordCount = 0
            searchWord = []
            productWord = []

            try:
                    for n,m in zip(search_split,product_split):
                        wordCount +=1
                        searchWord.append(n)
                        productWord.append(m)
            except:
                    continue
            finally:
                    if searchWord == productWord:
                        search_list.append(i)
                    else:
                        continue


            count_search = len(search_list)
    return render_template('shop.html', inventory_list=inventory_list, search_list=search_list,
                           count_search=count_search)


@app.route('/addCart/<int:id>', methods=["GET", "POST"])
def addCart(id):
    if request.method == "POST":
        inventory_dict = {}
        db = shelve.open('db/Inventory/inventory.db', 'r')
        inventory_dict = db['Inventory']  # {1: object-apple, desc,price  2: object-banana,desc}
        db.close()

        cart_dict = {}
        db2 = shelve.open('db/Cart/cart.db', 'c')

        print("added to cart")

        try:
            cart_dict = db2['Cart']
        except:
            print("Error in retieving Cart from cart.db")

        quantity = request.form.get("quantity")
        inventory_id = request.form.get("inventory.get_inventory_id()")
        inventory_product = inventory_dict[int(inventory_id)]
        print(inventory_product)
        print(cart_dict)

        added = False
        user_id_list = []
        product_list = {}
        cart_values = []
        for i in cart_dict.values():  # {1:testerbanana
            try:
                product_list[i.get_user_id()].append(i.get_product_name())
            except:
                product_list[i.get_user_id()] = [i.get_product_name()]

            user_id_list.append(i.get_user_id())
            cart_values.append(i)
            print(product_list)

        if current_user.get_id() not in user_id_list:
            cart = Cart.Cart(inventory_product.get_product_name(), inventory_product.get_product_desc(),
                             inventory_product.get_category(),
                             inventory_product.get_price(), inventory_product.get_discount(),
                             inventory_product.get_quantity(), inventory_product.get_product_image(), quantity,
                             current_user.get_id())
            added = True

        else:
            print(cart_dict.values())  #
            made = False
            for i in cart_dict.values():  # {1:testerbanana
                if i.get_user_id() == current_user.get_id():
                    if i.get_product_name() in product_list[i.get_user_id()]:
                        if inventory_product.get_product_name() == i.get_product_name():
                            i.set_quantity_bought(int(i.get_quantity_bought()) + int(quantity))
                            made = True
                            break
            if made == False:
                if inventory_product.get_product_name() not in product_list[current_user.get_id()]:
                    cart = Cart.Cart(inventory_product.get_product_name(), inventory_product.get_product_desc(),
                                     inventory_product.get_category(),
                                     inventory_product.get_price(), inventory_product.get_discount(),
                                     inventory_product.get_quantity(), inventory_product.get_product_image(), quantity,
                                     current_user.get_id())
                    added = True

        if added == True:
            for key in cart_dict:  # {1:bronze 6:silver 3: bronze}
                if key == cart.get_cart_id():
                    cart.set_cart_id(int(cart.get_cart_id()) + 1)
            cart_dict[cart.get_cart_id()] = cart
            # 1:bronze 2:silver 3:bronze 4:gold

        db2['Cart'] = cart_dict
        db2.close()
        flash(f"{inventory_product.get_product_name()} has been added to cart.")
        return redirect(url_for('shop', id=inventory_id))


@app.route('/retrieveCart')
def retrieve_Cart():
    cart_dict = {}

    db = shelve.open('db/Cart/cart.db', 'c')
    try:
        if 'Cart' in db:
            cart_dict = db['Cart']
        else:
            db['Cart'] = cart_dict
    except:
        print("Error in opening storage.db")
    db.close()

    cart_list = []
    for key in cart_dict:  # {1:object(lucas,1,3),2:object(qwdqdw,3,4)}
        cart = cart_dict.get(key)
        cart_list.append(cart)

    total = 0
    for object in cart_list:
        if object.get_user_id() == current_user.get_id():
            subtotal = object.set_subtotal(object.get_price(), object.get_discount(), object.get_quantity_bought())
            total = total + float(subtotal)

    return render_template('shoppingCart.html', count=len(cart_list), cart_list=cart_list, total_price=total)


@app.route('/updateQuantity/<int:id>', methods=['POST'])
def update_quantity(id):
    cart_dict = {}

    db = shelve.open('db/Cart/cart.db', 'w')
    try:
        if 'Cart' in db:
            cart_dict = db['Cart']
        else:
            db['Cart'] = cart_dict
    except:
        print("Error in opening storage.db")
        print('hello')
    if request.method == "POST":
        quantity = request.form.get('quantity')
        print(cart_dict.get(id).get_quantity_bought())
        cart_dict.get(id).set_quantity_bought(quantity)
        print(quantity)
        print(cart_dict.get(id).get_quantity_bought())

    db['Cart'] = cart_dict
    db.close()
    return redirect(url_for('retrieve_Cart'))


@app.route('/deleteCart/<int:id>', methods=['POST'])
def delete_cart(id):
    cart_dict = {}
    db = shelve.open('db/Cart/cart.db', 'w')
    cart_dict = db['Cart']

    cart_dict.pop(id)

    db['Cart'] = cart_dict
    db.close()

    return redirect(url_for('retrieve_Cart'))


@app.route('/confirmPage', methods=["GET", "POST"])
@login_required
def confirm_page():
    db3 = shelve.open('db/Card/card', 'c')
    card_dict = {}

    try:
        if 'Card' in db3:
            card_dict = db3['Card']
        else:
            db3['Card'] = card_dict
    except:
        print("Error in opening storage.db")
    db3.close()

    card_list = []
    for i in card_dict:
        card = card_dict.get(i)
        if card.get_user_id() == current_user.get_id():
            card_list.append(card)
    cart_dict = {}

    db = shelve.open('db/Cart/cart.db', 'r')
    try:
        if 'Cart' in db:
            cart_dict = db['Cart']
        else:
            db['Cart'] = cart_dict
    except:
        print("Error in opening storage.db")
    db.close()

    if request.method == "POST":
        point_discount = 0
        point_discount = request.form.get('points')
        if point_discount == None:
            point_discount = 0
            print(point_discount)


        quantity = request.form.get('quantity')
        print(quantity)
        cart_list = []
        for key in cart_dict:
            cart = cart_dict.get(key)
            cart_list.append(cart)

        total = 0
        for object in cart_list:
            if object.get_user_id() == current_user.get_id():
                subtotal = object.set_subtotal(object.get_price(), object.get_discount(), object.get_quantity_bought())
                total = total + float(subtotal)

        total_price_without_discount = total
        if point_discount != None:
            total = total - float(point_discount)

        points_left = current_user.getpoints() - float(point_discount)

        db2 = shelve.open('db/customer/users')
        user_dict = {}
        user_dict = db2['customer']
        for users in user_dict.values():
            user_list = []
            if users.get_id() == current_user.get_id():
                user_list.append(users)
            else:
                continue
            user = user_list[0]
        db2.close()

    return render_template('confirmationPage.html', count=len(cart_list), cart_list=cart_list, user=user,
                           total_price=round(total,2), card_list=card_list,point_discount=round(float(point_discount),2),total_price_without_discount=total_price_without_discount,points_left=round(points_left,2))


@app.route("/addCard", methods=["GET", "POST"])
def addCard():
    creditCard_form = CreateCreditCardForm()
    if request.method == "POST":
        # Retrieve the user data from the signup form
        card_name = creditCard_form.card_name.data
        credit_number = creditCard_form.credit_number.data
        credit_cvv = creditCard_form.credit_cvv.data
        expiry_date = creditCard_form.expiry_date.data

        error = None
        card_dict = {}
        try:
            db = shelve.open('db/Card/card', 'c')
            if 'Card' in db:
                card_dict = db['Card']
            else:
                db['Card'] = card_dict

            card = Card.Card(card_name, credit_number, credit_cvv, expiry_date, current_user.get_id())
            card_dict[card.get_card_id()] = card
            db['Card'] = card_dict
            db.close()
            return redirect(url_for('update'))
        except IOError:
            print("IO Error")
        except Exception as ex:
            print(f"Unknown error occurred as {ex}")

    return render_template('CreditCardForm.html', form=creditCard_form)


@app.route('/deleteCard/<int:id>', methods=['POST'])
def delete_card(id):
    card_dict = {}
    db = shelve.open('db/Card/card', 'w')
    card_dict = db['Card']

    card_dict.pop(id)

    db['Card'] = card_dict
    db.close()

    return redirect(url_for('update'))


@app.route('/addSales', methods=["GET", "POST"])
def addSales():
    cart_dict = {}
    db = shelve.open('db/Cart/cart.db', 'w')
    cart_dict = db['Cart']

    sales_dict = {}
    db2 = shelve.open('db/Sales/sales.db', 'c')

    print("added to sales")

    try:
        sales_dict = db2['Sales']

    except:
        db2['Sales'] = sales_dict
        print("Error in retrieving Cart from cart.db")

    db3 = shelve.open('db/customer/users', 'w')
    user_dict = {}
    user_dict = db3['customer']

    if request.method == "POST":
        point_discount = request.form.get("pointsSales")
        print(f"discount{point_discount}")
        address = request.form.get("address")
        credit_card = request.form.get("credit_card")
        key_list = []
        total_quantity = 0
        sales_id_list = []
        for key in cart_dict:  # {1: object-lucas,2:object-banana}
            if cart_dict.get(key).get_user_id() == current_user.get_id():
                total_quantity += 1
                key_list.append(key)
                cart_product = cart_dict.get(key)
                print(cart_product)
                sales = Sales.Sales(cart_product.get_product_name(), cart_product.get_product_desc(),
                                    cart_product.get_price(), cart_product.get_discount(), cart_product.get_quantity(),
                                    cart_product.get_quantity_bought(), address, current_user.get_id())


                for key in sales_dict:  # 1:bronze 6:silver 3: bronze
                    if key == sales.get_sales_id():
                        sales.set_sales_id(int(sales.get_sales_id()) + 1)
                # {}
                sales_id_list.append(sales.get_sales_id())
                sales_dict[sales.get_sales_id()] = sales
                # {1:object(lucas,2,3,4, 2: object(wewd,4,5,6)}

                print(sales_dict)  # {1:object-apple,}
                inventory_dict = {}

                db4 = shelve.open('db/Inventory/inventory.db', 'w')
                inventory_dict = db4['Inventory']

                for i in inventory_dict:  # {1:object(lucas,2,3,3) 2: dewwqdq}
                    inventory_name = cart_product.get_product_name()  # lucas
                    inventory = inventory_dict.get(i)  # object(lucas,2,3,3)

                    if inventory.get_product_name() == inventory_name:
                        print(sales.get_quantity())
                        print(sales.get_quantity_bought())
                        inventory.set_quantity(int(sales.get_quantity()) - int(sales.get_quantity_bought()))

                db4['Inventory'] = inventory_dict
                db4.close()

    points_discounted_per_item = float(point_discount)/total_quantity
    current_user_id = current_user.get_id()
    for i in sales_id_list:
        salesProduct = sales_dict.get(i)
        salesProduct.set_point_discount(points_discounted_per_item)
        user_dict.get(current_user_id).setpoints((float(user_dict.get(current_user_id).getpoints()) + float(
                            salesProduct.set_subtotal(salesProduct.get_price(), salesProduct.get_discount(),
                                               salesProduct.get_quantity_bought(),salesProduct.get_point_discount()) * 0.2)))
    user_dict.get(current_user_id).setpoints(round((float(user_dict.get(current_user_id).getpoints())-float(point_discount)),2))
    print(f"points:{current_user.getpoints()}")




    Cart.Cart.count_id = 0

    for i in key_list:
        cart_dict.pop(i)
        print(i)
    print(cart_dict)
    db3['customer'] = user_dict
    db2['Sales'] = sales_dict
    db["Cart"] = cart_dict
    db.close()
    db2.close()
    db3.close()
    flash("Items has been purchased.")
    return redirect(url_for('shop'))


# @app.route('/createSales', methods=['GET', 'POST'])
# def create_sales():
#     inventory_dict = {}
#     db = shelve.open('inventory.db', 'r')
#     inventory_dict = db['Inventory']
#     db.close()
#
#     create_sales_form = CreateSalesForm(request.form)
#     if request.method == 'POST' and create_sales_form.validate():
#         sales_dict = {}
#         db =shelve.open('sales.db','c')
#
#         try:
#                 sales_dict = db['Sales']
#         except:
#                 print("Error in retrieving Sales from sales.db.")
#         product_name = create_sales_form.product_name.data
#
#         sales = {}
#         for key in inventory_dict:
#             product = inventory_dict.get(key)
#             product_in_inventory = product.get_product_name()
#             if product_name == product_in_inventory:
#                 sales = Sales.Sales(product.get_product_name(),product.get_product_desc(),product.get_price(),product.get_discount(),product.get_quantity(),create_sales_form.quantity_bought.data)
#                 for i in sales_dict: # 1:bronze 6:silver 3: bronze
#                     if i == sales.get_sales_id():
#                        sales.set_sales_id(int(sales.get_sales_id())+1)
#                 sales_dict[sales.get_sales_id()] = sales
#             else:
#                 print("not in inventory")
#
#
#
#         db['Sales'] = sales_dict
#         db.close()
#
#         return redirect(url_for('retrieve_sales'))
#     return render_template('createSales.html', form=create_sales_form)

@app.route('/retrieveSales')
def retrieve_sales():
    sales_dict = {}
    db = shelve.open('db/Sales/sales.db', 'c')
    try:
        if 'Sales' in db:
            sales_dict = db['Sales']
        else:
            db['Sales'] = sales_dict
    except:
        print("Error in opening storage.db")
    db.close()
    # {1: lebron, 2: curry, 3: gianiss}
    sales_list = []

    # var1 = []
    # var2 = []
    for key in sales_dict:  # [lebron, curry, giayniss]
        # variable = sales_dict.get(key)
        # var1.append(variable.get_quantity())
        # var2.append(variable.get_brand())
        sales = sales_dict.get(key)
        sales_list.append(sales)

    return render_template('retrieveSales.html', count=len(sales_list), sales_list=sales_list)


@app.route('/createInventory', methods=['GET', 'POST'])
def create_inventory():
    create_inventory_form = CreateInventoryForm(request.form)
    if request.method == 'POST' and create_inventory_form.validate():
        req = request.files.to_dict()['product_image']
        req.save('./' + app.config['UPLOAD_FOLDER'] + req.filename)

        inventory_dict = {}
        db = shelve.open('db/Inventory/inventory.db', 'c')

        try:
            inventory_dict = db['Inventory']
        except:
            db['Inventory'] = inventory_dict
            print("Error in retrieving Inventory from inventory.db.")

        inventory = Inventory.Inventory(create_inventory_form.product_name.data,
                                        create_inventory_form.product_desc.data, create_inventory_form.category.data,
                                        create_inventory_form.price.data,
                                        create_inventory_form.discount.data, create_inventory_form.quantity.data,
                                        req.filename)

        for key in inventory_dict:  # {1:bronze 6:silver 3: bronze}
            if key == inventory.get_inventory_id():
                inventory.set_inventory_id(int(inventory.get_inventory_id()) + 1)
        inventory_dict[inventory.get_inventory_id()] = inventory  # 1:bronze 2:silver 3:bronze 4:gold

        db['Inventory'] = inventory_dict
        db.close()

        return redirect(url_for('retrieve_inventory'))
    return render_template('createInventory.html', form=create_inventory_form)


@app.route('/retrieveInventory')
def retrieve_inventory():
    inventory_dict = {}
    db = shelve.open('db/Inventory/inventory.db', 'c')
    try:
        if 'Inventory' in db:
            inventory_dict = db['Inventory']
        else:
            db['Inventory'] = inventory_dict
    except:
        print("Error in opeing storage.db")
    db.close()

    inventory_list = []
    for key in inventory_dict:
        inventory = inventory_dict.get(key)
        inventory_list.append(inventory)

    return render_template('retrieveInventory.html', count=len(inventory_list), inventory_list=inventory_list)


@app.route('/updateInventory/<int:id>/', methods=['GET', 'POST'])
def update_inventory(id):
    update_inventory_form = CreateInventoryForm(request.form)
    if request.method == 'POST' and update_inventory_form.validate():
        inventory_dict = {}
        db = shelve.open('db/Inventory/inventory.db', 'w')
        inventory_dict = db['Inventory']

        inventory = inventory_dict.get(id)
        inventory.set_product_name(update_inventory_form.product_name.data)
        inventory.set_product_desc(update_inventory_form.product_desc.data)
        inventory.set_category(update_inventory_form.category.data)
        inventory.set_price(update_inventory_form.price.data)
        inventory.set_discount(update_inventory_form.discount.data)
        inventory.set_quantity(update_inventory_form.quantity.data)
        inventory.set_product_image(update_inventory_form.product_image.data)

        db['Inventory'] = inventory_dict
        db.close()

        return redirect(url_for('retrieve_inventory'))
    else:
        inventory_dict = {}
        db = shelve.open('db/Inventory/inventory.db', 'r')
        inventory_dict = db['Inventory']
        db.close()

        inventory = inventory_dict.get(id)
        update_inventory_form.product_name.data = inventory.get_product_name()
        update_inventory_form.product_desc.data = inventory.get_product_desc()
        update_inventory_form.category.data = inventory.get_category()
        update_inventory_form.price.data = inventory.get_price()
        update_inventory_form.discount.data = inventory.get_discount()
        update_inventory_form.quantity.data = inventory.get_quantity()
        update_inventory_form.product_image.data = inventory.get_product_image()

        return render_template('updateInventory.html', form=update_inventory_form)


@app.route('/deleteInventory/<int:id>', methods=['POST'])
def delete_inventory(id):
    inventory_dict = {}
    db = shelve.open('db/Inventory/inventory.db', 'w')
    inventory_dict = db['Inventory']

    inventory_dict.pop(id)

    db['Inventory'] = inventory_dict
    db.close()

    return redirect(url_for('retrieve_inventory'))


# GENERATION INNIT
@app.route('/InventoryGeneration')
def inventory_generation():
    inventory_dict = {}
    db = shelve.open('db/Inventory/inventory.db', 'r')
    try:
        if 'Inventory' in db:
            inventory_dict = db['Inventory']
        else:
            db['Inventory'] = inventory_dict
    except:
        print("Error in opening storage.db")
    db.close()

    inventory_product_names = []
    inventory_quantities = []
    colors = []
    color_count = 0
    for key in inventory_dict:
        inventory = inventory_dict.get(key)
        inventory_quantities.append(inventory.get_quantity())
        inventory_product_names.append(inventory.get_product_name())
        if int(inventory.get_quantity()) < 400:
            colors.append('#b93737')
        elif int(inventory.get_quantity()) < 800:
            colors.append('#ffd766')
        else:
            colors.append('#bada55')

    df = pd.DataFrame(dict(
        x=inventory_product_names,
        y=inventory_quantities
    ))

    df.to_excel(r'C:\Users\Elijah\Downloads\Koryo_Mart_Inventory.xlsx', index=False)

    data = [
        go.Bar(x=df['x'], y=df['y'], width=0.5, marker_color=colors)
    ]
    graph1JSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('inventoryGeneration.html', graph1JSON=graph1JSON)


@app.route('/SalesGeneration')
def sales_generation():
    sales_dict = {}
    db = shelve.open('db/Sales/sales.db', 'r')
    try:
        if 'Sales' in db:
            sales_dict = db['Sales']
        else:
            db['Sales'] = sales_dict
    except:
        print("Error in opening storage.db")
    db.close()

    sales_product_names = []
    sales_product_total = []
    colors = []
    color_count = 0

    sales_report_dict = {}
    for key in sales_dict:  # apple, banna, apple,
        sales = sales_dict.get(key)
        total = 0
        if sales.get_product_name() in sales_report_dict:
            total = int(sales_report_dict[str(sales.get_product_name())]) + int(
                sales.set_subtotal(sales.get_price(), sales.get_discount(), sales.get_quantity_bought(),sales.get_point_discount()))
            sales_report_dict[sales.get_product_name()] = total

        else:
            sales_report_dict[sales.get_product_name()] = total
            total = int(sales_report_dict[str(sales.get_product_name())]) + int(
                sales.set_subtotal(sales.get_price(), sales.get_discount(), sales.get_quantity_bought(),sales.get_point_discount()))
            sales_report_dict[sales.get_product_name()] = total

    for key in sales_report_dict:
        sales = sales_report_dict.get(key)
        sales_product_names.append(key)
        sales_product_total.append(sales)
        if int(total) > 0:
            colors.append('#666a8c')
        else:
            colors.append('#b93737')

    df = pd.DataFrame(dict(
        x=sales_product_names,
        y=sales_product_total
    ))

    df.to_excel(r'C:\Users\Elijah\Downloads\Koryo_Mart_Sales.xlsx', index=False)

    data = [
        go.Bar(x=df['x'], y=df['y'], width=0.5, marker_color=colors)
    ]
    graph1JSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('SalesGeneration.html', graph1JSON=graph1JSON)


# CUSTOMER SUPPORT INNNIT
@app.route('/createFeedbackForm', methods=['GET', 'POST'])
@login_required
def create_feedback():
    create_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('db/Feedback/feedback.db', 'c')

        try:
            feedback_dict = db['Feedback']
        except:
            print("Error in retrieving Feedback from feedback.db.")

        feedback = FeedbackForm.Feedback(create_feedback_form.name.data, create_feedback_form.email.data,
                                         create_feedback_form.question1.data, create_feedback_form.question2.data,
                                         create_feedback_form.question3.data, create_feedback_form.remarks.data)
        for key in feedback_dict:
            if key == feedback.get_feedback_id():
                feedback.set_feedback_id(int(feedback.get_feedback_id()) + 1)
        feedback_dict[feedback.get_feedback_id()] = feedback
        db['Feedback'] = feedback_dict
        db.close()

        answer = create_feedback_form.question1.data
        if answer != 0:
            flash("Thank you for your feedback!", "success")

        db = shelve.open('db/customer/users')
        user_dict = {}
        user_dict = db['customer']
        for users in user_dict.values():
            if users.get_id() == current_user.get_id():
                users.setusername(create_feedback_form.name.data)
                users.setemail(create_feedback_form.email.data)
                db['customer'] = user_dict
                db.close()
        return redirect(url_for('home'))
    else:
        create_feedback_form.name.data = current_user.getusername()
        create_feedback_form.email.data = current_user.getemail()

    return render_template('createFeedbackForm.html', form=create_feedback_form)


@app.route('/retrieveFeedbackForm')
def retrieve_feedback():
    feedback_dict = {}
    db = shelve.open('db/Feedback/feedback.db', 'r')
    feedback_dict = db['Feedback']
    db.close()

    feedback_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        feedback_list.append(feedback)

    return render_template('retrieveFeedbackForm.html', count=len(feedback_list), feedback_list=feedback_list)


@app.route('/deleteFeedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedback_dict = {}
    db = shelve.open('db/Feedback/feedback.db', 'w')
    feedback_dict = db['Feedback']

    feedback_dict.pop(id)

    db['Feedback'] = feedback_dict
    db.close()

    return redirect(url_for('retrieve_feedback'))


@app.route('/createReportForm', methods=['GET', 'POST'])
@login_required
def create_report():

    create_report_form = CreateReportForm(request.form)
    if request.method == 'POST' and create_report_form.validate():
        req = request.files.to_dict()['report_image']
        req.save('./' + app.config['UPLOAD_FOLDER'] + req.filename)

        report_dict = {}
        db = shelve.open('db/Report/report.db', 'c')

        try:
            report_dict = db['Report']
        except:
            print("Error in retrieving Report from report.db.")

        report = ReportForm.Report(create_report_form.name.data, create_report_form.email.data,
                                   create_report_form.contact.data, create_report_form.problem.data,
                                   create_report_form.other.data, create_report_form.date.data, req.filename,
                                   create_report_form.remarks.data)
        for key in report_dict:
            if key == report.get_report_id():
                report.set_report_id(int(report.get_report_id()) + 1)
        report_dict[report.get_report_id()] = report
        db['Report'] = report_dict
        db.close()

        answer = create_report_form.name.data
        if answer != 0:
            flash("Thank you for submitting your report. We will get back to you as soon as possible.")

        db = shelve.open('db/customer/users')
        user_dict = {}
        user_dict = db['customer']
        for users in user_dict.values():
            if users.get_id() == current_user.get_id():
                users.setusername(create_report_form.name.data)
                users.setemail(create_report_form.email.data)
                users.setphone_number(create_report_form.contact.data)
                db['customer'] = user_dict
                db.close()
        return redirect(url_for('home'))
    else:
        create_report_form.name.data = current_user.getusername()
        create_report_form.email.data = current_user.getemail()
        create_report_form.contact.data = current_user.getphone_number()

    return render_template('createReportForm.html', form=create_report_form)


@app.route('/retrieveReportForm')
def retrieve_report():
    report_dict = {}
    db = shelve.open('db/Report/report.db', 'r')
    report_dict = db['Report']
    db.close()

    report_list = []
    for key in report_dict:
        report = report_dict.get(key)
        report_list.append(report)

    return render_template('retrieveReportForm.html', count=len(report_list), report_list=report_list)


@app.route('/deleteReport/<int:id>', methods=['POST'])
def delete_report(id):
    report_dict = {}
    db = shelve.open('db/Report/report.db', 'w')
    report_dict = db['Report']

    report_dict.pop(id)

    db['Report'] = report_dict
    db.close()

    return redirect(url_for('retrieve_report'))


@app.route("/updateStatus/<int:id>", methods=['POST'])
def update_status(id):
    report_dict = {}
    db = shelve.open('db/Report/report.db', 'w')

    try:
        if 'Report' in db:
            report_dict = db['Report']
        else:
            db['Report'] = report_dict
    except:
        print("Error in opening storage.db")

    report = report_dict.get(id)
    report.set_status('completed')
    db['Report'] = report_dict

    db.close()

    return redirect(url_for('retrieve_report'))


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


@app.route('/customerchatlogs')
def retrieve_conversation():
    conversation_dict = {}
    db = shelve.open('db/Conversation/conversation.db', 'r')
    conversation_dict = db['Conversation']
    db.close()

    conversation_list = []
    for key in conversation_dict:
        conversation = conversation_dict.get(key)
        conversation_list.append(conversation)

    return render_template('customerchatlogs.html', count=len(conversation_list), conversation_list=conversation_list)


@app.route('/deleteConversation/<int:id>', methods=['POST'])
def delete_conversation(id):
    conversation_dict = {}
    db = shelve.open('db/Conversation/conversation.db', 'w')
    conversation_dict = db['Conversation']

    conversation_dict.pop(id)

    db['Conversation'] = conversation_dict
    db.close()

    return redirect(url_for('retrieve_conversation'))


if __name__ == '__main__':
    app.run(debug=True)
