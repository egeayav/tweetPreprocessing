import os
import tweepy as tw
from credentials import *
import pandas as pd
import re
from nltk.tokenize import TweetTokenizer
#pip install ekphrasis
#pip install tweet-preprocessor
import preprocessor as p
import threading
import time
import sys
import random
import webview

TW_NUM=250

class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False
        self.auth = tw.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.tapi = tw.API(self.auth, wait_on_rate_limit=True)
        self.index = 0
        self.tweets={}
        self.cleaned={}

    def init(self):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response

    def get(self,search):
        self.rawtweets = tw.Cursor(self.tapi.search,
              q=search,
              lang="en",
              since="2019-01-01").items(TW_NUM)
    
        p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.HASHTAG, p.OPT.SMILEY, p.OPT.MENTION, p.OPT.NUMBER)
    

        i=0
        for self.tweet in self.rawtweets:
            #print("************************************"),
            #print("***Text: ",tweet.text)
            self.tweets[i]=self.tweet.text
            t=p.clean(self.tweet.text)
            self.cleaned[i]=t
            i=i+1

        response = {'message': '{0} tweet indirildi'.format(TW_NUM),'index': '{0}'.format(self.index+1),'original':self.tweets[self.index],'cleaned':self.cleaned[self.index]}        
        
        self.index = self.index + 1
        
        return response
    
   
    def positive(self):

        with open("positive.csv","a") as myfile:
            myfile.write(self.cleaned[self.index]+"\n")
            
        response = {'message':'Tweet #{0} kaydedildi.'.format(self.index) ,'index': '{0}'.format(self.index+1),'original':self.tweets[self.index],'cleaned':self.cleaned[self.index]}        
         
        
        self.index = self.index + 1        
        return response

    def negative(self):
        
        with open("negative.csv","a") as myfile:
            myfile.write(self.cleaned[self.index]+"\n")
            
        response = {'message':'Tweet #{0} kaydedildi.'.format(self.index) ,'index': '{0}'.format(self.index+1),'original':self.tweets[self.index],'cleaned':self.cleaned[self.index]}        
         
        
        self.index = self.index + 1        
        return response
    
         
    def none(self):
        
        with open("none.csv","a") as myfile:
            myfile.write(self.cleaned[self.index]+"\n")
            
        response = {'message':'Tweet #{0} kaydedildi.'.format(self.index) ,'index': '{0}'.format(self.index+1),'original':self.tweets[self.index],'cleaned':self.cleaned[self.index]}        
         
        
        self.index = self.index + 1        
        return response
    
         

    def error(self):
        raise Exception('This is a Python exception')

twitter_html='''
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">
<style>
body {background-color: #D8D8D8;}
.button {
  border: none;
  color: white;
  padding: 30px 64px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 32px;
  margin: 8px 4px;
  cursor: pointer;
}

.button1 {background-color: #ff0000;} /* Red */
.button2 {background-color: #008CBA;} /* Blue */
.button3 {background-color: #00FF00;} /* Green */
.button4 {background-color: #71078B;} /* Yellow */



</style>
<style>
    #response-container {
        display: none;
        padding: 1rem;
        margin: 1rem 2rem;
        font-size: 80%;
        border: 4px dashed #ccc;
    }
    #tweet-container {
        padding: 1rem;
        margin: 1rem 1rem;
        font-size: 80%;
        border: 1px solid  #fff;
    }
    label {
        margin-left: 0.3rem;
        margin-right: 0.3rem;
    }
    button {
        font-size: 100%;
        padding: 0.5rem;
        margin: 0.3rem;
    }
</style>
</head>
<body>
<h1>Tweet Ön İşleme</h1>
<!--<p id='pywebview-status'><i>pywebview</i> is not ready</p>-->
<!--<button onClick="initialize()">Hello Python</button><br/>-->


<label for="keyword">Kelime Arayın:</label>&nbsp;&nbsp;&nbsp;
<input type="text" id="keyword" name="keyword" placeholder="Aranacak Kelime Girin">
<button class="button2" onClick="get()" type="button">Tweetleri Çek</button><br><br>

<div id="tweet-container">
<strong>Tweet Sayısı:</strong><span id="tweetnumber" name="Tweet Sayısı"></span>
<br>

<strong>Orijinal:</strong>&nbsp;&nbsp;&nbsp;<span id="original" name="original">&nbsp;</span><br>

<strong>Temizlenmiş:</strong>&nbsp;&nbsp;&nbsp;<span  id="cleaned" name="cleaned">&nbsp;</span><br>
</div>


<button class="button button3" onClick="positive()" type="button">Pozitif</button>
<button class="button button1" onClick="negative()" type="button">Negatif</button>
<button class="button button4" onClick="none()" type="button">Hiçbiri</button>

<div id="response-container"></div>
<script>
    window.addEventListener('pywebviewready', function() {
        var container = document.getElementById('pywebview-status')
        container.innerHTML = '<i>pywebview</i> is ready'
    })
    function showResponse(response) {
        var container = document.getElementById('response-container')
        container.innerText = response.message
        container.style.display = 'block'
        
        if(response.index!=-1){
            var container = document.getElementById('tweetnumber')
            container.innerText = response.index
            container.style.display = 'block'
            var container = document.getElementById('original')
            container.innerText = response.original
            container.style.display = 'block'
            var container = document.getElementById('cleaned')
            container.innerText = response.cleaned
            container.style.display = 'block'        
        }
        
        
    }
   
    
    function initialize() {
        pywebview.api.init().then(showResponse)
    }
    
    function getRandomNumber() {
        pywebview.api.getRandomNumber().then(showResponse)
    }
    function get() {
        var search = document.getElementById('keyword').value;

        pywebview.api.get(search).then(showResponse)
        
        //pywebview.api.selectTweet().then(showTweet)
        
    }
    function positive() {
        pywebview.api.positive().then(showResponse)
    }
    function negative() {
        pywebview.api.negative().then(showResponse)
    }
    function none() {
        pywebview.api.none().then(showResponse)
    }
    
    function catchException() {
        pywebview.api.error().catch(showResponse)
    }
</script>
</body>
</html>
'''

if __name__ == '__main__':
    api = Api()
    window = webview.create_window('Tweet Ön İşleme', html=twitter_html, js_api=api, min_size=(1000,520))
    webview.start()
