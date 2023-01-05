import sys, os 
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from datetime import datetime
from io import BytesIO 
from pandas import read_csv
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QLabel
from xml.etree.ElementTree import parse

from api import API

class ActivitySummaryWidget(QWidget):
    """
    Individual widget used for each activity
    Days with multiple activities can be formed with a stack
    """    

    def __init__(self, api : API, date : datetime):
        """Creates summary of activities on a day

        Args:
            api (API): Garmin API instance
            date (datetime): Date of day
        """        
        super().__init__()

        ##Can separate into categories to read from csv file(can be passed as parameter)
        ##And gpx and given categories
        ##Temporary format
        self.head_categories = ["Date", "Location"]
        self.csv_categories = ["Time", "Distance", "Elevation Gain", "Avg Pace", "Avg HR"]
        
        ##Date above stack
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(5)

        ##Add date above all activities
        self.add_label(self.layout, date.strftime("%Y-%m-%d"))

        #Stack for activity frames
        self.stack_layout = QStackedLayout()
        self.stack_layout.setContentsMargins(5,5,5,5)

        ##Retrieve all activities for the day
        activities = api.get_activities_by_date(date, date)
        self.num_frames = len(activities)

        ##Create frames for each activity
        for act in activities:
            act_id = act["activityId"]
            gpx_data = BytesIO(api.get_gpx_data(act_id))
            csv_data = BytesIO(api.get_csv_data(act_id))
        
            ##Arrange labels vertically
            frame = QVBoxLayout()
            frame.setSpacing(5)

            ##Add location label from gpx
            self.add_location(frame, gpx_data)

            ##Add data from csv
            self.add_csv_data(frame, csv_data)

            ##Add index label for user
            index = activities.index(act) + 1
            self.add_label(frame, f"{index} of {self.num_frames}", italic = True)

            ##Add layout to widget then stack
            frame_widget = QWidget()
            frame_widget.setLayout(frame)
            self.stack_layout.addWidget(frame_widget)
        
        ##Add stack to widget layout
        stack_widget = QWidget()
        stack_widget.setLayout(self.stack_layout)
        self.layout.addWidget(stack_widget)



        
    def add_label(self, frame : QVBoxLayout, text : str, italic : bool = False):
        """Adds a label to a specified layout frame

        Args:
            frame (QVBoxLayout): Frame to add label to
            text (str): Text for label
        """             
        ##May need to set maximum width for label
        label = QLabel()
        label.setText(text)
        font = label.font()
        font.setPointSize(12)
        font.setItalic(italic)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        frame.addWidget(label)

    def add_location(self, frame : QVBoxLayout, gpx_data : BytesIO):
        """Adds location title for an activity

        Args:
            frame (QVBoxLayout): Frame to add location label to
            gpx_data (BytesIO): In memory gpx file for activity
        """    
        tree = parse(gpx_data)
        root = tree.getroot()

        namespace = {"gpx" : "http://www.topografix.com/GPX/1/1"}
        location = root.find(".//gpx:name", namespace)

        self.add_label(frame, str(location.text))
    
    def add_csv_data(self, frame : QVBoxLayout, csv_data : BytesIO):
        """Adds data from csv file for an activity

        Args:
            frame (QVBoxLayout): Frame to add labels to
            csv_data (BytesIO): In memory csv file for activity
        """        
        act_data = read_csv(csv_data)
        summary = act_data.tail(1)

        for cat in self.csv_categories:
            val = summary[cat].values[0]
            self.add_label(frame, str(val))
    
    def mouseReleaseEvent(self, e : QMouseEvent):
        """Overrides the parent event handler
        Either iterates through stack

        Future: or selects activity for isolated view

        Args:
            e (QMouseEvent): Mouse event description
        """        
        ##Override event handler
        ##User wants next frame in stack
        if e.button() == Qt.MouseButton.RightButton:
            current = self.stack_layout.currentIndex()
            new = (current + 1) % self.num_frames
            self.stack_layout.setCurrentIndex(new)
        ##User wants to select activity
        elif e.button() == Qt.MouseButton.LeftButton:
            pass