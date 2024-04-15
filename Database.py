from pymongo import MongoClient

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.mongoClient = None
            cls._instance.database = None
            cls._instance.connect()
        return cls._instance

    def connect(self):
        connectionString = "mongodb+srv://adminUser:adminUser@supermercado.jwzvs6g.mongodb.net/?retryWrites=true&w=majority&appName=supermercado"
        self.mongoClient = MongoClient(connectionString)
        self.database = self.mongoClient.supermercado

    def getStockCount(self):
        collection = self.database.productos
        total_count = collection.count_documents({})
        return total_count

    def getStock(self, skip, limit):
        collection = self.database.productos
        products = collection.find().skip(skip).limit(limit)
        return products
