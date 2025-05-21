from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QDialogButtonBox, QHBoxLayout,
    QLineEdit, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import mysql.connector
from datetime import datetime

class VaccinationHistoryModule(QWidget):
    def __init__(self, db_config, parent=None):
        super().__init__(parent)
        self.db_config = db_config
        self.setup_ui()
        self.load_historial_vacunaciones_data()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Historial de Vacunación")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.historial_vacunaciones_table = QTableWidget(0, 5)
        self.historial_vacunaciones_table.setHorizontalHeaderLabels(["ID Paciente", "Vacuna", "Fecha", "Dosis", "Observaciones"])
        self.historial_vacunaciones_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.historial_vacunaciones_table)

        # Botones
        btn_add = QPushButton("Agregar Vacunación")
        btn_edit = QPushButton("Editar Vacunación")
        btn_delete = QPushButton("Eliminar Vacunación")
        btn_pdf = QPushButton("Generar PDF")

        btn_add.clicked.connect(self.add_record)
        btn_edit.clicked.connect(self.edit_record) 
        btn_delete.clicked.connect(self.delete_record)
        btn_pdf.clicked.connect(self.generate_pdf)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_pdf)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_historial_vacunaciones_data(self):
        self.historial_vacunaciones_table.setRowCount(0)
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("""
                SELECT paciente_id, vacuna, fecha, dosis, observaciones
                FROM historial_vacunaciones
                ORDER BY fecha DESC
            """)
            for row_data in cursor.fetchall():
                self.add_row([str(item) for item in row_data])
            cursor.close()
            connection.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error de Base de Datos", str(e))

    def add_row(self, data):
        row = self.historial_vacunaciones_table.rowCount()
        self.historial_vacunaciones_table.insertRow(row)
        for column, item in enumerate(data):
            self.historial_vacunaciones_table.setItem(row, column, QTableWidgetItem(item))

    def add_record(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nueva Vacunación")
        layout = QVBoxLayout()

        fields = [
            ("ID Paciente", QLineEdit()),
            ("Vacuna", QLineEdit()),
            ("Fecha Aplicación", QLineEdit("YYYY-MM-DD")),
            ("Dosis", QComboBox()),
            ("Observaciones", QLineEdit())
        ]
        fields[3][1].addItems(["Única", "1ra", "2da", "Refuerzo"])

        for label_text, widget in fields:
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
            values = [
                widget.text() if isinstance(widget, QLineEdit) else widget.currentText()
                for _, widget in fields
            ]

            # Validación de campos
            if not all(values):
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
                return

            # Validar formato de fecha
            try:
                datetime.strptime(values[2], "%Y-%m-%d")
            except ValueError:
                QMessageBox.warning(self, "Error", "Formato de fecha incorrecto. Use YYYY-MM-DD.")
                return

            try:
                connection = mysql.connector.connect(**self.db_config)
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO historial_vacunaciones (paciente_id, vacuna, fecha, dosis, observaciones)
                    VALUES (%s, %s, %s, %s, %s)
                """, values)
                connection.commit()
                cursor.close()
                connection.close()

                self.add_row(values)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error de Base de Datos", str(e))
