from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from Database import Database
from Pedidos.DetallePedidos import DetallePedido

class Pedidos(QWidget):
    def __init__(self):
        super().__init__()
        self.currentPage = 0
        self.pageSize = 20
        self.initUI()
        self.detallePedidosWindow = None

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
        self.table_pedidos = QTableWidget()
        self.table_pedidos.setColumnCount(5)
        self.table_pedidos.setHorizontalHeaderLabels(["ID", "ID cliente", "Estado", "Fecha Entrega", "Hora Entrega"])
        self.table_pedidos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_pedidos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table_pedidos)

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

        self.actualizarTablaPedidos()

        self.table_pedidos.itemDoubleClicked.connect(self.abrirDialogoPedidos)

    def actualizarTablaPedidos(self):
        totalItems = Database().getDocumentosCount("pedidos")
        self.totalPages = (totalItems // self.pageSize) + 1
        self.showPage()

    def showPage(self):
        startIndex = self.currentPage * self.pageSize
        pedidos = Database().getDocumentosPedidos(startIndex, self.pageSize)

        self.table_pedidos.setRowCount(0)
        for row, pedido in enumerate(pedidos):
            self.table_pedidos.insertRow(row)
            self.table_pedidos.setItem(row, 0, QTableWidgetItem(str(pedido["_id"])))
            self.table_pedidos.setItem(row, 1, QTableWidgetItem(pedido["idCliente"]))
            self.table_pedidos.setItem(row, 2, QTableWidgetItem(pedido["estado"]))
            self.table_pedidos.setItem(row, 3, QTableWidgetItem(pedido["fechaEntrega"]))
            self.table_pedidos.setItem(row, 4, QTableWidgetItem(pedido["horaEntrega"]))

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
            resultados = Database().buscarPedidos(texto_busqueda)
            self.mostrarResultadosBusqueda(resultados)
        else:
            self.actualizarTablaPedidos()

    def mostrarResultadosBusqueda(self, resultados):
        self.table_pedidos.setRowCount(0)
        for row, pedido in enumerate(resultados):
            self.table_pedidos.insertRow(row)
            self.table_pedidos.setItem(row, 0, QTableWidgetItem(str(pedido["_id"])))
            self.table_pedidos.setItem(row, 1, QTableWidgetItem(pedido["idCliente"]))
            self.table_pedidos.setItem(row, 2, QTableWidgetItem(pedido["estado"]))
            self.table_pedidos.setItem(row, 3, QTableWidgetItem(pedido["fechaEntrega"]))
            self.table_pedidos.setItem(row, 4, QTableWidgetItem(pedido["horaEntrega"]))

        self.page_label.setText("Resultados de la búsqueda")

    def abrirDialogoPedidos(self, item):
        id_pedido = self.table_pedidos.item(item.row(), 0).text()
        pedido = Database().getDocumentoById("pedidos", id_pedido)
        self.detallePedidosWindow = DetallePedido(pedido)
        self.detallePedidosWindow.showMaximized()