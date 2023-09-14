import sys
import socket
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit,
                             QTextEdit, QMessageBox)
from codecs import decode


def connect_to_sign(ip_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_address, port))
    return s

def send_to_sign(s):
    steps = [
        (10000, b'\x01Z00\x02E$$$$\x04'),
        (500, b'SETPLAYLISTTOC'),
        (500, b'\x01Z00\x02E#DE\x04'),
        (500, b'\x01Z00\x02E.SLA\x04'),
        (500, b'\x01Z00\x02E#T1\x04'),
        (500, b'\x01Z00\x02E#MbOb\x04'),
        (500, b'\x01Z00\x02AATHIS SIGN IS NOW SETUP FOR ADP PROTOCOL\x04'),
    ]

    success = True
    for i in steps:
        data = i[1]
        try:
            print(f"sending {i}")
            s.sendall(data)
            time.sleep(i[0] / 1000)
        except Exception as e:
            success = False
            print(f"Error while sending step {i}: {e}")

    if success:
        print("ADP LOAD SUCCESSFUL")
    else:
        print("Error occurred during ADP load")

def send_test_string(s, test_string):
    data = decode("01", "hex") + "Z00".encode() + decode("02", "hex") + f"AA{test_string}".encode() + decode("04", "hex")
    s.sendall(data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ADP Setup v.1.0")
        self.resize(500, 300)

        layout = QVBoxLayout()

        self.ip_address_label = QLabel("Enter sign IP ADDRESS:")
        self.ip_address_input = QLineEdit()
        self.port_label = QLabel("Enter a port number:")
        self.port_input = QLineEdit()

        layout.addWidget(self.ip_address_label)
        layout.addWidget(self.ip_address_input)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.on_connect_button_click)
        layout.addWidget(self.connect_button)

        self.load_adp_button = QPushButton("Load ADP")
        self.load_adp_button.clicked.connect(self.on_load_adp_button_click)
        self.load_adp_button.setEnabled(False)
        layout.addWidget(self.load_adp_button)

        self.test_string_label = QLabel("Enter a message:")
        self.test_string_input = QLineEdit()
        layout.addWidget(self.test_string_label)
        layout.addWidget(self.test_string_input)

        self.test_button = QPushButton("Send Text to sign")
        self.test_button.clicked.connect(self.on_test_button_click)
        self.test_button.setEnabled(False)
        layout.addWidget(self.test_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.socket = None

    def on_connect_button_click(self):
        ip_address = self.ip_address_input.text()
        port = int(self.port_input.text())
        try:
            self.socket = connect_to_sign(ip_address, port)
            QMessageBox.information(self, "Connection", "Connection Established")
            self.load_adp_button.setEnabled(True)
            self.test_button.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Connection", f"Error: {e}")

    def on_load_adp_button_click(self):
        if self.socket:
            try:
                send_to_sign(self.socket)
                QMessageBox.information(self, "Load ADP", "ADP LOAD SUCCESSFUL")
            except Exception as e:
                QMessageBox.warning(self, "Load ADP", f"Error while loading ADP: {e}")
        else:
            QMessageBox.warning(self, "Error", "Socket not initialized. Please connect first.")

    def on_test_button_click(self):
        test_string = self.test_string_input.text()
        if self.socket:
            try:
                send_test_string(self.socket, test_string)
                QMessageBox.information(self, "Test String", "Test string sent successfully")
            except Exception as e:
                QMessageBox.warning(self, "Test String", f"Error while sending test string: {e}")
        else:
            QMessageBox.warning(self, "Error", "Socket not initialized. Please connect first.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())



