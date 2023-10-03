from chatbot import app
from flask import Flask, render_template,flash, request, jsonify
from chatbot.forms import chatbotform
from chatbot.__init__ import model,words,classes,intents

import nltk
import pickle
import json
import numpy as np
from tensorflow.keras.models import Sequential,load_model
import random
from datetime import datetime
import pytz
import requests
import os
import billboard
import time
from pygame import mixer
import COVID19Py

from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()


#Predict
def clean_up(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def create_bow(sentence,words):
    sentence_words=clean_up(sentence)
    bag=list(np.zeros(len(words)))

    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence,model):
    p=create_bow(sentence,words)
    res=model.predict(np.array([p]))[0]
    threshold=0.9
    results=[[i,r] for i,r in enumerate(res) if r>threshold]
    results.sort(key=lambda x: x[1],reverse=True)
    return_list=[]

    for result in results:
        return_list.append({'intent':classes[result[0]],'prob':str(result[1])})
    return return_list



""" def prices_prompt():
    r = int(input('For food prices: \n Enter 1 to search by product name (eg. Bitterleaf) \n Enter 2 to search by observed date (eg. 03/03/2023) \n Enter 3 to search by market location (eg. Wuse, FCT Abuja) \n Enter 4 to search by market name (eg. Wuse Market) \n Enter here: '))
    ans = response(r)
    print(ans) """

def get_response(return_list,intents_json,text):

    if len(return_list)==0:
        tag='noanswer'
    else:
        tag=return_list[0]['intent']
    if tag=='datetime':
        x= "The date and time in Africa/ Nigeria are "
        tz = pytz.timezone('Africa/Lagos')
        dt=datetime.now(tz)
        x+=str(dt.strftime("%A"))+' '
        x+=str(dt.strftime("%d %B %Y"))+', '
        x+=str(dt.strftime("%H:%M:%S")) 
        return x, 'datetime'
        
    '''
        if tag=='prices':
        while True:
            try:
                # Store the prompt in a variable
                prompt = "For food prices: \n Enter 1 to search by product name (eg. Bitterleaf) \n Enter 2 to search by observed date (eg. 03/03/2023) \n Enter 3 to search by market location (eg. Wuse, FCT Abuja) \n Enter 4 to search by market name (eg. Wuse Market) \n Enter here: "

                # Get the input from the user and store it in a variable
                r = int(input(prompt)) 

                r = int(input('For food prices: \n Enter 1 to search by product name (eg. Bitterleaf) \n Enter 2 to search by observed date (eg. 03/03/2023) \n Enter 3 to search by market location (eg. Wuse, FCT Abuja) \n Enter 4 to search by market name (eg. Wuse Market) \n Enter here: '))

                #return r,'prices'
        #r = request.args.get('r')
        #return prices_prompt()

                if r == '1':
                    x = searchByProductDesc()
                return str(x), 'prices' 
                if r==1:
                    x = searchByProductDesc()
                    #print(x)
                    return str(x), 'prices'
                elif r==2:
                    x = searchByDate()
                    #print(x)
                    return x, 'prices'
                elif r==3:
                    x = searchByLocation()
                    #print(x)
                    return x, 'prices'
                elif r==4:
                    x = searchByMarketName()
                    #print(x)
                    return x, 'prices'
            except ValueError:
                print ("Sorry your input must be a number")
            #continue
                    
        
        #print(str(r))
        #return r, 'prices'
        '''


    if tag=='weather':
        x=''
        api_key='987f44e8c16780be8c85e25a409ed07b'
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        # city_name = input("Enter city name : ")
        city_name = text.split(':')[1].strip()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        response=response.json()
        pres_temp=round(response['main']['temp']-273,2)
        feels_temp=round(response['main']['feels_like']-273,2)
        cond=response['weather'][0]['main']
        x+='Present temp.:'+str(pres_temp)+'C. Feels like:'+str(feels_temp)+'C. '+str(cond)
        print(x)
        return x,'weather'

    if tag=='news':
        main_url = " http://newsapi.org/v2/top-headlines?country=in&apiKey=bc88c2e1ddd440d1be2cb0788d027ae2"
        open_news_page = requests.get(main_url).json()
        article = open_news_page["articles"]
        results = []
        x=''
        for ar in article:
            results.append([ar["title"],ar["url"]])

        for i in range(10):
            x+=(str(i + 1))
            x+='. '+str(results[i][0])
            x+=(str(results[i][1]))
            if i!=9:
                x+='\n'

        return x,'news'

    if tag=='cricket':
        c = Cricbuzz()
        matches = c.matches()
        for match in matches:
            print(match['srs'],' ',match['mnum'],' ',match['status'])

    if tag=='song':
        chart=billboard.ChartData('hot-100')
        x='The top 10 songs at the moment are: \n'
        for i in range(10):
            song=chart[i]
            x+=str(i+1)+'. '+str(song.title)+'- '+str(song.artist)
            if i!=9:
                x+='\n'
        return x,'songs'

    if tag=='timer':
        #mixer.init()
        x=text.split(':')[1].strip()
        time.sleep(float(x)*60)
        mixer.music.load('Handbell-ringing-sound-effect.mp3')
        mixer.music.play()
        x='Timer ringing...'
        return x,'timer'


    if tag=='covid19':

        covid19=COVID19Py.COVID19(data_source='jhu')
        country=text.split(':')[1].strip()
        x=''
        if country.lower()=='world':
            latest_world=covid19.getLatest()
            x+='Confirmed Cases:'+str(latest_world['confirmed'])+' Deaths:'+str(latest_world['deaths'])
            return x,'covid19'
        else:
            latest=covid19.getLocations()
            latest_conf=[]
            latest_deaths=[]
            for i in range(len(latest)):

                if latest[i]['country'].lower()== country.lower():
                    latest_conf.append(latest[i]['latest']['confirmed'])
                    latest_deaths.append(latest[i]['latest']['deaths'])
            latest_conf=np.array(latest_conf)
            latest_deaths=np.array(latest_deaths)
            x+='Confirmed Cases:'+str(np.sum(latest_conf))+' Deaths:'+str(np.sum(latest_deaths))
            return x,'covid19'

    list_of_intents= intents_json['intents']
    for i in list_of_intents:
        if tag==i['tag'] :
            result= random.choice(i['responses'])
    return result,tag


def response(text):
    return_list=predict_class(text,model)
    response,_=get_response(return_list,intents,text)
    return response

'''@app.route('/login')
def login():
    return render_template(login.html)

from flask import Flask, request, redirect, render_template
app = Flask(__name__)'''

# Load user data from JSON file
@app.route('/login', methods=["GET", "POST"])
def login():
    # Load the users data from the JSON file
    with open("users.json", "r") as f:
        users = json.load(f)

    # Check if the form data was submitted
    if request.method == "POST":
        # Get the username and password from the form data
        username = request.form["username"]
        password = request.form["password"]

        # Check if the username and password are valid
        if username in users and users[username] == password:
            # Redirect the user to the next page
            return redirect("/home")
        else:
            # Show an error message
            return render_template("login.html", error="💩 Invalid username or password")

    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Load the users data from the JSON file
    with open("users.json", "r") as f:
        users = json.load(f)

    # Check if the form data was submitted
    if request.method == "POST":
        # Get the username and password from the form data
        username = request.form["username"]
        password = request.form["password"]

        # Check if the username already exists
        if username in users:
            # Show an error message
            return render_template("signup.html", error="Username already exists")
        else:
            # Add the new user to the users data
            users[username] = password

            # Save the updated users data to the JSON file
            with open("users.json", "w") as f:
                json.dump(users, f)

            # Redirect the user to the login page
            return redirect("/login")

    return render_template('signup.html')

#@app.route('/home')
#def home():
#    return "Welcome to the home page!"

@app.route('/',methods=['GET','POST'])
#@app.route('/home',methods=['GET','POST'])
def yo():
    return render_template('main.html')



'''with open('chatbot_codes/users.json', 'r') as f:
    users = json.load(f)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # Create a new user account
    users[username] = {'email': email, 'password': password}
    # Save user data to JSON file
    with open('chatbot_codes/users.json', 'w') as f:
        json.dump(users, f)
    return "Account created!"

@app.route('/', methods=["GET", "POST"])
def login():
    return render_template('login.html')

  # Get the username and password from the form data
    username = request.form["username"]
    password = request.form["password"]

  # Check if the username and password are valid
    if username in users and users[username] == password:
    # Redirect the user to the next page
        return redirect("/home")
    else:
    # Show an error message
        return render_template("login.html", error="💩 Invalid username or password")
'''

@app.route('/chat',methods=['GET','POST'])
#@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route("/get",methods=['GET','POST'])
def chatbot():
    userText = request.args.get('msg')
    resp=response(userText)
    return resp


""" @app.route("/get_data",methods=['GET'])
def get_data():
    '''data=[]
    with open('chatbot_codes\GeneralProductPricing.csv','r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)'''        
    user_txt = str(escape(request.args.get('msg')))
    res=response(user_txt) 
    
    r = int(input('For food prices: \n Enter 1 to search by product name (eg. Bitterleaf) \n Enter 2 to search by observed date (eg. 03/03/2023) \n Enter 3 to search by market location (eg. Wuse, FCT Abuja) \n Enter 4 to search by market name (eg. Wuse Market) \n Enter here: '))

    return r
    
    if r==1:
            res = searchByProductDesc()
            #print(x)
            return str(res), 'prices'
    elif r==2:
            x = searchByDate()
            #print(x)
            return x, 'prices'
    elif r==3:
            x = searchByLocation()
            #print(x)
            return x, 'prices'
    elif r==4:
            x = searchByMarketName()
            #print(x)
            return x, 'prices'
    else:
            res = 'Sorry, invalid input! For food prices: \n Enter 1 to search by product name (eg. Bitterleaf) \n Enter 2 to search by observed date (eg. 03/03/2023) \n Enter 3 to search by market location (eg. Wuse, FCT Abuja) \n Enter 4 to search by market name (eg. Wuse Market) \n Try again! '
            #print(x)
            return res, 'prices'

    return str(res) """
