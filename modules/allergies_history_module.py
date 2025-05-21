from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QDialogButtonBox, QHBoxLayout,
    QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AllergiesModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Historial de Alergias")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID Paciente", "Alergia", "Gravedad"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_add = QPushButton("Agregar Alergia")
        btn_add.clicked.connect(self.add_record)
        layout.addWidget(btn_add)

        self.setLayout(layout)

    def load_sample_data(self):
        self.add_row(["1", "Penicilina", "Alta"])
        self.add_row(["2", "Polen", "Moderada"])

    def add_row(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, val in enumerate(data):
            self.table.setItem(row, col, QTableWidgetItem(val))

    def add_record(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nueva Alergia")
        layout = QVBoxLayout()

        id_paciente = QLineEdit()
        alergia = QLineEdit()
        gravedad = QLineEdit()

        form_layout = [
            ("ID Paciente", id_paciente),
            ("Alergia", alergia),
            ("Gravedad (Baja/Moderada/Alta)", gravedad),
        ]

        for label_text, widget in form_layout:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            row.addWidget(widget)
            layout.addLayout(row)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            values = [id_paciente.text(), alergia.text(), gravedad.text()]
            if all(values):
                self.add_row(values)
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
