from pymongo import MongoClient

client = MongoClient("mongo")
db = client['db']
users_pass_db = db['users'] #stores username and hashed passwords
email_db = db['emails'] #stores emails and usernames