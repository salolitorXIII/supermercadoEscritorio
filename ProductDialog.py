from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QComboBox, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl

class ProductDialog(QDialog):
    def __init__(self, producto=None):
        super().__init__()
        self.producto = producto
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Titulo
        self.setWindowTitle("Añadir Producto" if self.producto is None else "Editar Producto")

        # Campos de entrada
        form_layout = QVBoxLayout()
        self.nombre_field = QLineEdit(str(self.producto.get("nombre", "")))
        self.precio_compra_field = QLineEdit(str(self.producto.get("precioCompra", "")))
        self.precio_venta_field = QLineEdit(str(self.producto.get("precioVenta", "")))
        self.stock_field = QLineEdit(str(self.producto.get("stock", "")))

        form_layout.addWidget(QLabel("Nombre Producto"))
        form_layout.addWidget(self.nombre_field)
        form_layout.addWidget(QLabel("Precio Compra"))
        form_layout.addWidget(self.precio_compra_field)
        form_layout.addWidget(QLabel("Precio Venta"))
        form_layout.addWidget(self.precio_venta_field)
        form_layout.addWidget(QLabel("Stock"))
        form_layout.addWidget(self.stock_field)

        # Imagen
        self.imagen_label = QLabel()
        self.descargarImagen(self.producto.get("imagen", "https://placehold.co/200x200/orange/white"))
        self.imagen_label.setScaledContents(True)
        self.imagen_label.setMinimumSize(200, 200)

        layout.addLayout(form_layout)
        layout.addWidget(self.imagen_label)

        # Dropdowns
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
        manager = QNetworkAccessManager()
        manager.finished.connect(self.mostrarImagen)
        manager.get(QNetworkRequest(QUrl(url)))

    def mostrarImagen(self, reply):
        if reply.error() == 0:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.imagen_label.setPixmap(pixmap)
