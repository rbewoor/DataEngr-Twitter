# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 20:31:21 2018

Read the info from the Kafka topic and write to MongoDB
PROBLEM is this program runs TILL INFINITY AND DOES EXIT. MAYBE THIS IS THE ISSUE THAT IS CREATING RECORDS WITH NO DATA ??????????

@author: RB
"""
# copied from https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1

from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from datetime import datetime

countDocsWritten = 0
StartTime = datetime.now()
print('\nTime is:',StartTime.strftime("%c"))

consumer = KafkaConsumer(
    'TwitterTopic1',        # topic name in kafka
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
#     auto_commit_interval=50,
#     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))


client = MongoClient('localhost:27017')
collection = client.TwitterDb1.TwitterCol1


for message in consumer:
    message = message.value
#    if message == 
    collection.insert_one(message)
    countDocsWritten = countDocsWritten + 1
    print('\nWritten %d th record' %(countDocsWritten))
#    print('{} added to {}'.format(message, collection))

print('\nWritten %d documents to MongoDb' %(countDocsWritten))	# stupid thing never reaches this code and continues in the for loop above
EndTime = datetime.now()
print('\nDone processing at:',EndTime.strftime("%c"))