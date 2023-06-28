import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from plyer import notification
from threading import Thread


class ServerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notification Server")
        self.setGeometry(100, 100, 200, 100)

        self.start_button = QPushButton("Start Server")
        self.start_button.clicked.connect(self.start_server)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.server_socket = None

    def start_server(self):
        self.start_button.setEnabled(False)
        Thread(target=self.run_server).start()

    def run_server(self):
        HOST = '0.0.0.0'  # Use 0.0.0.0 to listen on all available interfaces
        PORT = 12345

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)

        print(f"Server listening on {HOST}:{PORT}...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address} established.")

            message = client_socket.recv(1024).decode('utf-8')

            notification.notify(
                title='Notification',
                message=message,
                timeout=5
            )

            client_socket.close()

    def closeEvent(self, event):
        if self.server_socket:
            self.server_socket.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerWindow()
    window.show()
    sys.exit(app.exec())
