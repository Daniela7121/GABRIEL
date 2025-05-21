from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import mysql.connector


class DoctorsModule(QWidget):
    def __init__(self, db_config, parent=None):
        super().__init__(parent)
        self.db_config = db_config
        self.setup_ui()
        self.load_doctors_from_db()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Doctores")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Herramientas de búsqueda y filtro
        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()

        self.doctor_search = QLineEdit()
        self.doctor_search.setPlaceholderText("Buscar doctores...")
        self.doctor_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")

        self.doctor_filter = QComboBox()
        self.doctor_filter.addItems(["Todos", "Activos", "Inactivos", "Especialidad"])
        self.doctor_filter.setStyleSheet("padding: 8px;")

        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        search_btn.clicked.connect(self.filter_doctors)

        tool_layout.addWidget(self.doctor_search)
        tool_layout.addWidget(self.doctor_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        # Tabla de doctores
        self.doctor_table = QTableWidget(0, 6)
        self.doctor_table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Especialidad", "Teléfono", "Email", "Estado"]
        )
        self.doctor_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #27AE60;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.doctor_table.horizontalHeader().setStretchLastSection(True)
        self.doctor_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.doctor_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.doctor_table.verticalHeader().setVisible(False)
        layout.addWidget(self.doctor_table)

        # Botones de acción
        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Doctor", self.add_doctor),
            ("Editar Doctor", self.edit_doctor),
            ("Activar/Desactivar", self.toggle_doctor_status),
            ("Exportar a CSV", self.export_doctors)
        ]
        for text, handler in actions:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2C3E50;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 8px;
                    font-weight: bold;
                    margin-right: 10px;
                }
                QPushButton:hover {
                    background-color: #34495E;
                }
            """)
            btn.clicked.connect(handler)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def connect_db(self):
        return mysql.connector.connect(**self.db_config)

    def load_doctors_from_db(self):
        self.doctor_table.setRowCount(0)
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, especialidad, telefono, email, estado FROM doctores")
            for row_data in cursor.fetchall():
                row = self.doctor_table.rowCount()
                self.doctor_table.insertRow(row)
                for col, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    if col == 5:
                        item.setForeground(QColor(39, 174, 96) if data == "Activo" else QColor(192, 57, 43))
                    self.doctor_table.setItem(row, col, item)
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar doctores:\n{str(e)}")

    def filter_doctors(self):
        search_text = self.doctor_search.text().lower()
        filter_type = self.doctor_filter.currentText()
        for row in range(self.doctor_table.rowCount()):
            match = True
            name = self.doctor_table.item(row, 1).text().lower()
            specialty = self.doctor_table.item(row, 2).text().lower()
            status = self.doctor_table.item(row, 5).text()
            if search_text and search_text not in name and search_text not in specialty:
                match = False
            if filter_type == "Activos" and status != "Activo":
                match = False
            if filter_type == "Inactivos" and status != "Inactivo":
                match = False
            if filter_type == "Especialidad" and search_text != specialty:
                match = False
            self.doctor_table.setRowHidden(row, not match)

    def add_doctor(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Doctor")
        dialog.setFixedSize(400, 300)
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit()),
            ("Especialidad:", QLineEdit()),
            ("Teléfono:", QLineEdit()),
            ("Email:", QLineEdit()),
        ]
        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(100)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            datos = [f[1].text() for f in fields]
            if all(datos):
                try:
                    conn = self.connect_db()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO doctores (nombre, especialidad, telefono, email, estado) VALUES (%s,%s,%s,%s,'Activo')",
                        tuple(datos)
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.load_doctors_from_db()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo agregar doctor:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_doctor(self):
        selected_row = self.doctor_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Editar", "Seleccione un doctor primero.")
            return
        current_id = self.doctor_table.item(selected_row, 0).text()
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Doctor")
        dialog.setFixedSize(400, 300)
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit(self.doctor_table.item(selected_row,1).text())),
            ("Especialidad:", QLineEdit(self.doctor_table.item(selected_row,2).text())),
            ("Teléfono:", QLineEdit(self.doctor_table.item(selected_row,3).text())),
            ("Email:", QLineEdit(self.doctor_table.item(selected_row,4).text())),
        ]
        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(100)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            datos = [f[1].text() for f in fields]
            if all(datos):
                try:
                    conn = self.connect_db()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE doctores SET nombre=%s, especialidad=%s, telefono=%s, email=%s WHERE id=%s",
                        (*datos, current_id)
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.load_doctors_from_db()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo editar doctor:\n{str(e)}")

    def toggle_doctor_status(self):
        selected_row = self.doctor_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Estado", "Seleccione un doctor primero.")
            return
        current_id = self.doctor_table.item(selected_row, 0).text()
        current_status = self.doctor_table.item(selected_row, 5).text()
        new_status = "Inactivo" if current_status == "Activo" else "Activo"
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE doctores SET estado=%s WHERE id=%s", (new_status, current_id))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_doctors_from_db()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cambiar estado:\n{str(e)}")

    def export_doctors(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Exportar Doctores", "doctores.csv", "CSV Files (*.csv)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    headers = [self.doctor_table.horizontalHeaderItem(col).text() for col in range(self.doctor_table.columnCount())]
                    f.write(','.join(headers) + '\n')
                    for row in range(self.doctor_table.rowCount()):
                        if not self.doctor_table.isRowHidden(row):
                            row_data = [self.doctor_table.item(row, col).text() if self.doctor_table.item(row, col) else "" for col in range(self.doctor_table.columnCount())]
                            f.write(','.join(row_data) + '\n')
                QMessageBox.information(self, "Éxito", f"Doctores exportados a:\n{file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{str(e)}")
