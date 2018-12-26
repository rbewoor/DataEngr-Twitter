# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 16:26:19 2018

@author: RB

# access all the data stored into the mongoDB and do data analysis to answer some questions
"""
import pymongo
from pymongo import MongoClient
#from json import loads
from datetime import datetime

print('\nStartTime is:',datetime.now().strftime("%c"))

client = MongoClient('localhost:27017')
#dbName = client['TwitterDb2']
#colName = dbName['TwitterCol2']
dbName = client.TwitterDb2
collection = dbName.TwitterCol2
 
#Query 1
#Show the top 10 handles by NUMBER OF TWEETS BY USER AS MAINTAINED IN TWITTER RECORDS - NOT BASED ON ACTUAL NUMBER OF TWEETS DOWNLOADED VIA API (what shows on the top of the users profile)
#CursorTop10ByNoOfTweets = collection.find({},{"_id" :0, "user.screen_name" :1, "user.statuses_count" :1}).sort({"user.statuses_count": -1}).limit(10)
CursorTop10ByNoOfTweets = collection.find({},{"_id" :0, "user.screen_name" :1, "user.statuses_count" :1}).sort([("user.statuses_count", -1)]).limit(10)

for cursor1 in CursorTop10ByNoOfTweets:
    print(cursor1)



print('\nEndTime is:',datetime.now().strftime("%c"))
#cursorTop10ByNoOfTweets =
#db.TwitterCol1.find( {}, {"_id" :0, "user.screen_name" :1, "user.statuses_count" :1} ).sort({"user.statuses_count": -1}).limit(10)

#retDoc = colName.find_one()

#retDocUser = retDoc['user']

#print('\nDocument field created_at value is:', retDoc['created_at'])
#print('\nDocument field user.screen_name value is:', retDocUser['screen_name'])

#keys = retDoc.keys()

#print('\n\nFull document:',retDoc,'\n\n')

#keys_str = str(keys)

