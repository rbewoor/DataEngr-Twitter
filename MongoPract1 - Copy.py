# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 16:26:19 2018

@author: RB

# access first document from mongo. Access a field at high level. Access another field (user) at high level and then access the screen_name field within it.
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
print('\nDocument field created_at value is:', retDoc['created_at'])

retDocUser = retDoc['user']
print('\nDocument field user.screen_name value is:', retDocUser['screen_name'])

#keys = retDoc.keys()

#print('\n\nFull document:',retDoc,'\n\n')

#keys_str = str(keys)

print('\nEnded')