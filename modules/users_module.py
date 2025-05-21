import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class UsersModule(QWidget):
    def __init__(self):
        super().__init__()
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '12345678',
            'database': 'hospitales'
        }
        self.init_ui()
        self.load_users_from_db()

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al conectar a la base de datos:\n{e}")
            return None

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Usuarios")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_layout = QHBoxLayout()

        self.user_search = QLineEdit()
        self.user_search.setPlaceholderText("Buscar usuarios...")

        search_btn = QPushButton("Buscar")
        search_btn.clicked.connect(self.filter_users)

        tool_layout.addWidget(self.user_search)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.user_table = QTableWidget(0, 6)
        self.user_table.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Rol", "Estado", "Contraseña"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.hideColumn(5)  # Oculta la contraseña

        layout.addWidget(self.user_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Usuario", self.agregar_usuario),
            ("Editar Usuario", self.editar_usuario),
            ("Cambiar Estado", self.toggle_user_status),
            ("Eliminar Usuario", self.eliminar_usuario),
            ("Exportar a CSV", self.export_users)
        ]
        for text, handler in actions:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_users_from_db(self):
        conexion = self.get_connection()
        if not conexion:
            return
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.usuario_id AS id, u.nombre, u.email, r.nombre AS rol, u.activo, u.contrasena
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.rol_id
            """)
            usuarios = cursor.fetchall()
            self.user_table.setRowCount(0)
            for usuario in usuarios:
                row = self.user_table.rowCount()
                self.user_table.insertRow(row)
                self.user_table.setItem(row, 0, QTableWidgetItem(str(usuario['id'])))
                self.user_table.setItem(row, 1, QTableWidgetItem(usuario['nombre']))
                self.user_table.setItem(row, 2, QTableWidgetItem(usuario['email']))
                self.user_table.setItem(row, 3, QTableWidgetItem(usuario['rol']))
                estado_texto = "Activo" if usuario['activo'] else "Inactivo"
                estado_item = QTableWidgetItem(estado_texto)
                estado_item.setForeground(QColor(0, 128, 0) if usuario['activo'] else QColor(192, 0, 0))
                self.user_table.setItem(row, 4, estado_item)
                self.user_table.setItem(row, 5, QTableWidgetItem(usuario['contrasena']))
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al consultar la base de datos:\n{e}")
        finally:
            conexion.close()

    def get_roles(self):
        conexion = self.get_connection()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM roles")
            roles = [row[0] for row in cursor.fetchall()]
            return roles
        except Error as e:
            QMessageBox.critical(self, "Error", f"No se pudieron obtener los roles:\n{e}")
            return []
        finally:
            conexion.close()

    def get_rol_id(self, nombre_rol):
        conexion = self.get_connection()
        if not conexion:
            return None
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT rol_id FROM roles WHERE nombre = %s", (nombre_rol,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        finally:
            conexion.close()

    def filter_users(self):
        texto = self.user_search.text().lower()
        for row in range(self.user_table.rowCount()):
            visible = any(
                texto in (self.user_table.item(row, col).text().lower() if self.user_table.item(row, col) else '')
                for col in range(5)  # Ignora contraseña
            )
            self.user_table.setRowHidden(row, not visible)
    
    def eliminar_usuario(self):
        fila = self.user_table.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Eliminar", "Seleccione un usuario.")
            return

        user_id = int(self.user_table.item(fila, 0).text())
        confirm = QMessageBox.question(self, "Confirmar", "¿Seguro que desea eliminar al usuario?", QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return

        conexion = self.get_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM usuarios WHERE usuario_id = %s", (user_id,))
                conexion.commit()
                QMessageBox.information(self, "Éxito", "Usuario eliminado.")
                self.load_users_from_db()
            except Error as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el usuario:\n{e}")
            finally:
                conexion.close()

    def agregar_usuario(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Usuario")
        dialog.setFixedSize(400, 300)

        layout = QVBoxLayout()
        nombre_input = QLineEdit()
        email_input = QLineEdit()
        rol_input = QComboBox()
        rol_input.addItems(self.get_roles())
        contrasena_input = QLineEdit()
        contrasena_input.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Nombre:")); layout.addWidget(nombre_input)
        layout.addWidget(QLabel("Email:")); layout.addWidget(email_input)
        layout.addWidget(QLabel("Rol:")); layout.addWidget(rol_input)
        layout.addWidget(QLabel("Contraseña:")); layout.addWidget(contrasena_input)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialog.accept)
        botones.rejected.connect(dialog.reject)
        layout.addWidget(botones)
        dialog.setLayout(layout)

        if dialog.exec_():
            rol_id = self.get_rol_id(rol_input.currentText())
            if not rol_id:
                QMessageBox.warning(self, "Error", "Rol no válido.")
                return

            conexion = self.get_connection()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("""
                        INSERT INTO usuarios (nombre, email, rol_id, activo, contrasena)
                        VALUES (%s, %s, %s, TRUE, %s)
                    """, (nombre_input.text(), email_input.text(), rol_id, contrasena_input.text()))
                    conexion.commit()
                    QMessageBox.information(self, "Éxito", "Usuario agregado.")
                    self.load_users_from_db()
                except Error as e:
                    QMessageBox.critical(self, "Error", f"No se pudo agregar el usuario:\n{e}")
                finally:
                    conexion.close()

    def editar_usuario(self):
        fila = self.user_table.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Editar", "Seleccione un usuario.")
            return

        user_id = int(self.user_table.item(fila, 0).text())
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Usuario")
        dialog.setFixedSize(400, 300)

        layout = QVBoxLayout()
        nombre_input = QLineEdit(self.user_table.item(fila, 1).text())
        email_input = QLineEdit(self.user_table.item(fila, 2).text())
        rol_input = QComboBox()
        roles = self.get_roles()
        rol_input.addItems(roles)
        rol_input.setCurrentText(self.user_table.item(fila, 3).text())

        layout.addWidget(QLabel("Nombre:")); layout.addWidget(nombre_input)
        layout.addWidget(QLabel("Email:")); layout.addWidget(email_input)
        layout.addWidget(QLabel("Rol:")); layout.addWidget(rol_input)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(dialog.accept)
        botones.rejected.connect(dialog.reject)
        layout.addWidget(botones)
        dialog.setLayout(layout)

        if dialog.exec_():
            rol_id = self.get_rol_id(rol_input.currentText())
            conexion = self.get_connection()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("""
                        UPDATE usuarios SET nombre=%s, email=%s, rol_id=%s WHERE usuario_id=%s
                    """, (nombre_input.text(), email_input.text(), rol_id, user_id))
                    conexion.commit()
                    QMessageBox.information(self, "Éxito", "Usuario actualizado.")
                    self.load_users_from_db()
                except Error as e:
                    QMessageBox.critical(self, "Error", f"No se pudo editar:\n{e}")
                finally:
                    conexion.close()

    def toggle_user_status(self):
        fila = self.user_table.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Estado", "Seleccione un usuario.")
            return

        user_id = int(self.user_table.item(fila, 0).text())
        actual = self.user_table.item(fila, 4).text() == "Activo"
        nuevo_estado = not actual

        conexion = self.get_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("UPDATE usuarios SET activo = %s WHERE usuario_id = %s", (nuevo_estado, user_id))
                conexion.commit()
                QMessageBox.information(self, "Éxito", "Estado actualizado.")
                self.load_users_from_db()
            except Error as e:
                QMessageBox.critical(self, "Error", f"No se pudo cambiar el estado:\n{e}")
            finally:
                conexion.close()

    def export_users(self):
        archivo, _ = QFileDialog.getSaveFileName(self, "Exportar Usuarios", "", "CSV Files (*.csv)")
        if not archivo:
            return
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                cabeceras = [self.user_table.horizontalHeaderItem(i).text() for i in range(5)]
                f.write(",".join(cabeceras) + "\n")
                for row in range(self.user_table.rowCount()):
                    fila = []
                    for col in range(5):
                        item = self.user_table.item(row, col)
                        fila.append(item.text() if item else "")
                    f.write(",".join(fila) + "\n")
            QMessageBox.information(self, "Éxito", "Usuarios exportados.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{e}")
