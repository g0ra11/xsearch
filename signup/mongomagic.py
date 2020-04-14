import pymongo


class MongoClient:
    def __init__(self, cl="mongodb://localhost:27017/", db="accounts", col="accounts"):
        self.client = pymongo.MongoClient(cl)
        self.db = self.client[db]
        self.col = self.db[col]

    def insert(self, doc):
        self.col.insert_one(doc)
        print(doc)
        print('data uploaded to db')

    def find(self, doc):
        return list(self.col.find(doc))

    def delete(self, doc):
        return self.col.delete_many(doc)

    def update(self, elem, value):
        return self.col.update_one(elem, value)
