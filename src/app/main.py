import sys, os 
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from datetime import datetime 
from PyQt6.QtWidgets import QMainWindow, QApplication

from api import API
from custom.MapWidget import MapWidget
from custom.LogInWindow import LogInWidget

class MainWindow(QMainWindow):

  def __init__(self, api: API):
    super().__init__()
    
    # Fixed date for now
    date = datetime.strptime('2023-01-01', '%Y-%m-%d')
    activity = api.get_activities_by_date(date, date)[0]
    gpx = api.get_gpx_data(activity["activityId"])
    self.setCentralWidget(MapWidget(gpx))

if __name__ == "__main__":
  valid = False
  while not valid:
    email = input("Enter email: ")
    password = input("Enter password: ")
    api = API()
    valid = api.setup(email, password)
  app = QApplication(sys.argv)
  window = MainWindow(api)
  window.show()
  app.exec()