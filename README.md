# Samaritan, Food Chatbot

## About this Project
"Samaritan" is a proprietary NLP-based Chatbot assistant (like Chatgpt but for food) built using Python3 that will fetch (through prompt) our real-time, collected and researched pricing data (in all major currencies) of Africa's informal food markets and present them to users in a simplified way via question and answer format (prompts) on a web dashboard. It uses NLP and Deep-Learning to analyse the user's message, classify it into the a broader category and then reply with a suitable message or the required information. It is hosted using flask.


## Project UI
Home Page:

To run it locally on your system, follow these steps:
1. Clone this repository onto your system. On Command Prompt, run the following command:

```
git clone (https://github.com/Qoshawa/Chatbot.git)
```
2. Change your directory to Chatbot:
```
cd Chatbot
```
3. Make sure you have all the required libraries listed in requirements.txt. In case any of the libraries are missing, install them using pip. Type this command into your Command Prompt, replacing 'Your-library-name' by the required library name:
```
pip install requirements.txt
```
4. Then run the follwing commands to run the application:
```
set FLASK_APP=chatbot.py
python -m flask run
```

5. Enter the url provided after running the previous commands into your web browser

Samaritan is now ready to chat!


##### Copyright (c) 2023 The Barn Of Egypt

