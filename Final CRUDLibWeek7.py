# Author: Chris Trimmer
# Course: CS340 Client/Server Development
# Assignment: Week 7 Project
# Date: 10/11/2023


import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint


# Create the library that client code will interface with
class AnimalShelter(object):
    
    # Modified constructor to pass username and password as variables from the client
    def __init__(self, uname, upass):
        #USER = 'aacuser'
        #PASS = 'aac1234'
        USER = uname
        PASS = upass
        HOST = 'nv-desktop-services.apporto.com'
        HOST2 = 'localhost'
        PORT = 31321
        #PORT=7308
        #PORT = 31580
        #DB = 'aac'
        #DB = 'AAC'
        DB = 'AACWeek7'
        COL = 'animals'
        
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]
        
        print(f"Chris Trimmer, CS340, Module 7 Project 2")
        print (f"{USER} and {PASS} from lib file")
        
        
    # Create a new document
    # Use the cursor find_one function to find to test if the record already exists
    # If the document doesn't already exist, then use cursor insert_one function
    # Return true if the document was created, false if it wasn't
    def create(self, data):
        if data is None or data == {}:
            print("-> Error creating new document.")
            return False
        else:
            cursorCreate = self.collection.find_one(data,{"_id":False})
            if cursorCreate is None:
                newDocument = self.collection.insert_one(data)
                if newDocument.inserted_id:
                    return True
            else:
                return False

    # Read a document and return result as cursor
    # This is for future in case when we need to return cursor instead of list
    def readCursor(self, data):
        cursorRead = self.collection.find(data,{"_id":False})
        return cursorRead
    
    
    # Read all documents in the collection
    # use try/catch block to catch failures or bad find
    # save the cursor to a list using built-in python/pymongo list() function
    # Return the list to the caller for processing
    def readAll(self, data):
        try:
            #cursorRead = self.collection.find(data,{"_id":False})
            cursorRead = self.collection.find(data)
            resultList = list(cursorRead)
            print("-> " + str(cursorRead.count()) + " of " + str(self.collection.count_documents({})) + 
                  " document(s) read.")
            return resultList
        except Exception as e:
            print(e)
        return []
        
        
    # Read a single document in the collection
    # use try/catch block to catch failures or bad find
    # save the cursor to a list using built-in python/pymongo list() function
    # Return the list to the caller for processing
    def read(self, data):
        try:
            cursorRead = self.collection.find(data,{"_id":False})
            #cursorRead = self.collection.find(data)
            resultList = list(cursorRead)
            print("-> " + str(cursorRead.count()) + " of " + str(self.collection.count_documents({})) + 
                  " document(s) read.")
            return resultList
        except Exception as e:
            print(e)
        return []
    

    # Update document(s)
    # Use update_many cursor function to update the documents
    # Use $set operator to update the fields
    # Returns the amount of documents updated using the modified_count cursor property
    def update(self, data, info):
        if data is None:
            print("-> Error updating data.")
            return 0
        
        try:
            cursorUpdate = self.collection.update_many(data, {"$set":info})
            if cursorUpdate.modified_count > 0:
                print(f"-> " + str(cursorUpdate.modified_count) + " of " + str(self.collection.count_documents({})) + " document(s) updated.")
            return cursorUpdate.modified_count
        except Exception as e:
            print(e)
        return 0
            
        
    # Delete document(s)
    # Use delete_many function of cursor
    # Returns the count of deleted documents using deleted_count cursor function
    def delete(self, data):
        if data is None or data == {}:
            print("-> Error deleting data.")
            return False

        deleteCursor = self.collection.delete_many(data)
        if deleteCursor.deleted_count > 0:
            print("-> Document (rec_num): " + str(data["rec_num"]) + " has been deleted.")
            print("-> " + str(self.collection.count_documents({})) + " documents in the collection")
            return deleteCursor.deleted_count
        else:
            print("-> Error deleting data.")
            return 0

    