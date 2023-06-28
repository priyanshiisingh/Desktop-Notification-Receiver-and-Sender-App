import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit


class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notification Client")
        self.setGeometry(100, 100, 300, 150)

        self.message_input = QLineEdit()
        self.send_button = QPushButton("Send Notification")
        self.send_button.clicked.connect(self.send_notification)

        layout = QVBoxLayout()
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def send_notification(self):
        HOST = '172.29.1.111'  # Replace with the IP address of the target computer
        PORT = 12345

        message = self.message_input.text()

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(message.encode('utf-8'))

            print("Notification sent successfully.")
        except ConnectionRefusedError:
            print("Connection to the server failed.")
        finally:
            if client_socket:
                client_socket.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientWindow()
    window.show()
    sys.exit(app.exec())
