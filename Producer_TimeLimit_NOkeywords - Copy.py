# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 19:42:25 2018

Enter the credentials of your twitter.
No filter and pull whatever twitter has. Program runs for specified no. of seconds

@author: RB
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
from kafka import SimpleProducer, KafkaClient
from datetime import datetime

access_token = ""
access_token_secret =  ""
consumer_key =  ""
consumer_secret =  ""

StartTime = datetime.now()
print('\nTime is:',StartTime.strftime("%c"))

class StdOutListener(StreamListener):
    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            producer.send_messages("TwitterTopic1", data.encode('utf-8'))
#            print (data)
            return True
        else:
            print
            return False
        
    def on_error(self, status):
        print (status)
    
    def __init__(self, time_limit=3):     # SPECIFY THE TIME IN SECONDS
        self.start_time = time.time()
        self.limit = time_limit
        super(StdOutListener, self).__init__()

kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.sample()

EndTime = datetime.now()
print('\nDone processing at:',EndTime.strftime("%c"))