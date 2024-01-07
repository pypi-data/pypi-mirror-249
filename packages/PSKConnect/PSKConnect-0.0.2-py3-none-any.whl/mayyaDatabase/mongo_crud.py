from typing import Any
import os
import pandas as pd
import pymongo
import json
from ensure import ensure_annotations
from pymongo.mongo_client import MongoClient

class mongo_operation:
    
    def __init__(self,client_url: str, database_name: str):
        self.client_url=client_url
        self.database_name=database_name

    def create_mongo_client(self):
        client = MongoClient(self.client_url)
        return client
    
    def create_database(self):
        client = self.create_mongo_client()
        self.database = client[self.database_name]
        return self.database
    
    def create_collection(self,collection_name:str):
        database = self.create_database()
        collection = database[collection_name]
        return collection
    
    def insert_record(self,record: dict, collection_name: str):
        if type(record) == list:
            for data in record:
                if type(data) != dict:
                    raise TypeError("record must be in the dict")    
            collection=self.create_collection(collection_name)
            collection.insert_many(record)
        elif type(record)==dict:
            collection=self.create_collection(collection_name)
            collection.insert_one(record)
        return

    def read_record(self,collection_name:str):
        collection = self.create_collection(collection_name)
        records = collection.find()
        for record in records:
            print(record)
        return 

    def delete_record(self,record,collection_name:str):
        collection = self.create_collection(collection_name)
        result = collection.delete_many(record)
        print(result.deleted_count)
        return
    
    def update_record(self,query,update,collection_name):
        collection=self.create_collection(collection_name)
        collection.update_many(query,update)
        return
    
    def bulk_insert(self,datafile,collection_name:str):
        self.path=datafile
        if self.path.endswith('.csv'):
            df = pd.read.csv(self.path,encoding='utf-8')
        elif self.path.endswith(".xlsx"):
            df = pd.read_excel(self.path,encoding='utf-8') 
        datajson=json.loads(df.to_json(orient='record'))
        collection=self.create_collection(collection_name)
        collection.insert_many(datajson)


