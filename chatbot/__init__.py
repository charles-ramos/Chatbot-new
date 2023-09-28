import flask
from flask import Flask
from chatbotconfig import Config

app=Flask(__name__)
app.config.from_object(Config)

import keras
import nltk
import pickle
import json
from keras.models import load_model
import csv

from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()

model=load_model('chatbot_codes/mymodel.h5')
intents = json.loads(open('chatbot_codes/intents.json').read())
#intents = json.loads(open('chatbot_codes\intents.json', encoding='cp1252', errors='ignore').read())
words = pickle.load(open('chatbot_codes/words.pkl','rb'))
classes = pickle.load(open('chatbot_codes/classes.pkl','rb'))
csv_file = csv.reader(open('chatbot_codes\GeneralProductPricing.csv','r'))

if __name__=='__main__':
    app.run()
    
from chatbot import routes
