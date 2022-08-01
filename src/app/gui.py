import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import Qt 

class LogInWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Garmin Buddy")

        ##Arrange widgets vertically
        layout = QVBoxLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(5)

        ##Arrange buttons horizontally
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        ##Label widget
        label = QLabel("Login to Garmin Connect")
        font = label.font()
        font.setPointSize(18)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        layout.addWidget(label)

        ##Email entry widget
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Email")

        ##Password entry widget
        self.pass_entry = QLineEdit()
        self.pass_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_entry.setPlaceholderText("Password")

        ##Submit button widget
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_entries)

        ##Clear button widget
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_entries)

        ##Adding widgets to layout
        layout.addWidget(self.email_entry)
        layout.addWidget(self.pass_entry)

        button_layout.addWidget(submit_button)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        ##Adding layout to window
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def submit_entries(self):
        email = self.email_entry.text()
        password = self.pass_entry.text()
        print(email, password)
    
    def clear_entries(self):
        self.email_entry.clear()
        self.pass_entry.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogInWindow()
    window.show()
    app.exec()





