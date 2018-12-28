# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 16:26:19 2018

@author: RB

# access all the data stored into the mongoDB and do data analysis to answer some questions
"""
from pymongo import MongoClient
#from json import loads
from datetime import datetime

print('\nStartTime is:',datetime.now().strftime("%c"))

client = MongoClient('localhost:27017')
#dbName = client['TwitterDb1']
#colName = dbName['TwitterCol1']
dbName = client.TwitterDb1        # alternative way to code is:::  dbName = client['TwitterDb1']
collection = dbName.TwitterCol1   # alternative way to code is:::  collection = dbName['TwitterCol1']

#Query 0         Query 0         Query 0         Query 0
#Summary info: Total count of documents, Count of Create_type, Count of Delete_type, Count of Distinct Handles, Count of Tweets that are RETWEETS
#MONGOSHELL:
#   Total count: db.TwitterCol1.find().count()
#   Create_type count: db.TwitterCol1.find({"created_at": {$ne: null}}).count()
#   Create_type count ALTERNATIVE: db.TwitterCol1.find({"created_at": {"$exists": 1}}).count()
#   Delete_type count: db.TwitterCol1.find({"delete": {$ne: null}}).count()
#   Delete_type count ALTERNATIVE: db.TwitterCol1.find({"delete": {"$exists": 1}}).count()
#   Distinct Handles count BAD WAY: db.TwitterCol1.distinct("user.id_str").length
#   DISTINCT handles count GOOD WAY: db.TwitterCol1.aggregate({$group:{_id: '$user.id_str'}}, {$group: {_id: 1, count: {$sum: 1} } } )
#Total COUNT OF RETWEETS in the pulled data:   find({"text": {$regex: /^RT /}}).count()
TotalDocsCount = collection.count_documents({})
TotalDocsCreateType = collection.count_documents({"created_at": {"$exists": 1}})
TotalDocsDeleteType = collection.count_documents({"delete": {"$exists": 1}})
TotalRetweetsInDbData = collection.count_documents({ "text": {"$regex": "^RT "} })
pipelineQuery0 =[{"$group":{"_id": "$user.id_str"}}, {"$group": {"_id": 1, "count": {"$sum": 1} } }]
TotalDistinctUsersCursor = collection.aggregate(pipelineQuery0)

print('Database Info summary:::')
print('Total documents = %d, create_type docs = %d , delete_type docs = %d' %(TotalDocsCount, TotalDocsCreateType, TotalDocsDeleteType))
for cursor in TotalDistinctUsersCursor:
    print('Number of Distinct Handles = %d' %( cursor["count"] ))
TotalDistinctUsersCursor.close()
print('Total count of Retweets in database = %d'%(TotalRetweetsInDbData))

#Query 1         Query 1         Query 1         Query 1
#Top 10 handles by NUMBER OF TWEETS BY USER AS MAINTAINED IN TWITTER RECORDS - NOT BASED ON ACTUAL NUMBER OF TWEETS DOWNLOADED VIA API (from statuses_count field in "user" field)
print('\nQuery 1 Top 10 Handles by Total Tweets+Retweets count:')
#MONGOSHELL: db.TwitterCol1.find({{"created_at": {$ne: null}},{"_id" :0, "user.screen_name" :1, "user.statuses_count" :1}).sort({"user.statuses_count": -1}).limit(10)
CursorTop10HandlesByTotalTweetsCount = collection.find({"created_at": {"$ne": None}},{"_id" :0, "user.screen_name" :1, "user.statuses_count" :1}).sort([("user.statuses_count", -1)]).limit(10)
for cursor in CursorTop10HandlesByTotalTweetsCount:
    print(cursor)
CursorTop10HandlesByTotalTweetsCount.close()

#Query 2         Query 2         Query 2         Query 2
#Top 10 TWEETS by the number of LIKES FOR TWEETS
print('\nQuery 2 Top 10 Handles by Tweet Likes count:')
#MONGOSHELL: db.TwitterCol1.find({"created_at": {$ne: null}},{"_id": 0, "user.screen_name": 1 ,"favorite_count": 1}).sort({"favorite_count": -1}).limit(10)
CursorTop10HandlesByTweetLikesCount = collection.find( {"created_at": {"$ne": None}},{"_id": 0, "user.screen_name": 1 ,"favorite_count": 1, "text": 1}).sort([("favorite_count", -1)]).limit(10)
for cursor in CursorTop10HandlesByTweetLikesCount:
    print(cursor)
CursorTop10HandlesByTweetLikesCount.close()

#Query 3         Query 3         Query 3         Query 3
#Top 10 handles by the number of LIKES FOR USER
print('\nQuery 3 answer:')
#MONGOSHELL: db.TwitterCol1.find( {}, {"_id" :0, "user.screen_name" :1, "user.favourites_count" :1} ).sort({"user.favourites_count": -1}).limit(10)
CursorTop10HandlesByUserLikesCount = collection.find( {}, {"_id" :0, "user.screen_name" :1, "user.favourites_count" :1} ).sort([("user.favourites_count", -1)]).limit(10)
for cursor in CursorTop10HandlesByUserLikesCount:
    print(cursor)
CursorTop10HandlesByUserLikesCount.close()


#Query 4         Query 4         Query 4         Query 4
#Top 10 handles by number of tweets - BASED ON THE DATA PULLED into the database (NOT like the previous QUERY)
print('\nQuery 4 answer:')
#MONGOSHELL: db.TwitterCol1.aggregate( {$match: {"created_at": {$exists: 1}}}, {$group: {_id: "$user.screen_name", "NoOfTweets": {$sum: 1}} } , {$sort: {"NoOfTweets": -1}} , {$limit: 10} )
pipelineQuery4 = [ {"$match": {"created_at": {"$exists": 1}}} , {"$group": {"_id": "$user.screen_name", "NoOfTweets": {"$sum": 1}} } , {"$sort": {"NoOfTweets": -1}} , {"$limit": 10}]
CursorTop10HandlesByTotalTweets4mDataInDb = collection.aggregate(pipelineQuery4)
for cursor in CursorTop10HandlesByTotalTweets4mDataInDb:
    print(cursor)
CursorTop10HandlesByTotalTweets4mDataInDb.close()


#Query 5         Query 5         Query 5         Query 5
#Summarise the SOURCE type from the source field
print('\nQuery 5 answer:')
#MONGOSHELL: db.TwitterCol1.aggregate([{$match: {"created_at": {$exists: 1}, "source": {$regex: /Twitter Lite<\/a>$/}}}, {$group: {_id: 1, count: {$sum: 1}}}])
pipelineQuery5 = [{"$match": {"created_at": {"$exists": 1}, "source": {"$regex": "/.*Twitter Lite<*./"}}}, {"$group": {"_id": 1, "count": {"$sum": 1}}}]
CursorSourceForTWITTERLITE = collection.aggregate(pipelineQuery5)
for cursor in CursorSourceForTWITTERLITE:
    sourceCountTwitterLite = cursor["count"]
CursorSourceForTWITTERLITE.close()

pipelineQuery5 = [{"$match": {"created_at": {"$exists": 1}, "source": {"$regex": "/.*Twitter for Android<*./"}}}, {"$group": {"_id": 1, "count": {"$sum": 1}}}]
CursorSourceForTWITTERFORANDROID = collection.aggregate(pipelineQuery5)
for cursor in CursorSourceForTWITTERFORANDROID:
    sourceCountTwitterForAndroid = cursor["count"]
CursorSourceForTWITTERFORANDROID.close()

pipelineQuery5 = [{"$match": {"created_at": {"$exists": 1}, "source": {"$regex": "/.*Twitter Web Client<*./"}}}, {"$group": {"_id": 1, "count": {"$sum": 1}}}]
CursorSourceForTWITTERFORWEBCLIENT = collection.aggregate(pipelineQuery5)
for cursor in CursorSourceForTWITTERFORWEBCLIENT:
    sourceCountTwitterForWebClient = cursor["count"]
CursorSourceForTWITTERFORWEBCLIENT.close()

pipelineQuery5 = [{"$match": {"created_at": {"$exists": 1}, "source": {"$regex": "/.*Twitter for iPad<*./"}}}, {"$group": {"_id": 1, "count": {"$sum": 1}}}]
CursorSourceForTWITTERFORIPAD = collection.aggregate(pipelineQuery5)
for cursor in CursorSourceForTWITTERFORIPAD:
    sourceCountTwitterForIpad = cursor["count"]
CursorSourceForTWITTERFORIPAD.close()

pipelineQuery5 = [{"$match": {"created_at": {"$exists": 1}, "source": {"$regex": "/.*TweetDeck<*./"}}}, {"$group": {"_id": 1, "count": {"$sum": 1}}}]
CursorSourceForTWEETDECK = collection.aggregate(pipelineQuery5)
for cursor in CursorSourceForTWEETDECK:
    sourceCountTweetDeck = cursor["count"]
CursorSourceForTWEETDECK.close()

pipelineQuery5 = [{"$match": {"created_at": {"$exists": 1}, "source": {"$regex": "/.*SHOWROOM-LIVE<*./"}}}, {"$group": {"_id": 1, "count": {"$sum": 1}}}]
CursorSourceForSHOWROOMLIVE = collection.aggregate(pipelineQuery5)
for cursor in CursorSourceForSHOWROOMLIVE:
    sourceCountShowroomLive = cursor["count"]
CursorSourceForSHOWROOMLIVE.close()

pipelineQuery5 = [{"$match": {"created_at": {"$exists": 1}, "source": {"$regex": "/.*Google<*./"}}}, {"$group": {"_id": 1, "count": {"$sum": 1}}}]
CursorSourceForGOOGLE = collection.aggregate(pipelineQuery5)
for cursor in CursorSourceForGOOGLE:
    sourceCountGoogle = cursor["count"]
CursorSourceForGOOGLE.close()

pipelineQuery5 = [{"$match": {"created_at": {"$exists": 1}, "source": {"$regex": "/.*Instagram<*./"}}}, {"$group": {"_id": 1, "count": {"$sum": 1}}}]
CursorSourceForINSTAGRAM = collection.aggregate(pipelineQuery5)
for cursor in CursorSourceForINSTAGRAM:
    sourceCountInstagram = cursor["count"]
CursorSourceForINSTAGRAM.close()

print('Number of tweets with SOURCE as TWITTER LITE =', sourceCountTwitterLite)
print('Number of tweets with SOURCE as TWITTER FOR ANDROID =', sourceCountTwitterForAndroid)
print('Number of tweets with SOURCE as TWITTER FOR WEB CLIENT =', sourceCountTwitterForWebClient)
print('Number of tweets with SOURCE as TWITTER FOR IPAD =', sourceCountTwitterForIpad)
print('Number of tweets with SOURCE as TWEETDECK =', sourceCountTweetDeck)
print('Number of tweets with SOURCE as SHOWROOM-LIVE =', sourceCountShowroomLive)
print('Number of tweets with SOURCE as GOOGLE =', sourceCountGoogle)
print('Number of tweets with SOURCE as INSTAGRAM =', sourceCountInstagram)

print('\nProgram Endtime is:',datetime.now().strftime("%c"))
#cursorTop10ByNoOfTweets =
#db.TwitterCol1.find( {}, {"_id" :0, "user.screen_name" :1, "user.statuses_count" :1} ).sort({"user.statuses_count": -1}).limit(10)

#retDoc = colName.find_one()

#retDocUser = retDoc['user']

#print('\nDocument field created_at value is:', retDoc['created_at'])
#print('\nDocument field user.screen_name value is:', retDocUser['screen_name'])

#keys = retDoc.keys()

#print('\n\nFull document:',retDoc,'\n\n')

#keys_str = str(keys)

