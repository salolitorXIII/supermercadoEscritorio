from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QDialog, QFrame, QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, Qt
from Database import Database


class ProductDialog(QDialog):
    def __init__(self, producto=None):
        super().__init__()
        self.producto = producto
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.mostrarImagen)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Añadir Producto" if self.producto is None else "Editar Producto")

        # Campos input text
        form_layout = QVBoxLayout()
        self.nombre_field = QLineEdit(str(self.producto.get("nombre", "")) if self.producto is not None else "")
        self.packaging_field = QLineEdit(str(self.producto.get("packaging", "")) if self.producto is not None else "")
        self.precio_compra_field = QLineEdit(str(self.producto.get("precioCompra", "")) if self.producto is not None else "")
        self.precio_venta_field = QLineEdit(str(self.producto.get("precioVenta", "")) if self.producto is not None else "")
        self.precio_venta_str_field = QLineEdit(str(self.producto.get("precioVentaString", "")) if self.producto is not None else "")
        self.stock_field = QLineEdit(str(self.producto.get("stock", "")) if self.producto is not None else "")

        form_layout.addWidget(QLabel("Nombre Producto"))
        form_layout.addWidget(self.nombre_field)
        form_layout.addWidget(QLabel("Packaging"))
        form_layout.addWidget(self.packaging_field)
        form_layout.addWidget(QLabel("Precio Compra"))
        form_layout.addWidget(self.precio_compra_field)
        form_layout.addWidget(QLabel("Precio Venta"))
        form_layout.addWidget(self.precio_venta_field)
        form_layout.addWidget(QLabel("Precio Venta String"))
        form_layout.addWidget(self.precio_venta_str_field)
        form_layout.addWidget(QLabel("Stock"))
        form_layout.addWidget(self.stock_field)
        layout.addLayout(form_layout)

        # ComboBox
        dropdown_layout = QHBoxLayout()
        dropdown_layout.addWidget(QLabel("Categoría"))
        self.categoria_dropdown = QComboBox()
        dropdown_layout.addWidget(self.categoria_dropdown)
        dropdown_layout.addWidget(QLabel("Proveedor"))
        self.proveedor_dropdown = QComboBox()
        dropdown_layout.addWidget(self.proveedor_dropdown)
        layout.addLayout(dropdown_layout)
        # Llenar los ComboBox con datos
        self.llenarCategorias()
        self.llenarProveedores()

        # Imagen
        image_frame = QFrame()
        image_frame.setFrameShape(QFrame.Box)
        image_layout = QHBoxLayout()
        self.imagen_label = QLabel()
        self.imagen_label.setAlignment(Qt.AlignCenter)
        self.imagen_label.setMinimumSize(300, 300)
        self.descargarImagen(self.producto.get("image", "https://placehold.co/300x300/orange/white") if self.producto is not None else "https://placehold.co/300x300/orange/white")
        image_layout.addWidget(self.imagen_label)
        image_frame.setLayout(image_layout)
        layout.addWidget(image_frame)

        # Campo de URL de imagen
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Imagen URL"))
        self.image_field = QLineEdit(str(self.producto.get("image", "")) if self.producto is not None else "")
        url_layout.addWidget(self.image_field)
        layout.addLayout(url_layout)

        # Botones
        button_layout = QHBoxLayout()
        self.guardar_button = QPushButton("Guardar")
        self.guardar_button.clicked.connect(self.guardarProducto)
        button_layout.addWidget(self.guardar_button)
        self.eliminar_button = QPushButton("Eliminar")
        self.eliminar_button.clicked.connect(self.eliminarProducto)
        button_layout.addWidget(self.eliminar_button)
        self.cancelar_button = QPushButton("Cancelar")
        self.cancelar_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancelar_button)
        layout.addLayout(button_layout)


        self.setLayout(layout)


    def descargarImagen(self, url):
        self.manager.get(QNetworkRequest(QUrl(url)))

    def mostrarImagen(self, reply):
        if reply.error() == 0:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.imagen_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

    def llenarCategorias(self):
        categorias = Database().getCategorias()
        categorias_map = {}
        for categoria in categorias:
            idCategoria = categoria['_id']
            nombre = categoria['nombre']
            self.categoria_dropdown.addItem(nombre)
            categorias_map[nombre] = idCategoria
        if self.producto is not None:
            nombre_categoria = self.producto.get('nombreCategoria')
            if nombre_categoria in categorias_map:
                idCategoria = categorias_map[nombre_categoria]
                indexCategoria = self.categoria_dropdown.findText(nombre_categoria)
                if indexCategoria != -1:
                    self.categoria_dropdown.setCurrentIndex(indexCategoria)

    def llenarProveedores(self):
        proveedores = Database().getProveedores()
        proveedores_map = {}
        for proveedor in proveedores:
            idProveedor = proveedor['_id']
            nombre = proveedor['nombre']
            self.proveedor_dropdown.addItem(nombre)
            proveedores_map[nombre] = idProveedor
        if self.producto is not None:
            nombre_proveedor = self.producto.get('nombreProveedor')
            if nombre_proveedor in proveedores_map:
                idProveedor = proveedores_map[nombre_proveedor]
                indexProveedor = self.proveedor_dropdown.findText(nombre_proveedor)
                if indexProveedor != -1:
                    self.proveedor_dropdown.setCurrentIndex(indexProveedor)

    def guardarProducto(self):
        nombre = self.nombre_field.text().strip()
        packaging = self.packaging_field.text().strip()
        precio_compra = self.precio_compra_field.text().strip()
        precio_venta = self.precio_venta_field.text().strip()
        precio_venta_str = self.precio_venta_str_field.text().strip()
        stock = self.stock_field.text().strip()
        categoria_index = self.categoria_dropdown.currentIndex()
        proveedor_index = self.proveedor_dropdown.currentIndex()
        image_url = self.image_field.text().strip()

        if not nombre or not packaging or not precio_compra or not precio_venta or not precio_venta_str or categoria_index == -1 or proveedor_index == -1:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor, complete todos los campos.")
            return

        categoria_id = self.categoria_dropdown.itemData(categoria_index, Qt.UserRole)
        proveedor_id = self.proveedor_dropdown.itemData(proveedor_index, Qt.UserRole)

        try:
            precio_compra = float(precio_compra)
            precio_venta = float(precio_venta)
            stock = int(stock) if stock else 0
        except ValueError:
            QMessageBox.warning(self, "Formato Inválido", "Por favor, introduzca un número válido para el precio de compra, precio de venta y stock.")
            return
        
        producto = {
            "idCategoria": categoria_id,
            "nombreCategoria": self.categoria_dropdown.currentText(),
            "nombre": nombre,
            "image": image_url,
            "precioCompra": precio_compra,
            "precioVenta": precio_venta,
            "precioVentaString": precio_venta_str,
            "packaging": packaging,
            "stock": stock,
            "idProveedor": proveedor_id,
            "nombreProveedor": self.proveedor_dropdown.currentText()
        }

        if self.producto is not None:
            Database().actualizarProducto(self.producto.get('_id'), producto)
            QMessageBox.information(self, "Producto Actualizado", "El producto ha sido actualizado correctamente.")
            self.accept()
        else:
            Database().guardarProducto(producto)
            QMessageBox.information(self, "Producto Guardado", "El producto ha sido guardado correctamente.")
            self.accept()

    def eliminarProducto(self):
        nombre_producto = self.nombre_field.text().strip()
        confirmacion = self.obtenerConfirmacion("Eliminar Producto", f"¿Estás seguro de que deseas eliminar el producto '{nombre_producto}'?")

        if confirmacion == nombre_producto:
            QMessageBox.information(self, "Producto Eliminado", "El producto ha sido eliminado correctamente.")
            self.accept()
        elif confirmacion:
            QMessageBox.warning(self, "Confirmación Incorrecta", "El nombre del producto introducido no coincide. La eliminación ha sido cancelada.")
        else:
            QMessageBox.warning(self, "Eliminación Cancelada", "La eliminación del producto ha sido cancelada.")

    def obtenerConfirmacion(self, titulo, mensaje):
        text, ok = QInputDialog.getText(self, titulo, mensaje)
        return text if ok else None