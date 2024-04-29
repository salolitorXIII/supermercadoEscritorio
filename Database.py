from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId


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
    
    def getProductByID(self, product_id):
        collection = self.database.productos
        product = collection.find_one({"_id": ObjectId(product_id)})
        return product

    def buscarProducto(self, termino):
        try:
            ObjectId(termino)
            es_id = True
        except InvalidId:
            es_id = False

        filtro = {}

        if es_id:
            filtro.update({
                "$or": [
                    {"_id": ObjectId(termino)},
                    {"idCategoria": ObjectId(termino)},
                    {"idProveedor": ObjectId(termino)}
                ]
            })
        else:
            filtro.update({
                "$or": [
                    {"nombre": {"$regex": termino, "$options": "i"}},
                    {"nombreCategoria": {"$regex": termino, "$options": "i"}},
                    {"nombreProveedor": {"$regex": termino, "$options": "i"}}
                ]
            })

        productos = self.database.productos.find(filtro)
        return list(productos)

    def getCategorias(self):
        collection = self.database.categorias
        categorias = collection.find()
        return list(categorias)
    
    def getProveedores(self):
        collection = self.database.proveedores
        proveedores = collection.find()
        return list(proveedores)
    
    def guardarProducto(self, producto):
        collection = self.database.productos
        collection.insert_one(producto)

    def actualizarProducto(self, producto_id, producto):
        collection = self.database.productos
        collection.update_one({"_id": ObjectId(producto_id)}, {"$set": producto})

    def eliminarProducto(self, producto_id):
        collection = self.database.productos
        collection.delete_one({"_id": ObjectId(producto_id)})

    
    # Categorias
    def getCategoriasCount(self):
        collection = self.database.categorias
        total_count = collection.count_documents({})
        return total_count
    
    def getCategorias(self, skip, limit):
        collection = self.database.categorias
        products = collection.find().skip(skip).limit(limit)
        return products
    
    def buscarCategoria(self, termino):
        filtro = {}
        try:
            ObjectId(termino)
            filtro.update({
                "$or": [
                    {"_id": ObjectId(termino)}
                ]
            })
        except InvalidId:
            filtro.update({
                "$or": [
                    {"nombre": {"$regex": termino, "$options": "i"}}
                ]
            }) 

        categorias = self.database.categorias.find(filtro)
        return list(categorias)