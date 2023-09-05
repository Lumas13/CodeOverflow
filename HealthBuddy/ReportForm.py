class Report:
    count_id = 0

    # initializer method
    def __init__(self, name, email, contact, problem, other, date, report_image, remarks):
        Report.count_id += 1
        self.__status = 'incomplete'
        self.__report_id = Report.count_id
        self.__name = name
        self.__email = email
        self.__contact = contact
        self.__problem = problem
        self.__other = other
        self.__date = date
        self.__report_image = report_image
        self.__remarks = remarks

    # accessor methods
    def get_status(self):
        return self.__status

    def get_report_id(self):
        return self.__report_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_contact(self):
        return self.__contact

    def get_problem(self):
        return self.__problem

    def get_other(self):
        return self.__other

    def get_date(self):
        return self.__date

    def get_report_image(self):
        return self.__report_image

    def get_remarks(self):
        return self.__remarks

    def set_status(self, status):
        self.__status = status

    def set_report_id(self, report_id):
        self.__report_id = report_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_contact(self, contact):
        self.__contact = contact

    def set_problem(self, problem):
        self.__problem = problem

    def set_other(self, other):
        self.__other = other

    def set_date(self, date):
        self.__date = date

    def set_report_image(self, report_image):
        self.__report_image = report_image

    def set_remarks(self, remarks):
        self.__remarks = remarks