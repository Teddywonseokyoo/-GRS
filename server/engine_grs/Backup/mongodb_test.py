from pymongo import MongoClient
import pymongo
import urllib

password = urllib.quote_plus('gas1meter2iot')
client = MongoClient('mongodb://grsdatamanager:' + password + '@107.170.216.212')
print client
db = client.grsdata
cursor = db.grstasks.find({"superviser" : "" }).sort([("inputdate", pymongo.ASCENDING) ]).limit(1)
for document in cursor:
    print(document)

"""
find end task is null and high task importance
"""
"""
#Greater Than
cursor = collection.find({"importance" : {"$gt": 1}})
for document in cursor:
    print(document)
"""
"""
cursor = collection.find({"superviser" : "" })
for document in cursor:
    print(document)
"""
"""
cursor = collection.find({"starttime" : {'$ne': 'null' } })
for document in cursor:
    print(document)
"""
"""
#Less Than
cursor = collection.find({"importance" : {"$lt": 1}})
for document in cursor:
    print(document)
"""
"""
#oreder by
cursor = collection.find().sort([("inputdate", pymongo.ASCENDING) ]) #  pymongo.DESCENDING
for document in cursor:
    print(document)
"""

# and ,   or {"$or": [{"cuisine": "Italian"}, {"address.zipcode": "10075"}]})


