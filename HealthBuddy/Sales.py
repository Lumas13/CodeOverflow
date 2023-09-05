import Cart

class Sales():
    count_id = 0

    # initializer method
    def __init__(self, product_name, product_desc, price, discount, quantity, quantity_bought,address,user_id):
        Sales.count_id += 1
        self.__sales_id = Sales.count_id
        self.__quantity_bought = quantity_bought
        self.__subtotal = 0
        self.__user_id = user_id
        self.__pointsdiscount = 0
        #inventory innit
        self.__product_name = product_name
        self.__product_desc = product_desc
        self.__price = price
        self.__discount = discount
        self.__quantity = quantity
        self.__address = address




    # accessor methods
    def get_sales_id(self):
        return self.__sales_id

    def get_quantity_bought(self):
        return self.__quantity_bought

    def get_subtotal(self):
        return self.__subtotal

    def get_address(self):
        return self.__address
    def get_user_id(self):
        return self.__user_id
    def get_point_discount(self):
        return self.__pointsdiscount

    # mutator methods
    def set_sales_id(self, sales_id):
        self.__sales_id = sales_id

    def set_quantity_bought(self, quantity_bought):
        self.__quantity_bought = quantity_bought

    def set_subtotal(self,price,discount,quantity_bought,point_discount):
        self.__subtotal = (float(price)*(1-float(discount)/100)*float(quantity_bought))-float(point_discount)
        return self.__subtotal

    def set_address(self, address):
        self.__address = address

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_point_discount(self,point_discount):
        self.__pointsdiscount = point_discount

    #inventory
    def get_product_name(self):
        return self.__product_name

    def get_product_desc(self):
        return self.__product_desc

    def get_price(self):
        return self.__price

    def get_discount(self):
        return self.__discount

    def get_quantity(self):
        return self.__quantity

    # mutator methods

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_product_desc(self, product_desc):
        self.__product_desc = product_desc

    def set_price(self, price):
        self.__price = price

    def set_discount(self, discount):
        self.__discount = discount

    def set_quantity(self, quantity):
        self.__quantity = quantity
