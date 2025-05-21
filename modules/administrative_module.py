from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import mysql.connector

class AdministrativeModule(QWidget):
    def __init__(self, db_config, parent=None):
        super().__init__(parent)
        self.db_config = db_config
        self.init_ui()
        self.load_administrativos_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Personal Administrativo")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()

        self.admin_search = QLineEdit()
        self.admin_search.setPlaceholderText("Buscar administrativos...")
        self.admin_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")

        self.admin_filter = QComboBox()
        self.admin_filter.addItems(["Todos", "Activos", "Inactivos", "Por puesto"])
        self.admin_filter.setStyleSheet("padding: 8px;")

        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        search_btn.clicked.connect(self.filter_administrativos)

        tool_layout.addWidget(self.admin_search)
        tool_layout.addWidget(self.admin_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.admin_table = QTableWidget(0, 6)
        self.admin_table.setHorizontalHeaderLabels(["ID", "Nombre", "Puesto", "Teléfono", "Email", "Estado"])
        self.admin_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #E74C3C;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.admin_table.horizontalHeader().setStretchLastSection(True)
        self.admin_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.admin_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.admin_table.verticalHeader().setVisible(False)

        layout.addWidget(self.admin_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Administrativo", self.add_administrativo),
            ("Editar Administrativo", self.edit_administrativo),
            ("Cambiar Estado", self.toggle_administrativo_status),
            ("Exportar a CSV", self.export_administrativos)
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

    def load_administrativos_data(self):
        self.admin_table.setRowCount(0)
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, puesto, telefono, email, estado FROM administrativos")
            for row_data in cursor.fetchall():
                row = self.admin_table.rowCount()
                self.admin_table.insertRow(row)
                for col, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    if col == 5:
                        item.setForeground(QColor(39, 174, 96) if data == "Activo" else QColor(192, 57, 43))
                    self.admin_table.setItem(row, col, item)
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la información:\n{e}")

    def filter_administrativos(self):
        search_text = self.admin_search.text().lower()
        filter_type = self.admin_filter.currentText()
        for row in range(self.admin_table.rowCount()):
            match = True
            name = self.admin_table.item(row, 1).text().lower()
            position = self.admin_table.item(row, 2).text().lower()
            status = self.admin_table.item(row, 5).text()

            if search_text and search_text not in name:
                match = False
            if filter_type == "Activos" and status != "Activo":
                match = False
            if filter_type == "Inactivos" and status != "Inactivo":
                match = False
            if filter_type == "Por puesto" and position != search_text:
                match = False

            self.admin_table.setRowHidden(row, not match)

    def add_administrativo(self):
        dialog = self.create_admin_dialog("Agregar Administrativo")
        if dialog.exec_() == QDialog.Accepted:
            datos = [field[1].text() if not isinstance(field[1], QComboBox) else field[1].currentText() for field in dialog.fields]
            if all(datos):
                try:
                    conn = self.connect_db()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO administrativos (nombre, puesto, telefono, email, estado) VALUES (%s, %s, %s, %s, %s)",
                        (*datos, "Activo")
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.load_administrativos_data()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo agregar el administrativo:\n{e}")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_administrativo(self):
        row = self.admin_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Seleccione un administrativo para editar.")
            return
        admin_id = self.admin_table.item(row, 0).text()
        dialog = self.create_admin_dialog("Editar Administrativo", prefill=[
            self.admin_table.item(row, 1).text(),
            self.admin_table.item(row, 2).text(),
            self.admin_table.item(row, 3).text(),
            self.admin_table.item(row, 4).text()
        ])
        if dialog.exec_() == QDialog.Accepted:
            datos = [field[1].text() if not isinstance(field[1], QComboBox) else field[1].currentText() for field in dialog.fields]
            if all(datos):
                try:
                    conn = self.connect_db()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE administrativos 
                        SET nombre=%s, puesto=%s, telefono=%s, email=%s 
                        WHERE id=%s
                    """, (*datos, admin_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.load_administrativos_data()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo editar:\n{e}")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def toggle_administrativo_status(self):
        row = self.admin_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Seleccione un administrativo.")
            return
        admin_id = self.admin_table.item(row, 0).text()
        current_status = self.admin_table.item(row, 5).text()
        new_status = "Inactivo" if current_status == "Activo" else "Activo"
        if QMessageBox.question(self, "Confirmar", f"¿Cambiar estado a {new_status}?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            try:
                conn = self.connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE administrativos SET estado=%s WHERE id=%s", (new_status, admin_id))
                conn.commit()
                cursor.close()
                conn.close()
                self.load_administrativos_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cambiar el estado:\n{e}")

    def export_administrativos(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exportar a CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                headers = [self.admin_table.horizontalHeaderItem(i).text() for i in range(self.admin_table.columnCount())]
                f.write(",".join(headers) + "\n")
                for row in range(self.admin_table.rowCount()):
                    line = [self.admin_table.item(row, col).text() for col in range(self.admin_table.columnCount())]
                    f.write(",".join(line) + "\n")
            QMessageBox.information(self, "Éxito", "Exportación completada.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{e}")

    def create_admin_dialog(self, title, prefill=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(400, 350)
        layout = QVBoxLayout()
        puestos = ["Administrativo", "Paciente", "Doctor", "Administrador"]
        labels = ["Nombre:", "Puesto:", "Teléfono:", "Email:"]
        dialog.fields = []
        for i, label_text in enumerate(labels):
            h = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(100)
            if label_text == "Puesto:":
                input_field = QComboBox()
                input_field.addItems(puestos)
                if prefill:
                    input_field.setCurrentText(prefill[i])
            else:
                input_field = QLineEdit()
                if prefill:
                    input_field.setText(prefill[i])
            dialog.fields.append((label_text, input_field))
            h.addWidget(label)
            h.addWidget(input_field)
            layout.addLayout(h)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        return dialog
