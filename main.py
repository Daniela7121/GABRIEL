from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtGui import QFont
from views.login_view import LoginWindow


def main():
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    app.setFont(QFont("Segoe UI", 11))

    login = LoginWindow()
    login.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()