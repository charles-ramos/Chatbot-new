import flask
from flask import Flask
from chatbotconfig import Config

app=Flask(__name__)
app.config.from_object(Config)

import tensorflow
import nltk
import pickle
import json
#from silence_tensorflow import silence_tensorflow
#silence_tensorflow()
from tensorflow.keras.models import load_model
#import csv
import os
os.environ['TF_ENABLE_MLIR_OPTIMIZATIONS'] = '1'

from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()

model=load_model('chatbot_codes/mymodel.h5', compile = False)
intents = json.loads(open('chatbot_codes/intents.json').read())
words = pickle.load(open('chatbot_codes/words.pkl','rb'))
classes = pickle.load(open('chatbot_codes/classes.pkl','rb'))


#if __name__=='__main__':
app.run(debug=True,host='0.0.0.0',port=8181)
    
from chatbot import routes
