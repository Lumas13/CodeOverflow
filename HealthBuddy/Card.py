import Cart

class Card():
    count_id = 0

    # initializer method
    def __init__(self,card_name, card_no, cvv, expiry_date,user_id):
        Card.count_id += 1
        self.__card_id = Card.count_id
        self.__card_name = card_name
        self.__card_no = card_no
        self.__cvv = cvv
        self.__expiry_date = expiry_date
        self.__user_id = user_id
        self.__masked_card = ''


    # accessor methods
    def get_card_id(self):
        return self.__card_id

    def get_card_name(self):
        return self.__card_name

    def get_card_no(self):
        return self.__card_no

    def set_masked_card_no(self,card_no):
        card_split = []
        for no in card_no:
                card_split.append(no)
        card_split[0] = '*'
        card_split[1] = '*'
        card_split[2] = '*'
        card_split[3] = '*'
        card_split[4] = '*'
        card_split[5] = '*'
        card_split[6] = '*'
        card_split[7] = '*'
        card_split[8] = '*'
        card_split[9] = '*'
        card_split[10] = '*'
        card_split[11] = '*'

        masked_card = ''.join(card_split)
        self.__masked_card = masked_card
        return self.__masked_card






    def get_cvv(self):
        return self.__cvv

    def get_expiry_date(self):
        return self.__expiry_date


    def get_user_id(self):
        return self.__user_id

    # mutator methods
    def set_card_id(self, card_id):
        self.__card_id = card_id

    def set_card_name(self, card_name):
        self.__card_name = card_name

    def set_card_no(self, card_no):
        self.__card_no = card_no

    def set_cvv(self, cvv):
        self.__cvv = cvv

    def set_expiry_date(self,expiry_date):
        self.__expiry_date = expiry_date

    def set_user_id(self, user_id):
        self.__user_id = user_id





