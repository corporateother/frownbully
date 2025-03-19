from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt  # Import Qt for alignment
import sys


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Frownbully")
        self.setGeometry(100, 100, 500, 300)

        # Layout setup
        layout = QVBoxLayout()

        # Header and Subheader
        self.header_label = QLabel("Turn that frown upside down!", self)
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centering text
        layout.addWidget(self.header_label)

        # Start Button
        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet(
            "background-color: #66CC99; color: white; font-size: 16px; padding: 10px; border-radius: 5px; font-weight: bold; border: 2px solid #444;")
        self.start_button.clicked.connect(self.start_action)
        layout.addWidget(self.start_button)

        # Stop Button
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet(
            "background-color: #FF6699; color: white; font-size: 16px; padding: 10px; border-radius: 5px; font-weight: bold; border: 2px solid #444;")
        self.stop_button.clicked.connect(self.stop_action)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def start_action(self):
        self.start_button.setText("Running")
        self.start_button.setStyleSheet(
            "background-color: #FFD700; color: black; font-size: 16px; padding: 10px; border-radius: 5px; font-weight: bold; border: 2px solid #444;")

    def stop_action(self):
        self.start_button.setText("Start")
        self.start_button.setStyleSheet(
            "background-color: #66CC99; color: white; font-size: 16px; padding: 10px; border-radius: 5px; font-weight: bold; border: 2px solid #444;")


app = QApplication(sys.argv)
window = MyWindow()
window.show()

# Apply a custom global stylesheet
app.setStyleSheet(
    "QWidget { background-color: #F8E8EE; color: black; padding: 20px; font-family: 'Courier New', monospace; }")

sys.exit(app.exec())
