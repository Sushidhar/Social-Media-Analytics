# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 00:35:09 2017

@author: Sushidhar
"""

from twython import TwythonStreamer
import json
import re
import time
tweets = []

class MyStreamer(TwythonStreamer):
 
    def on_success(self, data):
        if 'lang' in data and data['lang'] == 'en':
            tweets.append(data)
#            self.loadAndDumpJson(data,'10K')  #Uncomment and comment if conditions to collect 10K tweets
            if data['user']['location'] != None:
                if self.findWholeWord('ca')(data['user']['location'].lower()) or self.findWholeWord('california')(data['user']['location'].lower()):
                    self.loadAndDumpJson(data,'CA')
                    
                elif self.findWholeWord('ny')(data['user']['location'].lower()) or self.findWholeWord('new york')(data['user']['location'].lower()):
                    self.loadAndDumpJson(data,'NY')
                    
                elif self.findWholeWord('tx')(data['user']['location'].lower()) or self.findWholeWord('texas')(data['user']['location'].lower()):    
                    self.loadAndDumpJson(data,'TX')
                    
                elif self.findWholeWord('az')(data['user']['location'].lower()) or self.findWholeWord('arizona')(data['user']['location'].lower()):
                    self.loadAndDumpJson(data,'AZ')
                    
                elif self.findWholeWord('fl')(data['user']['location'].lower()) or self.findWholeWord('florida')(data['user']['location'].lower()):
                    self.loadAndDumpJson(data,'FL')
                    
            
    def loadAndDumpJson(self,data,state):
        fileName = 'tweet_stream_{}.json'.format(state)
        with open(fileName) as f:
            dataJson = json.load(f)
        dataJson.append(data)
        with open(fileName, 'w') as f:
            json.dump(dataJson, f, indent=4)
        
    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()
 
    def findWholeWord(self,w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

 
if __name__ == '__main__':
    
    APP_KEY = "7SlvJXbh9RfzNfCsXSwTHAUaU"
    APP_SECRET =  "lxzADa4FKb13pjmHeh1SGpdyXnVcy9RWNr512s7LPyi2uubBcJ"
    OAUTH_TOKEN = "1538734669-jgM3RsoYwGGEuSSonE296i63vTDaDzR9ynxk8MO"
    OAUTH_TOKEN_SECRET = "RTQDVGXg0iQ54Qa958U0N8wI9F5aGSp0PTknD3MUNgSYA"
    while len(tweets) <= 10000:
        try:
            stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
            stream.statuses.filter(track='trump')
        except:
            time.sleep(30)
            continue