# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 20:31:21 2018

@author: RB
"""
# copied from https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1

#from kafka import KafkaConsumer
from pymongo import MongoClient
#from json import loads


client = MongoClient('localhost:27017')
collection = client.TwitterDb1.Timepass1

message = {"name":"Rohit Bewoor","age": 37}
collection.insert_one(message)
#print('{} added to {}'.format(message, collection))
print('\nDone')