# connector to mongodb

import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoConnector:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.host, self.port)
            self.db = self.client['test']
            self.collection = self.db['test_collection']
        except ConnectionFailure:
            print("Connection failed")

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, data):
        return self.collection.find_one(data)

    def find_all(self):
        return self.collection.find()

    def update(self, data, new_data):
        self.collection.update_one(data, new_data)

    def delete(self, data):
        self.collection.delete_one(data)

    def delete_all(self):
        self.collection.delete_many({})

    def close(self):
        self.client.close()