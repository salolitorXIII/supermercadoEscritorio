from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
import pymongo
import re


class Database:
    _instance = None
    activeUser = ""

    # Singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.mongoClient = None
            cls._instance.database = None
            cls._instance.connect()
        return cls._instance

    # Conector a la base de datos
    def connect(self):
        connectionString = "mongodb+srv://adminUser:adminUser@supermercado.jwzvs6g.mongodb.net/?retryWrites=true&w=majority&appName=supermercado"
        self.mongoClient = MongoClient(connectionString)
        self.database = self.mongoClient.supermercado


    # Métodos para interactuar con la base de datos
    # CREATE
    def guardarDocumento(self, collection_name, documento):
        collection = self.database[collection_name]
        collection.insert_one(documento)

    # READ
    def getDocumentoById(self, collection_name, documento_id):
        collection = self.database[collection_name]
        documento = collection.find_one({"_id": ObjectId(documento_id)})
        return documento
    
    def getDocumentosCount(self, collection_name):
        collection = self.database[collection_name]
        total_count = collection.count_documents({})
        return total_count

    def getDocumentos(self, collection_name, skip, limit):
        collection = self.database[collection_name]
        documentos = collection.find().skip(skip).limit(limit)
        return documentos
    
    def getAllDocumentos(self, collection_name):
        collection = self.database[collection_name]
        documentos = collection.find()
        return documentos

    # UPDATE
    def actualizarDocumento(self, collection_name, documento_id, documento):
        collection = self.database[collection_name]
        collection.update_one({"_id": ObjectId(documento_id)}, {"$set": documento})

    # DELETE
    def eliminarDocumento(self, collection_name, documento_id):
        collection = self.database[collection_name]
        collection.delete_one({"_id": ObjectId(documento_id)})


    # Métodos específicos para la colección de productos
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


    # Métodos específicos para la colección de categorías
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
    
    
    # Métodos específicos para la colección de proveedores
    def buscarProveedor(self, termino):
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

        proveedores = self.database.proveedores.find(filtro)
        return list(proveedores)
    

    # Métodos específicos para la colección de pedidos
    def buscarPedidos(self, termino):
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
                    {"estado": {"$regex": termino, "$options": "i"}},
                    {"idCliente": {"$regex": termino, "$options": "i"}},
                    {"fechaEntrega": {"$regex": termino, "$options": "i"}}
                ]
            }) 

        pedidos = self.database.pedidos.find(filtro)
        return list(pedidos)


    def getDocumentosPedidos(self, skip, limit):
        collection = self.database["pedidos"]
        
        estado_filtro = {"estado": {"$in": ["PENDIENTE", "COMPLETADO", "ENVIADO"]}}
        
        orden = [
            ("estado", pymongo.DESCENDING),
            ("fechaEntrega", pymongo.ASCENDING),
            ("horaEntrega", pymongo.ASCENDING)
        ]
        
        documentos = collection.find(estado_filtro).sort(orden).skip(skip).limit(limit)
        return list(documentos) 
    
    def actualizarEstadoPedido(self, pedido_id, nuevo_estado):
        collection = self.database["pedidos"]
        collection.update_one({"_id": ObjectId(pedido_id)}, {"$set": {"estado": nuevo_estado}})
    

    # Métodos específicos para la colección de detalles de pedidos
    def getDocumentosDetallesPedido(self, pedido_id):
        collection = self.database["detallesPedido"]
        documentos = collection.find({"idPedido": pedido_id})
        return list(documentos)
    
    def actualizarEstadoLineaPedido(self, linea_pedido_id, nuevo_estado):
        collection = self.database["detallesPedido"]
        collection.update_one({"_id": ObjectId(linea_pedido_id)}, {"$set": {"estadoLinea": nuevo_estado}})

    
    # Metodos específicos para la clase Login
    def login(self, username, password):
        regex_username = re.compile(username, re.IGNORECASE)
        employee = self.database.empleados.find_one({"correo": {"$regex": regex_username}})

        if employee:
            if password == employee["contrasenya"]:
                Database.activeUser = str(username).lower()
                return True

        return False