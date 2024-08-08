from fastapi import Depends, HTTPException, status
from gainz.settings import Settings
import pymongo
import logging
from .model import Thread, Message
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Developers should be installed mongoDB for their own to check this backend. 
# (For mongoDB installation guide. https://www.mongodb.com/zh-cn/docs/manual/tutorial/install-mongodb-on-os-x/)
# And as time constrict and convenience for test, I don't set any admin password for the database. 
# To Do. 
# 1. Setup remote testing, staging and production DB
# 2. Add admin name and password

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

# DB name and Collection (i.e. Table) are hardcode. Will be updated later. 
db = myclient["gainz"]


def get_db():
    return db

def get_collection(name:str):
    return db[name]

# OpenAI database function
def create_thread_record(thread: Thread):
    # Hash the password before storing
    try:
        print(thread.json())
        db = get_db()
        collection = db['Thread']
        data = vars(thread)
        data['_id']= thread.id
        collection.insert_one(data)
        return True
    except:
        return False
    
async def create_message_record(message: Message):
    # Hash the password before storing
    try:
        db = get_db()
        collection = db['Message']
        data = vars(message)
        data['_id']= message.id
        collection.insert_one(data)
        return True
    except:
        return False
    
def list_all_threads(uid: str):
    try:
        arr=[]
        db = get_db()
        collection = db['Thread']
        query = {"uid": uid}
        results = collection.find(query)
        for record in results:
            arr.append(record)
            print(record)
        return arr
    except:
        return False

def delete_all_threads(uid: str):
    try:
        db = get_db()
        collection = db['Thread']
        query = {"uid": uid}
        results = collection.delete_many(query)
        return True
    except:
        return False
