# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 14:54:39 2018

@author: RB
"""

#from tweepy.streaming import StreamListener
#from tweepy import OAuthHandler
#from tweepy import Stream
from kafka import KafkaProducer
from datetime import datetime

StartTime = datetime.now()
print('\nStart time is:',StartTime.strftime("%c"))

topicName = 'TestTopic2'
producer = KafkaProducer(bootstrap_servers='localhost:9092')

keepProducingFlag = True
startKey = 1

while keepProducingFlag:
    msgFromUser = input("\nEnter your message to send Kafka:\n")
    if str(msgFromUser) == 'exit':
        keepProducingFlag = False
    else:
        msgToSend = str(msgFromUser)
        producer.send(topicName, key=str(startKey).encode('utf-8'), value=msgToSend.encode('utf-8'))
        startKey = startKey + 1

#producer.send_messages("TwitterTopic1", data.encode('utf-8'))
#producer.send(topicName, b'Hello, World!')
#producer.send(topicName, key=b'message-two', value=b'This is Kafka-Python')

EndTime = datetime.now()
print('\nDone processing at:',EndTime.strftime("%c"))