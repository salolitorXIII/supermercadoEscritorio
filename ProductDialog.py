from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QDialog, QFrame
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, Qt, QSize

class ProductDialog(QDialog):
    def __init__(self, producto=None):
        super().__init__()
        self.producto = producto
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.mostrarImagen)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Titulo
        self.setWindowTitle("Añadir Producto" if self.producto is None else "Editar Producto")

        # Campos de entrada
        form_layout = QVBoxLayout()
        self.nombre_field = QLineEdit(str(self.producto.get("nombre", "")))
        self.packaging_field = QLineEdit(str(self.producto.get("packaging", "")))
        self.precio_compra_field = QLineEdit(str(self.producto.get("precioCompra", "")))
        self.precio_venta_field = QLineEdit(str(self.producto.get("precioVenta", "")))
        self.precio_venta_str_field = QLineEdit(str(self.producto.get("precioVentaString", "")))
        self.stock_field = QLineEdit(str(self.producto.get("stock", "")))

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

        # Combo boxes
        dropdown_layout = QHBoxLayout()
        self.categoria_dropdown = QComboBox()
        self.categoria_dropdown.addItem("Seleccionar categoría")
        self.proveedor_dropdown = QComboBox()
        self.proveedor_dropdown.addItem("Seleccionar proveedor")
        dropdown_layout.addWidget(QLabel("Categoría"))
        dropdown_layout.addWidget(self.categoria_dropdown)
        dropdown_layout.addWidget(QLabel("Proveedor"))
        dropdown_layout.addWidget(self.proveedor_dropdown)
        layout.addLayout(dropdown_layout)

        # Imagen
        image_frame = QFrame()
        image_frame.setFrameShape(QFrame.Box)
        image_layout = QHBoxLayout()
        self.imagen_label = QLabel()
        self.imagen_label.setAlignment(Qt.AlignCenter)
        self.imagen_label.setMinimumSize(300, 300)
        self.descargarImagen(self.producto.get("image", "https://placehold.co/300x300/orange/white"))
        image_layout.addWidget(self.imagen_label)
        image_frame.setLayout(image_layout)
        layout.addWidget(image_frame)

        # Campo de URL de imagen
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Imagen URL"))
        self.image_field = QLineEdit(str(self.producto.get("image", "")))
        url_layout.addWidget(self.image_field)
        layout.addLayout(url_layout)

        # Botones
        button_layout = QHBoxLayout()
        self.guardar_button = QPushButton("Guardar")
        self.eliminar_button = QPushButton("Eliminar")
        self.cancelar_button = QPushButton("Cancelar")
        button_layout.addWidget(self.cancelar_button)
        button_layout.addWidget(self.guardar_button)
        button_layout.addWidget(self.eliminar_button)
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
