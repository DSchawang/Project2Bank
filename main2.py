from PyQt6.QtWidgets import QApplication
import sys

from guilogic import BankGUI


def main():
    app = QApplication(sys.argv)
    window = BankGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
