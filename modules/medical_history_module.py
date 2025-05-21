from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QDialogButtonBox, QHBoxLayout,
    QLineEdit, QTextEdit, QComboBox, QMessageBox, QDateEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
import mysql.connector

class MedicalHistoryModule(QWidget):
    def __init__(self, db_config, parent=None):
        super().__init__()
        self.db = mysql.connector.connect(**db_config)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Historial Médico")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID Paciente", "Fecha", "Diagnóstico", "Tratamiento", "Notas"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_add = QPushButton("Agregar Registro Médico")
        btn_add.clicked.connect(self.add_record)
        layout.addWidget(btn_add)

        self.setLayout(layout)

    def load_data(self):
        self.table.setRowCount(0)
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT h.paciente_id, h.fecha, 
                   SUBSTRING_INDEX(h.descripcion, '|', 1) AS diagnostico,
                   SUBSTRING_INDEX(SUBSTRING_INDEX(h.descripcion, '|', -2), '|', 1) AS tratamiento,
                   SUBSTRING_INDEX(h.descripcion, '|', -1) AS notas
            FROM historial_medico h
            ORDER BY h.fecha DESC
        """)
        for row_data in cursor.fetchall():
            self.add_row([str(item) for item in row_data])
        cursor.close()

    def add_row(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, val in enumerate(data):
            self.table.setItem(row, col, QTableWidgetItem(val))

    def add_record(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Registro Médico")
        layout = QVBoxLayout()

        id_paciente = QLineEdit()
        fecha = QDateEdit()
        fecha.setCalendarPopup(True)
        fecha.setDate(QDate.currentDate())
        diagnostico = QLineEdit()
        tratamiento = QLineEdit()
        notas = QTextEdit()

        campos = [
            ("ID Paciente", id_paciente),
            ("Fecha", fecha),
            ("Diagnóstico", diagnostico),
            ("Tratamiento", tratamiento),
            ("Notas", notas)
        ]

        for label_text, widget in campos:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            row.addWidget(widget)
            layout.addLayout(row)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            try:
                paciente_id = int(id_paciente.text())
                fecha_str = fecha.date().toString("yyyy-MM-dd")
                descripcion = f"{diagnostico.text()}|{tratamiento.text()}|{notas.toPlainText()}"

                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO historial_medico (paciente_id, descripcion, fecha)
                    VALUES (%s, %s, %s)
                """, (paciente_id, descripcion, fecha_str))
                self.db.commit()
                cursor.close()

                self.add_row([str(paciente_id), fecha_str, diagnostico.text(), tratamiento.text(), notas.toPlainText()])
                QMessageBox.information(self, "Éxito", "Registro médico guardado.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{str(e)}")
