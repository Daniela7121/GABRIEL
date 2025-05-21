import mysql.connector
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QMessageBox, QFileDialog, QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from datetime import datetime

class AuditModule(QWidget):
    def __init__(self, db_config):
        super().__init__()
        self.db_config = db_config
        self.init_ui()
        self.load_audit_data()

    def connect_db(self):
        return mysql.connector.connect(**self.db_config)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Registros de Auditoría")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Filtros
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        filter_layout = QHBoxLayout()

        self.audit_date_from = QLineEdit()
        self.audit_date_from.setPlaceholderText("Desde: DD/MM/AAAA")
        self.audit_date_to = QLineEdit()
        self.audit_date_to.setPlaceholderText("Hasta: DD/MM/AAAA")
        self.audit_user_filter = QLineEdit()
        self.audit_user_filter.setPlaceholderText("Usuario")
        self.audit_action_filter = QComboBox()
        self.audit_action_filter.addItems([
            "Todas", "login", "logout", 
            "creacion", "modificacion", "eliminacion",
            "lectura", "error", "acceso_denegado"
        ])
        self.audit_table_filter = QComboBox()
        self.audit_table_filter.addItems(["Todas", "usuarios", "citas", "medicamentos", "facturacion"])

        for widget in [
            self.audit_date_from, self.audit_date_to, 
            self.audit_user_filter, self.audit_action_filter,
            self.audit_table_filter
        ]:
            widget.setStyleSheet("padding: 8px;")
            filter_layout.addWidget(widget)

        self.audit_search_btn = QPushButton("Buscar")
        self.audit_search_btn.setStyleSheet("""
            QPushButton {
                background-color: #E67E22;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D35400;
            }
        """)
        self.audit_search_btn.clicked.connect(self.load_audit_data)
        filter_layout.addWidget(self.audit_search_btn)

        filter_frame.setLayout(filter_layout)
        layout.addWidget(filter_frame)

        # Tabla con las nuevas columnas
        self.audit_table = QTableWidget(0, 7)
        self.audit_table.setHorizontalHeaderLabels([
            "Fecha", "Usuario", "Acción", "Tabla", 
            "ID Afectado", "IP Origen", "Descripción"
        ])
        self.audit_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #E67E22;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
        """)
        self.audit_table.horizontalHeader().setStretchLastSection(True)
        self.audit_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.audit_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.audit_table.verticalHeader().setVisible(False)
        
        # Ajustar anchos de columnas
        self.audit_table.setColumnWidth(0, 150)  # Fecha
        self.audit_table.setColumnWidth(1, 150)  # Usuario
        self.audit_table.setColumnWidth(2, 100)  # Acción
        self.audit_table.setColumnWidth(3, 100)  # Tabla
        self.audit_table.setColumnWidth(4, 80)   # ID Afectado
        self.audit_table.setColumnWidth(5, 120)  # IP Origen
        
        layout.addWidget(self.audit_table)

        # Botones
        btn_layout = QHBoxLayout()
        export_btn = QPushButton("Exportar a CSV")
        clear_btn = QPushButton("Limpiar Filtros")
        details_btn = QPushButton("Ver Detalles")

        for btn in [export_btn, clear_btn, details_btn]:
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

        export_btn.clicked.connect(self.export_audit_logs)
        clear_btn.clicked.connect(self.clear_audit_filters)
        details_btn.clicked.connect(self.show_details)
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(details_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_audit_data(self):
        self.audit_table.setRowCount(0)

        query = """
            SELECT 
                a.fecha, 
                u.email, 
                a.accion, 
                a.tabla_afectada,
                a.id_afectado,
                a.ip_origen,
                a.descripcion
            FROM auditoria a
            JOIN usuarios u ON a.usuario_id = u.usuario_id
            WHERE 1 = 1
        """
        params = []

        # Filtros
        if self.audit_date_from.text():
            try:
                date_from = datetime.strptime(self.audit_date_from.text(), "%d/%m/%Y").date()
                query += " AND DATE(a.fecha) >= %s"
                params.append(date_from)
            except:
                QMessageBox.warning(self, "Formato inválido", "Fecha 'Desde' no válida.")
                return

        if self.audit_date_to.text():
            try:
                date_to = datetime.strptime(self.audit_date_to.text(), "%d/%m/%Y").date()
                query += " AND DATE(a.fecha) <= %s"
                params.append(date_to)
            except:
                QMessageBox.warning(self, "Formato inválido", "Fecha 'Hasta' no válida.")
                return

        if self.audit_user_filter.text():
            query += " AND u.email LIKE %s"
            params.append(f"%{self.audit_user_filter.text()}%")

        action_filter = self.audit_action_filter.currentText()
        if action_filter != "Todas":
            query += " AND a.accion = %s"
            params.append(action_filter.lower())

        table_filter = self.audit_table_filter.currentText()
        if table_filter != "Todas":
            query += " AND a.tabla_afectada = %s"
            params.append(table_filter.lower())

        query += " ORDER BY a.fecha DESC"

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()

            for row_data in results:
                row = self.audit_table.rowCount()
                self.audit_table.insertRow(row)
                
                for col, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    
                    # Colorear según el tipo de acción
                    if col == 2:  # Columna de Acción
                        if value == "login":
                            item.setForeground(QColor(41, 128, 185))
                        elif value == "logout":
                            item.setForeground(QColor(142, 68, 173))
                        elif value in ["creacion", "modificacion"]:
                            item.setForeground(QColor(39, 174, 96))
                        elif value == "eliminacion":
                            item.setForeground(QColor(192, 57, 43))
                        elif value == "error":
                            item.setForeground(QColor(231, 76, 60))
                    
                    self.audit_table.setItem(row, col, item)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los registros:\n{str(e)}")

    def show_details(self):
        selected_row = self.audit_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Detalles", "Seleccione un registro para ver los detalles.")
            return
        
        # Obtener todos los datos de la fila seleccionada
        details = []
        for col in range(self.audit_table.columnCount()):
            header = self.audit_table.horizontalHeaderItem(col).text()
            value = self.audit_table.item(selected_row, col).text()
            details.append(f"{header}: {value}")
        
        # Mostrar en un cuadro de diálogo
        msg = QMessageBox()
        msg.setWindowTitle("Detalles del Registro de Auditoría")
        msg.setText("\n".join(details))
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def clear_audit_filters(self):
        self.audit_date_from.clear()
        self.audit_date_to.clear()
        self.audit_user_filter.clear()
        self.audit_action_filter.setCurrentIndex(0)
        self.audit_table_filter.setCurrentIndex(0)
        self.load_audit_data()

    def export_audit_logs(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Auditoría", 
            f"auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", 
            "CSV Files (*.csv)"
        )
        
        if not file_name:
            return
            
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                # Escribir encabezados
                headers = [self.audit_table.horizontalHeaderItem(i).text() 
                          for i in range(self.audit_table.columnCount())]
                f.write(','.join(headers) + '\n')
                
                # Escribir datos
                for row in range(self.audit_table.rowCount()):
                    row_data = []
                    for col in range(self.audit_table.columnCount()):
                        item = self.audit_table.item(row, col)
                        text = item.text() if item else ""
                        # Escapar comas en los datos
                        if ',' in text:
                            text = f'"{text}"'
                        row_data.append(text)
                    f.write(','.join(row_data) + '\n')
                    
            QMessageBox.information(self, "Éxito", f"Datos exportados correctamente a:\n{file_name}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{str(e)}")