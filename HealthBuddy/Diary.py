import Inventory
from Food import *


# Cart class

class Diary(Food):  # Diary(Food)

    count_id = 0

    # initializer method
    def __init__(self, name, img, measure, calories, carbs, fats, protein, sodium, sugar, quantity, date, user_id,product_id):
        Diary.count_id += 1
        super().__init__(name, img, measure, calories, carbs, fats, protein, sodium, sugar)
        self.__diary_id = Diary.count_id
        self.__quantity = quantity
        self.__subtotal = 0
        self.__date = date
        self.__user_id = user_id
        self.__product_id = product_id

    # accessor methods

    def get_diary_id(self):
        return self.__diary_id

    def get_quantity(self):
        return self.__quantity

    def get_subtotal(self):
        return self.__subtotal

    def get_date(self):
        return self.__date

    def get_user_id(self):
        return self.__user_id

    def get_product_id(self):
        return self.__product_id

    # mutator methods
    def set_diary_id(self, diary_id):
        self.__diary_id = diary_id

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_subtotal(self, calories, quantity):
        self.__subtotal = float(calories) * float(quantity)
        return self.__subtotal

    def set_date(self, date):
        self.__date = date

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_product_id(self, product_id):
        self.__product_id = product_id


