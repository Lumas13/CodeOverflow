import random
import json
import shelve

import torch
from Conversation import Conversation
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from flask_login import current_user

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Koro"
#111111
def get_response(msg):
    conversation_dict = {}
    db = shelve.open('conversation.db', 'c')

    try:
        conversation_dict = db['Conversation']
    except:
        print("Error in retrieving Conversation from conversation.db.")

    conversation_list = []
    for key in conversation_dict:
        e_conversation = conversation_dict.get(key)
        conversation_list.append(e_conversation)

    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return_choice = random.choice(intent['responses'])
                # store sentence and return_choice
                conversation = Conversation(msg, return_choice, current_user.get_id())
                if len(conversation_list) > 0:
                    conversation.set_conversation_id(conversation_list[-1].get_conversation_id() + 1)
                conversation_dict[conversation.get_conversation_id()] = conversation
                db['Conversation'] = conversation_dict
                db.close()
                return return_choice

    conversation = Conversation(msg, "I'm sorry I do not \nunderstand. For further \nenquiries, please contact \nus via email\n<a href='mailto:KoryoMartBusiness@gmail.com'>Email Us</a> \nor send us feedback by \nclicking the <a href='http://127.0.0.1:5000/createFeedbackForm'>Feedback</a> \nlink.", current_user.get_id())

    if len(conversation_list) > 0:
        conversation.set_conversation_id(conversation_list[-1].get_conversation_id() + 1)
    conversation_dict[conversation.get_conversation_id()] = conversation
    db['Conversation'] = conversation_dict
    db.close()
    return "I'm sorry I do not \nunderstand. For further \nenquiries, please contact \nus via email\n<a href='mailto:KoryoMartBusiness@gmail.com'>Email Us</a> \nor send us feedback by \nclicking the <a href='http://127.0.0.1:5000/createFeedbackForm'>Feedback</a> \nlink."
#11111

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)
