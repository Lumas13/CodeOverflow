from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, email, password, id):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__id = id
        self.__role = ''
        self.__first_name = ''
        self.__last_name = ''
        self.__phone_number = ''
        self.__address = ''
        self.__profile_picture = ''
        self.__credit_number = ''
        self.__credit_cvv = ''
        self.__credit_date = ''
        self.__profile_picture = ''
        self.__points =  0

        self.__weight = 0
        self.__age = 0
        self.__height = 0
        self.__gender = ''
        self.__rec_cal = 1
        self.__activity_level = ''
        self.__goal = ''

    # Mutator Methods
    def getusername(self):
        return self.__username

    def getemail(self):
        return self.__email

    def getpassword(self):
        return self.__password

    def get_id(self):
        return self.__id

    def getrole(self):
        return self.__role

    def getfirst_name(self):
        return self.__first_name

    def getlast_name(self):
        return self.__last_name

    def getphone_number(self):
        return self.__phone_number

    def getaddress(self):
        return self.__address

    def getprofile_picture(self):
        return self.__profile_picture

    def getcredit_number(self):
        return self.__credit_number

    def getcredit_cvv(self):
        return self.__credit_cvv

    def getcredit_date(self):
        return self.__credit_date

    def getpoints(self):
        return self.__points



    # Accessor Methods
    def setusername(self, username):
        self.__username = username

    def setemail(self, email):
        self.__email = email

    def setpassword(self, password):
        self.__password = password

    def set_id(self, id):
        self.__id = id

    def setrole(self, role):
        self.__role = role

    def setfirst_name(self, first_name):
        self.__first_name = first_name

    def setlast_name(self, last_name):
        self.__last_name = last_name

    def setphone_number(self, phone_number):
        self.__phone_number = phone_number

    def setaddress(self, address):
        self.__address = address

    def setprofile_picture(self, profile_picture):
        self.__profile_picture = profile_picture

    def get_weight(self):
        return self.__weight

    def set_weight(self, weight):
        self.__weight = weight

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

    def get_height(self):
        return self.__height

    def set_height(self, height):
        self.__height = height

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        self.__gender = gender

    def get_rec_cal(self):
        return self.__rec_cal

    def set_rec_cal(self, rec_cal):
        self.__rec_cal = rec_cal

    def get_activity_level(self):
        return self.__activity_level

    def set_activity_level(self, activity_level):
        self.__activity_level = activity_level

    def setcredit_number(self, credit_number):
        self.__credit_number = credit_number

    def setcredit_cvv(self, cvv):
        self.__credit_cvv = cvv

    def setcredit_date(self, credit_date):
        self.__credit_date = credit_date

    def setpoints(self,points):
        self.__points = points

    def get_goal(self):
        return self.__goal
    def set_goal(self, goal):
        self.__goal = goal

