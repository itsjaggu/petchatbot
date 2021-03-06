# This scripts creates and load GUI for chatbot. tkinter
import nltk
from nltk.stem import WordNetLemmatizer
from numpy.core.fromnumeric import reshape
from werkzeug.utils import html
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pymongo

from tensorflow.keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

# connecting with MongoDB
conn = 'mongodb+srv://TeamCatViz:RockingTeam#1@cluster0.ddihz.mongodb.net/petfinder_db?retryWrites=true&w=majority'
#conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

# getting prediction tag from the model based on user input 
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# getting response from based on the predictions
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

# fetching data fromm mongodb based on prediction and response
def getPets(prop,param):
    # Retrieve the all images
    # Query Parameters
    print(param)
    if(prop == "type"):
        params = {
            "type" : {"$eq" : f"{param.capitalize()}"},
        }
        fields = {"_id":0
                    ,"url":1
                }
    elif(prop == "breed"):
        params = {
            "breeds.primary" : {"$eq" : f"{param.capitalize()}"},
        }
        fields = {"_id":0
                    ,"url":1
                }
    print(params,fields)
    db = client.petfinder_db
    pets_coll = db.tx_pet_data.find(params,fields).limit(5)
    pet_list = list(pets_coll)
    print(len(pet_list))
    url_list = []
    if(len(pet_list)>2):
        for pet in pet_list:
            url = pet["url"]
            url_list.append(f"<a href={url} target=\"_blank\">{url}</a>")
        return str(url_list)
    else:
        return f"Couldn't find any {param}"

# primary functin to get and send response to the user in chat window
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    print(ints,res)
    type_arr = ["search_dog","search_cat","search_bird","search_cat","search_horse","search_rabbit","search_barnyard","search_smallfurry"]
    breed_arr = ["search_dog_Hound","search_dog_Shepherd","search_cat_Tabby","search_cat_Tuxedo"]
    if(ints[0]['intent'] in type_arr):
        print(res)
        res = getPets("type",res)
    elif(ints[0]['intent'] in breed_arr):
        print(res)
        res = getPets("breed",res)

    return res

# tkinter GUI, commented as it is not supported in Heroku.
"""     #Creating GUI with tkinter
import tkinter
from tkinter import *

def main():
    def send():
        msg = EntryBox.get("1.0",'end-1c').strip()
        EntryBox.delete("0.0",END)

        if msg != '':
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
            res = chatbot_response(msg)
            ChatLog.insert(END, "Bot: " + res + '\n\n')
                
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)

    base = Tk()
    base.title("Hello")
    base.geometry("400x500")
    base.resizable(width=FALSE, height=FALSE)

    #Create Chat window
    ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

    ChatLog.config(state=DISABLED)

    #Bind scrollbar to Chat window
    scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
    ChatLog['yscrollcommand'] = scrollbar.set

    #Create the box to enter message
    EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
    #EntryBox.bind("<Return>", send)

    #Create Button to send message
    SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                        bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                        command= send )

    #Place all components on the screen
    scrollbar.place(x=376,y=6, height=386)
    ChatLog.place(x=6,y=6, height=386, width=370)
    EntryBox.place(x=6, y=401, height=90, width=265)
    SendButton.place(x=260, y=401, height=90)

    base.mainloop() """

