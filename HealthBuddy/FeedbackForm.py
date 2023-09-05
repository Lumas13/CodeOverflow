class Feedback:
    count_id = 0

    # initializer method
    def __init__(self, name, email, question1, question2, question3, remarks):
        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id
        self.__name = name
        self.__email = email
        self.__question1 = question1
        self.__question2 = question2
        self.__question3 = question3
        self.__remarks = remarks

    # accessor methods
    def get_feedback_id(self):
        return self.__feedback_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_question1(self):
        return self.__question1

    def get_question2(self):
        return self.__question2

    def get_question3(self):
        return self.__question3

    def get_remarks(self):
        return self.__remarks


    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_question1(self, question1):
        self.__question1 = question1

    def set_question2(self, question2):
        self.__question2 = question2

    def set_question3(self, question3):
        self.__question3 = question3

    def set_remarks(self, remarks):
        self.__remarks = remarks