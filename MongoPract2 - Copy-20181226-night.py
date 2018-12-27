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
import re

print('\nStartTime is:',datetime.now().strftime("%c"))

client = MongoClient('localhost:27017')
#dbName = client['TwitterDb1']
#colName = dbName['TwitterCol1']
dbName = client.TwitterDb1        # alternative way to code is:::  dbName = client['TwitterDb1']
collection = dbName.TwitterCol1   # alternative way to code is:::  collection = dbName['TwitterCol1']

#Query 0         Query 0         Query 0         Query 0
#Summary info: Total count of documents, Count of Create_type v/s Delete_type
#MONGOSHELL:
#   Total count: db.TwitterCol1.find().count()
#   Create_type count: db.TwitterCol1.find({"created_at": {$ne: null}}).count()
#   Delete_type count: db.TwitterCol1.find({"delete": {$ne: null}}).count()
#   Distinct Handles count BAD WAY: db.TwitterCol1.distinct("user.id_str").length
#   DISTINCT handles count GOOD WAY: db.TwitterCol1.aggregate({$group:{_id: '$user.id_str'}}, {$group: {_id: 1, count: {$sum: 1} } } )
TotalDocsCount = collection.count_documents({})
TotalDocsCreateType = collection.count_documents({"created_at": {"$ne": None}})
TotalDocsDeleteType = collection.count_documents({"delete": {"$ne": None}})
#TotalDistinctUsers = collection.distinct("user.id_str").length
pipelineQuery0 =[{"$group":{"_id": "$user.id_str"}}, {"$group": {"_id": 1, "count": {"$sum": 1} } }]
TotalDistinctUsers1 = collection.aggregate(pipelineQuery0)
print('Database Info summary: Total documents = %d, create_type = %d , delete_type = %d, '%(TotalDocsCount, TotalDocsCreateType, TotalDocsDeleteType))
print('Number of Distinct Handles = %d', %( TotalDistinctUsers1["count"] ))

#Query 1         Query 1         Query 1         Query 1
#Top 10 handles by NUMBER OF TWEETS BY USER AS MAINTAINED IN TWITTER RECORDS - NOT BASED ON ACTUAL NUMBER OF TWEETS DOWNLOADED VIA API (from statuses_count field in "user" field)
print('\nQuery 1 Top 10 Handles by Total Tweets+Retweets count:')
#MONGOSHELL: find({{"created_at": {$ne: null}},{"_id" :0, "user.screen_name" :1, "user.statuses_count" :1}).sort({"user.statuses_count": -1}).limit(10)
CursorTop10HandlesByTotalTweetsCount = collection.find({"created_at": {"$ne": None}},{"_id" :0, "user.screen_name" :1, "user.statuses_count" :1}).sort([("user.statuses_count", -1)]).limit(10)
for cursor in CursorTop10HandlesByTotalTweetsCount:
    print(cursor)
CursorTop10HandlesByTotalTweetsCount.close()

#Query 2         Query 2         Query 2         Query 2
#Top 10 TWEETS by the number of LIKES FOR TWEETS
print('\nQuery 2 Top 10 Handles by Tweet Likes count:')
#MONGOSHELL: find({"created_at": {$ne: null}},{"_id": 0, "user.screen_name": 1 ,"favorite_count": 1}).sort({"favorite_count": -1}).limit(10)
CursorTop10HandlesByTweetLikesCount = collection.find( {"created_at": {"$ne": None}},{"_id": 0, "user.screen_name": 1 ,"favorite_count": 1, "text": 1}).sort([("favorite_count", -1)]).limit(10)
for cursor in CursorTop10HandlesByTweetLikesCount:
    print(cursor)
CursorTop10HandlesByTweetLikesCount.close()

#Query 3         Query 3         Query 3         Query 3
#Top 10 handles by the number of LIKES FOR USER
print('\nQuery 3 answer:')
#MONGOSHELL: find( {}, {"_id" :0, "user.screen_name" :1, "user.favourites_count" :1} ).sort({"user.favourites_count": -1}).limit(10)
CursorTop10HandlesByUserLikesCount = collection.find( {}, {"_id" :0, "user.screen_name" :1, "user.favourites_count" :1} ).sort([("user.favourites_count", -1)]).limit(10)
for cursor in CursorTop10HandlesByUserLikesCount:
    print(cursor)
CursorTop10HandlesByUserLikesCount.close()

#Query 4         Query 4         Query 4         Query 4
#Total COUNT OF RETWEETS in the pulled data
print('\nQuery 4 answer:')
#MONGOSHELL: find({"text": {$regex: /^RT /}}).count()
TotalRetweetsInDbData = collection.count_documents({ "text": {"$regex": "^RT "} })
print('Total count of Retweets in database = %d'%(TotalRetweetsInDbData))

#Query 5         Query 5         Query 5         Query 5
#Top 10 handles by number of tweets - BASED ON THE DATA PULLED into the database (NOT like the previous QUERY)
print('\nQuery 5 answer:')
#MONGOSHELL: find
CursorXXXX = collection.find
for cursor in CursorXXXX:
    print(cursor)
CursorXXXX.close()

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

