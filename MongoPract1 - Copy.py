# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 16:26:19 2018

WIP: currently just reads first document from the db. Then accesses just the USER info field and prints it.

@author: RB

# access all the data stored into the mongoDB and do data analysis to answer some questions
"""
from pymongo import MongoClient
from json import loads
#from datetime import datetime

#StartTime = datetime.now()
#print('\nStartTime is:',StartTime.strftime("%c"),'\n')

client = MongoClient('localhost:27017')
dbName = client['TwitterDb1']
colName = dbName['TwitterCol1']

retDoc = colName.find_one()		# returns the whole document into a so called DICTIONARY type variable

retDocUser = retDoc['user']

print('\nDocument field created_at value is:', retDoc['created_at'])
print('\nDocument field user.screen_name value is:', retDocUser['screen_name'])

#keys = retDoc.keys()

#print('\n\nFull document:',retDoc,'\n\n')

#keys_str = str(keys)

print('\nEnded')