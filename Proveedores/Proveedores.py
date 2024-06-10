from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from Database import Database
from Proveedores.ProveedoresDialog import ProveedoresDialog

class Proveedores(QWidget):
    def __init__(self):
        super().__init__()
        self.currentPage = 0
        self.pageSize = 20
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Top
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)

        anadir_proveedor_button = QPushButton("Añadir Proveedor")
        anadir_proveedor_button.clicked.connect(self.anadirProveedor)
        top_layout.addWidget(anadir_proveedor_button)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar")
        self.search_field.setMinimumWidth(200)
        self.search_field.returnPressed.connect(self.buscarProveedor)
        top_layout.addWidget(self.search_field)

        buscar_button = QPushButton("Buscar")
        buscar_button.clicked.connect(self.buscarProveedor)
        top_layout.addWidget(buscar_button)
        layout.addLayout(top_layout)

        # Center
        self.table_proveedores = QTableWidget()
        self.table_proveedores.setColumnCount(5)
        self.table_proveedores.setHorizontalHeaderLabels(["ID", "Nombre", "Direccion", "Telefono", "Correo Electronico"])
        self.table_proveedores.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_proveedores.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table_proveedores)

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

        self.actualizarTablaProveedores()

        self.table_proveedores.itemDoubleClicked.connect(self.abrirDialogoProveedores)

    def actualizarTablaProveedores(self):
        totalItems = Database().getDocumentosCount("proveedores")
        self.totalPages = (totalItems // self.pageSize) + 1
        self.showPage()

    def showPage(self):
        startIndex = self.currentPage * self.pageSize
        proveedores = Database().getDocumentos("proveedores", startIndex, self.pageSize)

        self.table_proveedores.setRowCount(0)
        for row, proveedor in enumerate(proveedores):
            self.table_proveedores.insertRow(row)
            self.table_proveedores.setItem(row, 0, QTableWidgetItem(str(proveedor["_id"])))
            self.table_proveedores.setItem(row, 1, QTableWidgetItem(proveedor["nombre"]))
            self.table_proveedores.setItem(row, 2, QTableWidgetItem(proveedor["direccion"]))
            self.table_proveedores.setItem(row, 3, QTableWidgetItem(proveedor["telefono"]))
            self.table_proveedores.setItem(row, 4, QTableWidgetItem(proveedor["correoElectronico"]))

        self.page_label.setText(f"Página {self.currentPage + 1} de {self.totalPages}")

    def showPrevPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.showPage()

    def showNextPage(self):
        if self.currentPage < self.totalPages - 1:
            self.currentPage += 1
            self.showPage()

    def anadirProveedor(self):
        dialog = ProveedoresDialog()
        dialog.exec_()

    def buscarProveedor(self):
        texto_busqueda = self.search_field.text().strip().lower()

        if texto_busqueda:
            resultados = Database().buscarProducto(texto_busqueda)
            self.mostrarResultadosBusqueda(resultados)
        else:
            self.actualizarTablaProveedores()

    def mostrarResultadosBusqueda(self, resultados):
        self.table_proveedores.setRowCount(0)
        for row, proveedor in enumerate(resultados):
            self.table_proveedores.insertRow(row)
            self.table_proveedores.setItem(row, 0, QTableWidgetItem(str(proveedor["_id"])))
            self.table_proveedores.setItem(row, 1, QTableWidgetItem(proveedor["nombre"]))
            self.table_proveedores.setItem(row, 2, QTableWidgetItem(proveedor["direccion"]))
            self.table_proveedores.setItem(row, 3, QTableWidgetItem(proveedor["telefono"]))
            self.table_proveedores.setItem(row, 4, QTableWidgetItem(proveedor["correoElectronico"]))

        self.page_label.setText("Resultados de la búsqueda")

    def abrirDialogoProveedores(self, item):
        id_proveedor = self.table_proveedores.item(item.row(), 0).text()
        proveedor = Database().getDocumentoById("proveedores", id_proveedor)
        dialog = ProveedoresDialog(proveedor)
        dialog.exec_()
