import flask
from flask import Flask
from chatbotconfig import Config

app=Flask(__name__)
app.config.from_object(Config)

import keras
import nltk
import pickle
import json
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
from tensorflow.keras.models import load_model
#import csv
import os

from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()

model=load_model('chatbot_codes/mymodel.h5', compile = False)
intents = json.loads(open('chatbot_codes/intents.json').read())
#intents = json.loads(open('chatbot_codes\intents.json', encoding='cp1252', errors='ignore').read())
words = pickle.load(open('chatbot_codes/words.pkl','rb'))
classes = pickle.load(open('chatbot_codes/classes.pkl','rb'))
#csv_file = csv.reader(open('chatbot_codes/GeneralProductPricing.csv','r'))

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("Hub Version: ", hub.__version__)
print("GPU is", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")

os.environ[‘TF_CPP_MIN_LOG_LEVEL’] = ‘2’

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=8081)
    
from chatbot import routes
