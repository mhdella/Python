
# Description: This is a 'self learning' chatbot program

"""
 I will show you how to build your very own chat bot using the Python programming language and Machine Learning! 
More specifically I want to create a "Doctor Chat Bot On Chronic Kidney Disease",
meaning I can ask this chat bot about chronic kidney disease, and it can come up with a reasonable response.

A chat bot is software that conducts conversations.
There are broadly two variants of chat bots: Rule-Based and Self Learning.
A Rule-Based chat bot is a bot that answers questions based on some rules that it is trained on, 
while a Self Learning chat bot is a chat bot that uses some Machine Learning based technique to chat. 
We will use a little bit of both.


Your kidneys filter wastes and excess fluids.
Chronic kidney disease, also called chronic kidney failure, describes the gradual loss of kidney function.

"""

#Resources: 
# (1) https://github.com/randerson112358/Building-a-Simple-Chatbot-in-Python-using-NLTK
# (2) https://medium.com/datadriveninvestor/build-your-own-chat-bot-using-python-95fdaaed620f
# (3) https://medium.com/@randerson112358/build-a-movie-recommendation-engine-using-python-scikit-learn-machine-learning-e68ba297e163

pip install nltk

pip install newspaper3k

#import libraries
from newspaper import Article
import random
import string 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import warnings
warnings.filterwarnings('ignore') #ignore any warning messages

nltk.download('punkt', quiet=True) # Download the punkt package
nltk.download('wordnet', quiet=True) # Download the wordnet package

#Get the article URL
article = Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download() #Download the article
article.parse() #Parse the article
article.nlp() #Apply Natural Language Processing (NLP)
corpus = article.text #Store the article text into a corpus

print(corpus)

#Tokenization
text = corpus
sent_tokens = nltk.sent_tokenize(text)# convert the txt to a list of sentences

#Print the list of sentences
print(sent_tokens)

#Create a dictionary (key:value pair) to remove punctuations  
remove_punct_dict = dict(  (ord(punct), None) for punct in string.punctuation)

print(remove_punct_dict)

#Create a function to return a list of lemmatized lower case words after removing punctuations 
def LemNormalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))

print( nltk.word_tokenize(text.lower().translate(remove_punct_dict)) )

# Keyword Matching
#Greeting input from the user
GREETING_INPUTS = ["hi", "hello",  "hola", "greetings",  "wassup","hey"] 
#Greeting responses back to the user
GREETING_RESPONSES = ["howdy","hi", "hey", "what's good",  "hello","hey there"]
#Function to return a random greeting response to a users greeting
def greeting(sentence):
   #If user's input is a greeting, return a randomly chosen greeting response
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Generating response
def response(user_response):
    #Set the chatBot response to an empty string
    robo_response=''
    
    #Append the users response to the sentence list
    sent_tokens.append(user_response) 
    
    #Convert a collection of documents/text to a matrix of Term Frequency-Inverse Document Frequency (TF-IDF) features. NOTE: Stop Words: A stop word is a commonly used word (such as “the”, “a”, “an”, “in”) that a search engine has been programmed to ignore, both when indexing entries for searching and when retrieving them as the result of a search query.
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english') 
    
    #Learn vocabulary and idf, return term-document matrix
    #Tf-IDF weight is a weight often used in information retrieval and text mining. 
    #This weight is a statistical measure used to evaluate how important a word is to a document in a collection or corpus
    tfidf = TfidfVec.fit_transform(sent_tokens)
    
    
    #Get the measure of similarity (similarity scores) between these two vectors, the users response at position -1 and the rest of the text/sentence tokens converted to TF-IDF
    vals = cosine_similarity(tfidf[-1], tfidf) 
    
    #Sort the similarity scores in an array of indices of the same shape and return the second to last index.
    #Note: The most similar score will be at the last index located at position -1, which is the users response, so the next best is at location -2
    #Note2: We are basically getting the index of the most similar text/sentence to the users response
    idx=vals.argsort()[0][-2] 
    
    #Reduce the dimensionality of vals, a matrix (or list of lists) to a single list
    flat = vals.flatten()
   
    #Sort the list in ascending order
    flat.sort()
   
    #Set this variable equal to the most similar score to the users response,
    # that's not the reponse itself at position -1, so the next best is at location -2
    req_tfidf = flat[-2]
    
    #If the variable is 0 then the best similarity score is 0, meaning their is no text similar to the users response
    if(req_tfidf==0):
        robo_response=robo_response+"I apologize, I don't understand." #If there are no similarities then send this response
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx] #Respond back to the user with the most similar sentence located at position idx
        return robo_response

#Set a flag to true for the while loop, the while loop will stop when the flag is false
flag=True
print("DOCBOT: I am DOCTOR BOT or DOCBOT for short. I will answer your queries about Chronic Kidney Disease. If you want to exit, type Bye!")
while(flag==True):
    user_response = input() #Get the users input
    user_response=user_response.lower() #Convert the users input to all lower case letters
    if(user_response!='bye'): # if the users response is not bye
        if(user_response=='thanks' or user_response=='thank you' ): #Check if the users response is thanks or thank you
            flag=False #Set the flag to false to end the conversation / while loop
            print("DOCBOT: You're welcome !") #If the users response was thanks ot thank you then have the bot print You're welcome
        else:
            if(greeting(user_response)!=None):
                print("DOCBOT: "+greeting(user_response))
            else:
                print("DOCBOT: ",end="")
                print(response(user_response)) #Get a response from the text that the bot will use
                sent_tokens.remove(user_response) #Remove the users response from the list
    else: #Else the users response was bye
        flag=False #Set the flag to false to end the conversation / while loop
        print("DOCBOT: Chat with you later !")    #print Chat with you later ! to the screen