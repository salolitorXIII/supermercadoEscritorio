from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QInputDialog
from Database import Database


class CategoriaDialog(QDialog):
    def __init__(self, categoria=None):
        super().__init__()
        self.categoria = categoria
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Añadir Categoría" if self.categoria is None else "Editar Categoría")

        # Campo input text para el nombre de la categoría
        form_layout = QVBoxLayout()
        self.nombre_field = QLineEdit(self.categoria.get("nombre", "") if self.categoria is not None else "")
        form_layout.addWidget(QLabel("Nombre Categoría"))
        form_layout.addWidget(self.nombre_field)
        layout.addLayout(form_layout)

        # Botones para guardar, eliminar o cancelar la operación
        button_layout = QHBoxLayout()
        self.guardar_button = QPushButton("Guardar")
        self.guardar_button.clicked.connect(self.guardarCategoria)
        button_layout.addWidget(self.guardar_button)
        self.eliminar_button = QPushButton("Eliminar")
        self.eliminar_button.clicked.connect(self.eliminarCategoria)
        button_layout.addWidget(self.eliminar_button)
        self.cancelar_button = QPushButton("Cancelar")
        self.cancelar_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancelar_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def guardarCategoria(self):
        nombre = self.nombre_field.text().strip()

        if not nombre:
            QMessageBox.warning(self, "Campo Incompleto", "Por favor, complete el nombre de la categoría.")
            return

        categoria = {"nombre": nombre}

        if self.categoria is not None:
            Database().actualizarDocumento("categorias", self.categoria.get('_id'), categoria)
            QMessageBox.information(self, "Categoría Actualizada", "La categoría ha sido actualizada correctamente.")
            self.accept()
        else:
            Database().guardarDocumento("categorias", categoria)
            QMessageBox.information(self, "Categoría Guardada", "La categoría ha sido guardada correctamente.")
            self.accept()

    def eliminarCategoria(self):
        nombre_categoria = self.nombre_field.text().strip()
        confirmacion = self.obtenerConfirmacion("Eliminar Categoría", f"¿Estás seguro de que deseas eliminar la categoría '{nombre_categoria}'?")

        if confirmacion == nombre_categoria:
            Database().eliminarDocumento("categorias", self.categoria.get('_id'))
            QMessageBox.information(self, "Categoría Eliminada", "La categoría ha sido eliminada correctamente.")
            self.accept()
        elif confirmacion:
            QMessageBox.warning(self, "Confirmación Incorrecta", "El nombre de la categoría introducido no coincide. La eliminación ha sido cancelada.")
        else:
            QMessageBox.warning(self, "Eliminación Cancelada", "La eliminación de la categoría ha sido cancelada.")

    def obtenerConfirmacion(self, titulo, mensaje):
        text, ok = QInputDialog.getText(self, titulo, mensaje)
        return text if ok else None
