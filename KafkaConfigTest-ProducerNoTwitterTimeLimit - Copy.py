# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 17:11:08 2018

@author: RB
"""
# -*- coding: utf-8 -*-
#from tweepy.streaming import StreamListener
#from tweepy import OAuthHandler
#from tweepy import Stream
from kafka import KafkaProducer
from datetime import datetime
import time
import random

print('\nProducer program START time:',datetime.now().strftime("%c"))

MsgGenTimeLimit = 15          # specify time in seconds
MsgGenSleepTime = 0.5        # time in seconds to prevent very fast msg generations
msgKey = 100

topicName = 'TestTopic3'
producer = KafkaProducer(bootstrap_servers='localhost:9092')
LoopNumber = 1
MaxLoops = 8
EndLoopSleepTime = 15    # time in seconds

while LoopNumber < (MaxLoops+1):
    print('STARTING loop # %d ----------'%(LoopNumber))
    loopStartTime = time.time()
    while (time.time() - loopStartTime) < MsgGenTimeLimit:
        msgToSend = ''
        for i in range(0,3):
            msgToSend = msgToSend + chr(random.randint(97,122))
        msgToSend = msgToSend + str(msgKey)
        producer.send(topicName, key=str(msgKey).encode('utf-8'), value=msgToSend.encode('utf-8'))
        print('Msg sent to Kafka::: ',msgToSend)
        msgKey = msgKey + 1
        time.sleep(MsgGenSleepTime)
    #--------- sleep for a bit
    print('STARTING SLEEP for %d secs loop # %d ----------'%(EndLoopSleepTime, LoopNumber))
    time.sleep(EndLoopSleepTime)
    print('FINISHED loop # %d ----------'%(LoopNumber))
    LoopNumber = LoopNumber + 1

print('\nProducer program END time:',datetime.now().strftime("%c"))