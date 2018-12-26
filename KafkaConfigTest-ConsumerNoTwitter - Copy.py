# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 14:51:45 2018

@author: RB
"""

from kafka import KafkaConsumer
#from pymongo import MongoClient
#from json import loads
from datetime import datetime

countDocsWritten = 0

print('\nStart time of consuming program: ', datetime.now().strftime("%c"))

topicName = 'TestTopic4'
runningFlag = True
LoopNumber = 1
userInpDecision = ''

while runningFlag:
    consumer = KafkaConsumer(
    #        topicName,
            bootstrap_servers=['localhost:9092'],
    #        group_id = 'test-consumer-group',
    #        auto_offset_reset='earliest',
    #        auto_offset_reset='latest',
            enable_auto_commit = False,
            consumer_timeout_ms= 3 * 1000
            )
    
    consumer.subscribe(topicName)
    
    print('FOR ENTRY loop number %d time: '%(LoopNumber), datetime.now().strftime("%c"))
    for message in consumer:
        print (message.value)
        consumer.commit()
    
    print('FOR EXIT loop number %d at: '%(LoopNumber),datetime.now().strftime("%c"))
    LoopNumber = LoopNumber + 1
    userInpDecision = input("\nStill proceed? Enter y or n:: ")
    if userInpDecision in ['y','Y']:
        continue
    else:
        runningFlag = False
          

print('\nFINAL Exit from Program at: ',datetime.now().strftime("%c"))

#client = MongoClient('localhost:27017')
#collection = client.TestDB.TestCol1


#for message in consumer:
#    message = message.value
#    collection.insert_one(message)
#    countDocsWritten = countDocsWritten + 1
#    if (countDocsWritten % 250 == 0):
#        print('\nWritten %d th record' %(countDocsWritten))
#    print('\nWritten %d th record' %(countDocsWritten))
#    print('{} added to {}'.format(message, collection))

#print('\nWritten %d documents to MongoDb' %(countDocsWritten))
#EndTime = datetime.now()
#print('\nProgram exiting at:',EndTime.strftime("%c"))