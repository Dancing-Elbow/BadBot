import pymongo

class MongoHelper:
    def __init__(self, url):
        self.client = pymongo.MongoClient(url)
        print(self.client.list_database_names())
    def add_user(self, id, classInfo):
        pass