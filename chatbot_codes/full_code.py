
import keras
import nltk
import pickle
import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout,Activation
import random
import datetime
from googlesearch import *
import webbrowser
import requests
#from pycricbuzz import Cricbuzz (cricket news)
#import billboard
import time
from pygame import mixer
#import COVID19Py (covid19 results)
import csv
import io


from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()


words=[]
classes = []
documents = []
ignore_words = ['?','!',',',"'s"]
#data_file = io.open('chatbot_codes\intents.json', encoding='cp437').read()
#data_file = io.open('chatbot_codes\intents.json', encoding='utf8').read()
data_file = open('chatbot_codes\intents.json').read()
#data_file = io.open('chatbot_codes\intents.json', encoding='cp1252', errors='ignore').read()
#data_file = io.open('chatbot_codes\intents.json', encoding='latin1').read()
intents = json.loads(data_file)
csv_file=csv.reader(open('chatbot_codes/GeneralProductPricing.csv','r'))

for intent in intents['intents']:
    for pattern in intent['patterns']:
        #tokenize each word 
        w=nltk.word_tokenize(pattern)
        words.extend(w)
        #add documents in the corpus
        documents.append((w,intent['tag']))
        
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
# lemmaztize and lower each word and remove duplicates          
words=[lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_words]
words=sorted(list(set(words)))

# sort classes
classes=sorted(list(set(classes)))

# documents = combination between patterns and intents
print (len(documents), "documents")
# classes = intents
print (len(classes), "classes", classes)
# words = all words, vocabulary
print (len(words), "unique lemmatized words", words)

pickle.dump(words,open('chatbot_codes\words.pkl','wb'))
pickle.dump(classes,open('chatbot_codes\classes.pkl','wb'))

# create our training data
training = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag=[]
    # list of tokenized words for the pattern
    pattern = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern=[ lemmatizer.lemmatize(word.lower()) for word in pattern ]
    # create our bag of words array with 1, if word match found in current pattern
    for word in words:
        if word in pattern:
            bag.append(1)
        else:
            bag.append(0)
    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag,output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training=np.array(training)
#training = np.array(training, dtype=object)

# create train and test lists. X - patterns, Y - intents
X_train=list(training[:,0])
y_train=list(training[:,1])

# Create model - 3 layers. First layer 256 neurons, second layer 128 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model=Sequential()
model.add(Dense(1024, input_shape=(len(X_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(512, activation='relu'))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

# Compile model.
adam=tensorflow.keras.optimizers.Adam(0.001)
model.compile(optimizer=adam,loss='categorical_crossentropy',metrics=['accuracy'])
# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
#sgd: object = tf.keras.optimizers.legacy.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
#model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#fitting and saving the model
#model.fit(np.array(X_train),np.array(y_train),epochs=200,batch_size=10,verbose=1)
weights = model.fit(np.array(X_train),np.array(y_train),epochs=2000,batch_size=10,verbose=1)
model.save('chatbot_codes\mymodel.h5',weights)

print("model created and saved")

print(model.summary())

print("Done..You may proceed!")

from tensorflow.keras.models import load_model
model = load_model('chatbot_codes\mymodel.h5')
intents = json.loads(open('chatbot_codes\intents.json').read())
words = pickle.load(open('chatbot_codes\words.pkl','rb'))
classes = pickle.load(open('chatbot_codes\classes.pkl','rb'))


#Predict
def clean_up(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def create_bow(sentence, words):
    #def create_bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = list(np.zeros(len(words)))
    #bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                #if show_details:
                    #print ("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence,model):
    # filter out predictions below a threshold
    p = create_bow(sentence, words)
    #p = create_bow(sentence, words, show_details=False)
    res=model.predict(np.array([p]))[0]
    #predict class error threshold (0.1->0.9)
    threshold=0.9
    results = [[i,r] for i,r in enumerate(res) if r>threshold]
    # sort by strength of probability
    results.sort(key=lambda x: x[1],reverse=True)
    return_list=[]
    
    for result in results:
        return_list.append({'intent':classes[result[0]],'prob':str(result[1])})
    return return_list

def searchByProductDesc():
    product=input('Enter food item name\n')
    csv_file=csv.reader(open('chatbot_codes/GeneralProductPricing.csv','r'))

    for row in csv_file:
        if product==row[2]:
            c=str(print(', '.join(row)))
    return c

def searchByDate():
    product=input('Enter observed date of food prices\n')
    csv_file=csv.reader(open('chatbot_codes/GeneralProductPricing.csv','r'))

    for row in csv_file:
        if product==row[0]:
            c=str(print(', '.join(row)))
    return c

def searchByLocation():
    product=input('Enter the location of the market\n')
    csv_file=csv.reader(open('chatbot_codes/GeneralProductPricing.csv','r'))

    for row in csv_file:
        if product==row[4]:
            c=str(print(', '.join(row)))
    return c

def searchByMarketName():
    product=input('Enter the name of the market\n')
    csv_file=csv.reader(open('chatbot_codes/GeneralProductPricing.csv','r'))

    for row in csv_file:
        if product==row[5]:
            c=str(print(', '.join(row)))
    return c


def get_response(return_list, intents_json, text):
    
    if len(return_list)==0:
        tag='noanswer'
    else:    
        tag=return_list[0]['intent']

    if tag=='datetime':        
        print(time.strftime("%A"))
        print (time.strftime("%d %B %Y"))
        print (time.strftime("%H:%M:%S"))

    if tag=='prices':
        
        r = int(input('For food prices: \n Enter 1 to search by product name (eg. Bitterleaf) \n Enter 2 to search by observed date (eg. 03/03/2023) \n Enter 3 to search by market location (eg. Wuse, FCT Abuja) \n Enter 4 to search by market name (eg. Wuse Market) \n Enter here: '))

        print (r)

        if r==1:
            x = searchByProductDesc()
            #print(x)
            print (x)
        elif r==2:
            x = searchByDate()
            #print(x)
            print (x)
        elif r==3:
            x = searchByLocation()
            #print(x)
            print (x)
        elif r==4:
            x = searchByMarketName()
            #print(x)
            print (x)
        else:
            x = 'Sorry, invalid input! For food prices: \n Enter 1 to search by product name (eg. Bitterleaf) \n Enter 2 to search by observed date (eg. 03/03/2023) \n Enter 3 to search by market location (eg. Wuse, FCT Abuja) \n Enter 4 to search by market name (eg. Wuse Market) \n Try again! '
            #print(x)
            print (x)

    if tag=='google':
        query=input('Enter query...')
        chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
        for url in search(query, tld="co.in", num=1, stop = 1, pause = 2):
            webbrowser.open("https://google.com/search?q=%s" % query)
    if tag=='weather':
        api_key='987f44e8c16780be8c85e25a409ed07b'
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = input("Enter city name : ")
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url) 
        x=response.json()
        print('Present temp.: ',round(x['main']['temp']-273,2),'celcius ')
        print('Feels Like:: ',round(x['main']['feels_like']-273,2),'celcius ')
        print(x['weather'][0]['main'])
        
    if tag=='news':
        main_url = " http://newsapi.org/v2/top-headlines?country=in&apiKey=bc88c2e1ddd440d1be2cb0788d027ae2"
        open_news_page = requests.get(main_url).json()
        article = open_news_page["articles"]
        results = [] 
          
        for ar in article: 
            results.append([ar["title"],ar["url"]]) 
          
        for i in range(10): 
            print(i + 1, results[i][0])
            print(results[i][1],'\n')
            
    #if tag=='cricket':
    #    c = Cricbuzz()
    #    matches = c.matches()
    #    for match in matches:
    #        print(match['srs'],' ',match['mnum'],' ',match['status'])
    
    #if tag=='song':
    #    chart=billboard.ChartData('hot-100')
    #    print('The top 10 songs at the moment are:')
    #    for i in range(10):
    #        song=chart[i]
    #        print(song.title,'- ',song.artist)
    if tag=='timer':        
        mixer.init()
        x=input('Minutes to timer..')
        time.sleep(float(x)*60)
        mixer.music.load('Handbell-ringing-sound-effect.mp3')
        mixer.music.play()
        
    #if tag=='covid19':
    #    
    #   covid19=COVID19Py.COVID19(data_source='jhu')
    #    country=input('Enter Location...')
    #    
    #    if country.lower()=='world':
    #        latest_world=covid19.getLatest()
    #        print('Confirmed:',latest_world['confirmed'],' Deaths:',latest_world['deaths'])
    #    
    #    else:
    #            
    #        latest=covid19.getLocations()
    #        
    #        latest_conf=[]
    #        latest_deaths=[]
    #        for i in range(len(latest)):
    #            
    #            if latest[i]['country'].lower()== country.lower():
    #                latest_conf.append(latest[i]['latest']['confirmed'])
    #                latest_deaths.append(latest[i]['latest']['deaths'])
    #        latest_conf=np.array(latest_conf)
    #        latest_deaths=np.array(latest_deaths)
    #        print('Confirmed: ',np.sum(latest_conf),'Deaths: ',np.sum(latest_deaths))

    list_of_intents= intents_json['intents']    
    for i in list_of_intents:
        if tag==i['tag']:
            result= random.choice(i['responses'])
    return result

def response(text):
    return_list = predict_class(text,model)
    response = get_response(return_list, intents)
    return response

while(1):
    x=input()
    print(response(x))
    if x.lower() in ['bye', 'Byeeee...','Goodbye..','Get lost','See you','See ya..','Its been a pleasure chatting']:  
        break


#Self learning
print('Help me Learn?')
tag=input('Please enter general category of your question  ')
flag=-1
for i in range(len(intents['intents'])):
    if tag.lower() in intents['intents'][i]['tag']:
        intents['intents'][i]['patterns'].append(input('Enter your message: '))
        intents['intents'][i]['responses'].append(input('Enter expected reply: '))        
        flag=1

if flag==-1:
    
    intents['intents'].append (
        {'tag':tag,
         'patterns': [input('Please enter your message')],
         'responses': [input('Enter expected reply')]})
    
with open('chatbot_codes\intents.json','w') as outfile:
    outfile.write(json.dumps(intents,indent=4))
