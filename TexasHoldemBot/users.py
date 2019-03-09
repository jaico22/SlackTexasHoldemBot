import pymongo
import json

class Users :

    def __init__(self):
        self.mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        print('connecting to database')
        self.database = self.mongo_client["texas_holdem_bot"]
        print('connected')
        self.users_col = self.database["users"]

    def check_in_and_add_user(self,user_id):
        # Check if user exists
        cursor = self.users_col.find({"user_id" : user_id})
        print(cursor)
        result = None
        for doc in cursor :
            result = doc
        
        if result == None :
            # If doesn't, insert them into collection
            dictation = {"user_id": user_id, "chips": 1000}
            self.users_col.insert_one(dictation)
            print('Player has been added!')
            return 1000
        else : 
            # Otherwise, turn the amount of chips they have to player with
            print('Player is already in the game')
            return result["chips"]

    def cash_out(self,user_id,chips):
        print('Cashing out...')
        query = {"user_id":user_id}
        new_values = {"$set":{"chips":chips}}
        self.users_col.update_one(query,new_values)
        print('User has been cashed out')
        