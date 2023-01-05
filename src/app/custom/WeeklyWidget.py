import sys, os 
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from datetime import datetime, timedelta
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from ActivitySummaryWidget import ActivitySummaryWidget
from api import API

class WeeklyWidget(QWidget):

    def __init__(self, api : API, start_date : datetime, end_date : datetime):
        """Creates a summary of all activities from the week
        End date is exclusive (i.e. Monday to Monday)

        Args:
            api (API): Garmin API instance
            start_date (datetime): Start date
            end_date (datetime): End date
        """        

        super().__init__()

        self.api = api
        self.start = start_date
        self.end = end_date

        ##Arrange widgets horizontally
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(5,5,5,5)
        self.layout.setSpacing(5)

        ##Iterate over days in the week
        for date in self.week_dates():
            self.layout.addWidget(ActivitySummaryWidget(api, date))
    
    def week_dates(self):
        """Generator creating dates for the days in the given week

        Yields:
            datetime: Dates of days
        """        
        for n in range(int((self.end - self.start).days)):
            yield self.start + timedelta(n)