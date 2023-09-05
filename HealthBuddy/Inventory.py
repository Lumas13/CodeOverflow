# Inventory class
class Inventory:

    count_id = 0

    # initializer method
    def __init__(self, product_name, product_desc,category, price, discount, quantity,product_image):
        Inventory.count_id += 1
        self.__inventory_id = Inventory.count_id
        self.__product_name = product_name
        self.__product_desc = product_desc
        self.__category = category
        self.__price = price
        self.__discount = discount
        self.__quantity = quantity
        self.__product_image = product_image

    # accessor methods
    def get_inventory_id(self):
        return self.__inventory_id

    def get_product_name(self):
        return self.__product_name

    def get_product_desc(self):
        return self.__product_desc

    def get_category(self):
        return self.__category

    def get_price(self):
        return self.__price

    def get_discount(self):
        return self.__discount

    def get_quantity(self):
        return self.__quantity

    def get_product_image(self):
        return self.__product_image

    # mutator methods
    def set_inventory_id(self, inventory_id):
        self.__inventory_id = inventory_id

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_product_desc(self, product_desc):
        self.__product_desc = product_desc
    def set_category(self,category):
        self.__category = category

    def set_price(self, price):
        self.__price = price

    def set_discount(self, discount):
        self.__discount = discount

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_product_image(self,product_image):
        self.__product_image = product_image


