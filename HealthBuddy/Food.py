class Food():
    count_id = 0

    # initializer method
    def __init__(self, name,img, measure,calories, carbs, fats, protein, sodium,sugar):
        Food.count_id += 1
        self.__name = name
        self.__img = img
        self.__measure= measure
        self.__calories = calories
        self.__carbs = carbs
        self.__fats = fats
        self.__protein = protein
        self.__sodium = sodium
        self.__sugar = sugar
        self.__food_id = Food.count_id



    # accessor methods
    def set_name(self,name):
        self.__name= name

    def set_img(self,img):
        self.__img = img

    def set_measure(self,measure):
        self.__measure= measure

    def set_calories(self,calories):
        self.__calories = calories

    def set_carbs(self,carbs):
        self.__carbs = carbs

    def set_fats(self,fats):
        self.__fats= fats

    def set_protein(self,protein):
        self.__protein= protein

    def set_sodium(self,sodium):
        self.__sodium = sodium

    def set_sugar(self,sugar):
        self.__sugar = sugar

    def set_food_id(self,food_id):
        self.__food_id = food_id

    def get_name(self):
        return self.__name

    def get_img(self):
        return self.__img

    def get_measure(self):
        return self.__measure

    def get_calories(self):
        return self.__calories

    def get_carbs(self):
        return self.__carbs

    def get_fats(self):
        return self.__fats

    def get_protein(self):
        return self.__protein

    def get_sodium(self):
        return self.__sodium

    def get_sugar(self):
        return self.__sugar

    def get_food_id(self):
        return self.__food_id
