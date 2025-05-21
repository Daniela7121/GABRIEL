from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import mysql.connector


class OfficesModule(QWidget):
    def __init__(self, db_config, parent=None):
        super().__init__(parent)
        self.db_config = db_config
        self.setup_ui()
        self.load_offices_from_db()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Consultorios")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()

        self.office_search = QLineEdit()
        self.office_search.setPlaceholderText("Buscar consultorios...")
        self.office_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")

        self.office_filter = QComboBox()
        self.office_filter.addItems(["Todos", "Activos", "Inactivos", "Por ubicación"])
        self.office_filter.setStyleSheet("padding: 8px;")

        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)
        search_btn.clicked.connect(self.filter_offices)

        tool_layout.addWidget(self.office_search)
        tool_layout.addWidget(self.office_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.office_table = QTableWidget(0, 4)
        self.office_table.setHorizontalHeaderLabels(["ID", "Nombre", "Ubicación", "Estado"])
        self.office_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #1ABC9C;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.office_table.horizontalHeader().setStretchLastSection(True)
        self.office_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.office_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.office_table.verticalHeader().setVisible(False)

        layout.addWidget(self.office_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Consultorio", self.add_office),
            ("Editar Consultorio", self.edit_office),
            ("Activar/Desactivar", self.toggle_office_status),
            ("Exportar a CSV", self.export_offices)
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

    def load_offices_from_db(self):
        self.office_table.setRowCount(0)
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT consultorio_id, nombre, ubicacion, estado FROM consultorios")
            for row_data in cursor.fetchall():
                row = self.office_table.rowCount()
                self.office_table.insertRow(row)
                for col, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    if col == 3:
                        item.setForeground(QColor(39, 174, 96) if data == "Activo" else QColor(192, 57, 43))
                    self.office_table.setItem(row, col, item)
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar consultorios:\n{str(e)}")

    def filter_offices(self):
        search_text = self.office_search.text().lower()
        filter_type = self.office_filter.currentText()

        for row in range(self.office_table.rowCount()):
            match = True
            name = self.office_table.item(row, 1).text().lower()
            location = self.office_table.item(row, 2).text().lower()
            status = self.office_table.item(row, 3).text()

            if search_text and search_text not in name and search_text not in location:
                match = False
            if filter_type == "Activos" and status != "Activo":
                match = False
            if filter_type == "Inactivos" and status != "Inactivo":
                match = False
            if filter_type == "Por ubicación" and search_text != location:
                match = False

            self.office_table.setRowHidden(row, not match)

    def add_office(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Consultorio")
        dialog.setFixedSize(400, 250)

        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit()),
            ("Ubicación:", QLineEdit()),
        ]

        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(80)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            nombre = fields[0][1].text()
            ubicacion = fields[1][1].text()
            if nombre and ubicacion:
                try:
                    conn = self.connect_db()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO consultorios (nombre, ubicacion, estado)
                        VALUES (%s, %s, %s)
                    """, (nombre, ubicacion, "Activo"))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.load_offices_from_db()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo agregar consultorio:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_office(self):
        selected_row = self.office_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Editar", "Seleccione un consultorio primero.")
            return

        current_id = self.office_table.item(selected_row, 0).text()
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Consultorio")
        dialog.setFixedSize(400, 250)

        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit(self.office_table.item(selected_row, 1).text())),
            ("Ubicación:", QLineEdit(self.office_table.item(selected_row, 2).text())),
        ]

        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(80)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            nombre = fields[0][1].text()
            ubicacion = fields[1][1].text()
            if nombre and ubicacion:
                try:
                    conn = self.connect_db()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE consultorios
                        SET nombre=%s, ubicacion=%s
                        WHERE consultorio_id=%s
                    """, (nombre, ubicacion, current_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.load_offices_from_db()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo editar consultorio:\n{str(e)}")

    def toggle_office_status(self):
        selected_row = self.office_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Estado", "Seleccione un consultorio primero.")
            return

        current_id = self.office_table.item(selected_row, 0).text()
        current_status = self.office_table.item(selected_row, 3).text()
        new_status = "Inactivo" if current_status == "Activo" else "Activo"

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE consultorios SET estado=%s WHERE consultorio_id=%s", (new_status, current_id))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_offices_from_db()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cambiar el estado:\n{str(e)}")

    def export_offices(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Consultorios a CSV",
            "",
            "CSV Files (*.csv)",
            options=options
        )

        if not file_name:
            return

        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                headers = [self.office_table.horizontalHeaderItem(i).text() for i in range(self.office_table.columnCount())]
                f.write(",".join(headers) + "\n")

                for row in range(self.office_table.rowCount()):
                    row_data = []
                    for col in range(self.office_table.columnCount()):
                        item = self.office_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    f.write(",".join(row_data) + "\n")

            QMessageBox.information(self, "Éxito", "Los datos se exportaron correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{str(e)}")
