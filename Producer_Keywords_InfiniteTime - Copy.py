# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 19:42:25 2018

@author: RB
"""
# copied from https://www.bmc.com/blogs/working-streaming-twitter-data-using-kafka/

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient

access_token = ""
access_token_secret =  ""
consumer_key =  ""
consumer_secret =  ""

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("TwitterTopic1", data.encode('utf-8'))
        print (data)
        return True
    def on_error(self, status):
        print (status)

kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track=["donald trump", "hillary clinton", "barack obama", "bernie sanders"])