from Inventory import *
# Cart class

class Cart(Inventory):

    count_id = 0

    # initializer method
    def __init__(self, product_name, product_desc,category, price, discount, quantity, product_image, quantity_bought,user_id):
        Cart.count_id += 1
        super().__init__(product_name, product_desc,category, price, discount, quantity,product_image)
        self.__cart_id = Cart.count_id
        self.__quantity_bought = quantity_bought
        self.__subtotal = 0
        self.__user_id = user_id


    # accessor methods

    def get_cart_id(self):
        return self.__cart_id

    def get_quantity_bought(self):
        return self.__quantity_bought

    def get_subtotal(self):
        return self.__subtotal

    def get_user_id(self):
        return self.__user_id

    # mutator methods
    def set_cart_id(self, cart_id):
        self.__cart_id = cart_id

    def set_quantity_bought(self, quantity_bought):
        self.__quantity_bought = quantity_bought

    def set_subtotal(self,price,discount,quantity_bought):
        self.__subtotal = float(price)*(1-float(discount)/100)*float(quantity_bought)
        return self.__subtotal

    def set_user_id(self,user_id):
        self.__user_id = user_id

