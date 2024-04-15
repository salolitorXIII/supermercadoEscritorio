from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from Database import Database
from ProductDialog import ProductDialog

class Stock(QWidget):
    def __init__(self):
        super().__init__()
        self.currentPage = 0
        self.pageSize = 20
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Top
        top_layout = QHBoxLayout()
        anadir_producto_button = QPushButton("Añadir Producto")
        anadir_producto_button.clicked.connect(self.anadirProducto)
        top_layout.addWidget(anadir_producto_button)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar")
        top_layout.addWidget(self.search_field)

        buscar_button = QPushButton("Buscar")
        buscar_button.clicked.connect(self.buscarProducto)
        top_layout.addWidget(buscar_button)
        layout.addLayout(top_layout)

        # Center
        self.table_stock = QTableWidget()
        self.table_stock.setColumnCount(6)
        self.table_stock.setHorizontalHeaderLabels(["ID", "Nombre", "Packaging", "Categoría", "Proveedor", "Stock"])
        self.table_stock.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_stock.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table_stock)

        # Pagination
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Anterior")
        self.prev_button.clicked.connect(self.showPrevPage)
        self.next_button = QPushButton("Siguiente")
        self.next_button.clicked.connect(self.showNextPage)
        self.page_label = QLabel()
        pagination_layout.addStretch(1)
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addStretch(1)
        layout.addLayout(pagination_layout)

        self.actualizarStock()

        # Conectar señal itemDoubleClicked para abrir el diálogo con los datos del producto
        self.table_stock.itemDoubleClicked.connect(self.abrirDialogoProducto)

    def actualizarStock(self):
        totalItems = Database().getStockCount()
        self.totalPages = (totalItems // self.pageSize) + 1
        self.showPage()

    def showPage(self):
        startIndex = self.currentPage * self.pageSize
        endIndex = startIndex + self.pageSize
        stock = Database().getStock(startIndex, self.pageSize)

        self.table_stock.setRowCount(0)
        for row, producto in enumerate(stock):
            self.table_stock.insertRow(row)
            self.table_stock.setItem(row, 0, QTableWidgetItem(str(producto["_id"])))
            self.table_stock.setItem(row, 1, QTableWidgetItem(producto["nombre"]))
            self.table_stock.setItem(row, 2, QTableWidgetItem(producto["packaging"]))
            self.table_stock.setItem(row, 3, QTableWidgetItem(producto["nombreCategoria"]))
            self.table_stock.setItem(row, 4, QTableWidgetItem(producto["nombreProveedor"]))
            self.table_stock.setItem(row, 5, QTableWidgetItem(str(producto["stock"])))

        self.page_label.setText(f"Página {self.currentPage + 1} de {self.totalPages}")

    def showPrevPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.showPage()

    def showNextPage(self):
        if self.currentPage < self.totalPages - 1:
            self.currentPage += 1
            self.showPage()

    def anadirProducto(self):
        dialog = ProductDialog()
        dialog.exec_()

    def buscarProducto(self):
        pass

    def abrirDialogoProducto(self, item):
        id_producto = self.table_stock.item(item.row(), 0).text()
        producto = Database().getProductByID(id_producto)
        dialog = ProductDialog(producto)
        dialog.exec_()
