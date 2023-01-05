import sys, os 
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox, QApplication

from api import API

class LogInWidget(QWidget):
    """Runs the log-in window
    Inherits from QMainWindow
    Sets the Garmin connection for an API instance after authentication
    """    

    def __init__(self, api : API):
        """

        Args:
            api (API): Stores garminconnect API instance for external access
        """        
        super().__init__()

        self.api = api

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

    
    def submit_entries(self):
        """Slot for submit button signal
        Validates login and runs dialogs
        """        
        email = self.email_entry.text()
        password = self.pass_entry.text()
        success = self.api.setup(email, password)
        if success:
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Login")
            dialog.setText("Login successful")
            dialog.exec()
        else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Login")
            dialog.setText("Login unsuccessful\nInvalid details")
            dialog.exec()
            self.clear_entries()
    
    def clear_entries(self):
        """Slot for clear button signal
        """        
        self.email_entry.clear()
        self.pass_entry.clear()
