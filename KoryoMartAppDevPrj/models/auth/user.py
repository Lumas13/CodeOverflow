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
        self.__credit_number = ''
        self.__credit_cvv = ''
        self.__credit_date = ''
        self.__profile_picture = ''
        self.__points = 0

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

    def getcredit_number(self):
        return self.__credit_number

    def getcredit_cvv(self):
        return self.__credit_cvv

    def getcredit_date(self):
        return self.__credit_date

    def getprofile_picture(self):
        return self.__profile_picture

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

    def setcredit_number(self, credit_number):
        self.__credit_number = credit_number

    def setcredit_cvv(self, cvv):
        self.__credit_cvv = cvv

    def setcredit_date(self, date):
        self.__credit_date = date

    def setprofile_picture(self, profile_picture):
        self.__profile_picture = profile_picture

    def setpoints(self, points):
        self.__points = points
