from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from Pedidos.PedidosDialog import PedidosDialog
from Database import Database


class DetallePedido(QWidget):
    def __init__(self, pedido=None):
        super().__init__()
        self.pedido = pedido
        self.database = Database()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Top
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)

        btn_detalles_pedido = QPushButton("Ver todos los detalles del pedido")
        btn_detalles_pedido.clicked.connect(self.ver_detalles_pedido)
        top_layout.addWidget(btn_detalles_pedido)
        layout.addLayout(top_layout)

        # Center
        self.table_detalles_pedido = QTableWidget()
        self.table_detalles_pedido.setColumnCount(5)
        self.table_detalles_pedido.setHorizontalHeaderLabels(["ID", "Nombre producto", "Packaging producto", "Cantidad", "Estado"])
        self.table_detalles_pedido.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_detalles_pedido.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table_detalles_pedido)

        lineasPedido = self.database.getDocumentosDetallesPedido(str(self.pedido["_id"]))
        self.table_detalles_pedido.setRowCount(0)
        for row, lineaPedido in enumerate(lineasPedido):
            producto = self.database.getDocumentoById("productos", lineaPedido["idProducto"])
            self.table_detalles_pedido.insertRow(row)
            self.table_detalles_pedido.setItem(row, 0, QTableWidgetItem(str(lineaPedido["_id"])))
            self.table_detalles_pedido.setItem(row, 1, QTableWidgetItem(producto["nombre"]))
            self.table_detalles_pedido.setItem(row, 2, QTableWidgetItem(producto["packaging"]))
            self.table_detalles_pedido.setItem(row, 3, QTableWidgetItem(lineaPedido["cantidad"]))
            self.table_detalles_pedido.setItem(row, 4, QTableWidgetItem(lineaPedido["estadoLinea"]))

        self.table_detalles_pedido.itemDoubleClicked.connect(self.cambiarEstado)

    def ver_detalles_pedido(self):
        dialog = PedidosDialog(self.pedido)
        dialog.exec_()

    def cambiarEstado(self, item):
        row = item.row()
        id_linea_pedido = self.table_detalles_pedido.item(row, 0).text()
        estado_actual = self.table_detalles_pedido.item(row, 4).text()
        nuevo_estado = "NO" if estado_actual == "ANYADIDO" else "ANYADIDO"
        self.database.actualizarEstadoLineaPedido(id_linea_pedido, nuevo_estado)
        self.table_detalles_pedido.setItem(row, 4, QTableWidgetItem(nuevo_estado))
        self.verificarProductosAñadidos()

    def verificarProductosAñadidos(self):
        todos_añadidos = True
        for row in range(self.table_detalles_pedido.rowCount()):
            estado = self.table_detalles_pedido.item(row, 4).text()
            if estado != "ANYADIDO":
                todos_añadidos = False
                break
        if todos_añadidos:
            self.database.actualizarEstadoPedido(str(self.pedido["_id"]), "COMPLETADO")
        else:
            self.database.actualizarEstadoPedido(str(self.pedido["_id"]), "PENDIENTE")