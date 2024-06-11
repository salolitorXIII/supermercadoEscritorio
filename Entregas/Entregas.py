from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from Database import Database
from Pedidos.PedidosDialog import PedidosDialog

class Entregas(QWidget):
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

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar")
        self.search_field.setMinimumWidth(200)
        self.search_field.returnPressed.connect(self.buscarPedido)
        top_layout.addWidget(self.search_field)

        buscar_button = QPushButton("Buscar")
        buscar_button.clicked.connect(self.buscarPedido)
        top_layout.addWidget(buscar_button)
        layout.addLayout(top_layout)

        # Center
        self.table_entregas = QTableWidget()
        self.table_entregas.setColumnCount(5)
        self.table_entregas.setHorizontalHeaderLabels(["ID", "Fecha Entrega", "Hora Entrega", "Direccion", "Estado"])
        self.table_entregas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_entregas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table_entregas)

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

        self.actualizarTablaEntregas()

        self.table_entregas.itemDoubleClicked.connect(self.abrirDetallesPedido)

    def actualizarTablaEntregas(self):
        totalItems = Database().getEntregasCount()
        self.totalPages = (totalItems // self.pageSize) + 1
        self.showPage()

    def showPage(self):
        startIndex = self.currentPage * self.pageSize
        pedidos = Database().getDocumentosEntregas(startIndex, self.pageSize)

        self.table_entregas.setRowCount(0)
        for row, pedido in enumerate(pedidos):
            self.table_entregas.insertRow(row)
            self.table_entregas.setItem(row, 0, QTableWidgetItem(str(pedido["_id"])))
            self.table_entregas.setItem(row, 1, QTableWidgetItem(pedido["fechaEntrega"]))
            self.table_entregas.setItem(row, 2, QTableWidgetItem(pedido["horaEntrega"]))
            self.table_entregas.setItem(row, 3, QTableWidgetItem(pedido["dirección"]))
            self.table_entregas.setItem(row, 4, QTableWidgetItem(pedido["estado"]))

        self.page_label.setText(f"Página {self.currentPage + 1} de {self.totalPages}")

    def showPrevPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.showPage()

    def showNextPage(self):
        if self.currentPage < self.totalPages - 1:
            self.currentPage += 1
            self.showPage()

    def buscarPedido(self):
        texto_busqueda = self.search_field.text().strip().lower()

        if texto_busqueda:
            resultados = Database().buscarEntregas(texto_busqueda)
            self.mostrarResultadosBusqueda(resultados)
        else:
            self.actualizarTablaEntregas()

    def mostrarResultadosBusqueda(self, resultados):
        self.table_entregas.setRowCount(0)
        for row, pedido in enumerate(resultados):
            self.table_entregas.insertRow(row)
            self.table_entregas.setItem(row, 0, QTableWidgetItem(str(pedido["_id"])))
            self.table_entregas.setItem(row, 1, QTableWidgetItem(pedido["fechaEntrega"]))
            self.table_entregas.setItem(row, 2, QTableWidgetItem(pedido["horaEntrega"]))
            self.table_entregas.setItem(row, 3, QTableWidgetItem(pedido["direccion"]))
            self.table_entregas.setItem(row, 4, QTableWidgetItem(pedido["estado"]))

        self.page_label.setText("Resultados de la búsqueda")

    def abrirDetallesPedido(self, item):
        id_pedido = self.table_entregas.item(item.row(), 0).text()
        pedido = Database().getDocumentoById("pedidos", id_pedido)
        self.pedidoDialog = PedidosDialog(pedido)
        self.pedidoDialog.exec_()