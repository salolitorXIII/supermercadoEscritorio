from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QInputDialog
from Database import Database

class ProveedoresDialog(QDialog):
    def __init__(self, proveedor=None):
        super().__init__()
        self.proveedor = proveedor
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Añadir Proveedor" if self.proveedor is None else "Editar Proveedor")

        # Campo input text para el nombre
        form_layout = QVBoxLayout()
        self.nombre_field = QLineEdit(self.proveedor.get("nombre", "") if self.proveedor is not None else "")
        form_layout.addWidget(QLabel("Nombre"))
        form_layout.addWidget(self.nombre_field)

        # Campo input text para la dirección
        self.direccion_field = QLineEdit(self.proveedor.get("direccion", "") if self.proveedor is not None else "")
        form_layout.addWidget(QLabel("Dirección"))
        form_layout.addWidget(self.direccion_field)

        # Campo input text para el teléfono
        self.telefono_field = QLineEdit(self.proveedor.get("telefono", "") if self.proveedor is not None else "")
        form_layout.addWidget(QLabel("Teléfono"))
        form_layout.addWidget(self.telefono_field)

        # Campo input text para el correo electrónico
        self.correo_field = QLineEdit(self.proveedor.get("correoElectronico", "") if self.proveedor is not None else "")
        form_layout.addWidget(QLabel("Correo Electrónico"))
        form_layout.addWidget(self.correo_field)

        layout.addLayout(form_layout)

        # Botones para guardar, eliminar o cancelar la operación
        button_layout = QHBoxLayout()
        self.guardar_button = QPushButton("Guardar")
        self.guardar_button.clicked.connect(self.guardarProveedor)
        button_layout.addWidget(self.guardar_button)
        self.eliminar_button = QPushButton("Eliminar")
        self.eliminar_button.clicked.connect(self.eliminarProveedor)
        button_layout.addWidget(self.eliminar_button)
        self.cancelar_button = QPushButton("Cancelar")
        self.cancelar_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancelar_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def guardarProveedor(self):
        nombre = self.nombre_field.text().strip()
        direccion = self.direccion_field.text().strip()
        telefono = self.telefono_field.text().strip()
        correo = self.correo_field.text().strip()

        if not nombre or not direccion or not telefono or not correo:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor, complete todos los campos.")
            return

        proveedor = {
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono,
            "correoElectronico": correo
        }

        if self.proveedor is not None:
            Database().actualizarDocumento("proveedores", self.proveedor.get('_id'), proveedor)
            QMessageBox.information(self, "Proveedor Actualizado", "Los datos del proveedor han sido actualizados correctamente.")
            self.accept()
        else:
            Database().guardarDocumento("proveedores", proveedor)
            QMessageBox.information(self, "Proveedor Guardado", "Los datos del proveedor han sido guardados correctamente.")
            self.accept()

    def eliminarProveedor(self):
        nombre = self.nombre_field.text().strip()
        confirmacion = self.obtenerConfirmacion("Eliminar Proveedor", f"¿Estás seguro de que deseas eliminar el registro del proveedor '{nombre}'?")

        if confirmacion == nombre:
            Database().eliminarDocumento("proveedores", self.proveedor.get('_id'))
            QMessageBox.information(self, "Proveedor Eliminado", "El registro del proveedor ha sido eliminado correctamente.")
            self.accept()
        elif confirmacion:
            QMessageBox.warning(self, "Confirmación Incorrecta", "El nombre del proveedor introducido no coincide. La eliminación ha sido cancelada.")
        else:
            QMessageBox.warning(self, "Eliminación Cancelada", "La eliminación del registro del proveedor ha sido cancelada.")

    def obtenerConfirmacion(self, titulo, mensaje):
        text, ok = QInputDialog.getText(self, titulo, mensaje)
        return text if ok else None