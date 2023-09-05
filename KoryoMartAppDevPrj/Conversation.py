class Conversation:
    count_id = 0

    def __init__(self, sentence, return_choice, user_id):
        Conversation.count_id += 1
        self.__conversation_id = Conversation.count_id
        self.__sentence = sentence
        self.__return_choice = return_choice
        self.__user_id = user_id

    def get_conversation_id(self):
        return self.__conversation_id

    def get_sentence(self):
        return self.__sentence

    def get_return_choice(self):
        return self.__return_choice

    def get_user_id(self):
        return self.__user_id

    def set_conversation_id(self, conversation_id):
        self.__conversation_id = conversation_id

    def set_sentence(self, sentence):
        self.__sentence = sentence

    def set_return_choice(self, return_choice):
        self.__return_choice = return_choice

    def set_user_id(self, user_id):
        self.__user_id = user_id
