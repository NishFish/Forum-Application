from pymongo import MongoClient

client = MongoClient("mongo")
db = client['db']
auction_db = db['users']