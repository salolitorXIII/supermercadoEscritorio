from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog
from bson import ObjectId

class PedidosDialog(QDialog):
    def __init__(self, pedido=None):
        super().__init__()
        self.pedido = pedido
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Detalles del Pedido")

        # Helper function to create label pairs
        def create_label_pair(label_text, value_text):
            hbox = QHBoxLayout()
            label = QLabel(label_text)
            value = QLabel(value_text)
            hbox.addWidget(label)
            hbox.addWidget(value)
            return hbox

        id_text = str(self.pedido.get("_id", "")) if isinstance(self.pedido.get("_id", ""), ObjectId) else self.pedido.get("_id", "")
        
        layout.addLayout(create_label_pair("ID:", id_text))
        layout.addLayout(create_label_pair("ID del Cliente:", self.pedido.get("idCliente", "")))
        layout.addLayout(create_label_pair("Correo del Cliente:", self.pedido.get("correoCliente", "")))
        layout.addLayout(create_label_pair("ID del Empleado:", self.pedido.get("idEmpleado", "")))
        layout.addLayout(create_label_pair("Fecha y Hora:", self.pedido.get("fechaHora", "")))
        layout.addLayout(create_label_pair("Estado:", self.pedido.get("estado", "")))
        layout.addLayout(create_label_pair("Precio Total:", str(self.pedido.get("precioTotal", ""))))

        header_layout = QHBoxLayout()
        header_label = QLabel("DATOS ENTREGA:")
        header_layout.addWidget(header_label)
        layout.addLayout(header_layout)

        layout.addLayout(create_label_pair("Tipo de Entrega:", self.pedido.get("tipoEntrega", "")))
        layout.addLayout(create_label_pair("Dirección:", self.pedido.get("dirección", "")))
        layout.addLayout(create_label_pair("Fecha de Entrega:", self.pedido.get("fechaEntrega", "")))
        layout.addLayout(create_label_pair("Hora de Entrega:", self.pedido.get("horaEntrega", "")))

        button_layout = QHBoxLayout()
        self.cerrar_button = QPushButton("Cerrar")
        self.cerrar_button.clicked.connect(self.close)
        button_layout.addWidget(self.cerrar_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)