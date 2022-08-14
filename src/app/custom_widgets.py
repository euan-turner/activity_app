import sys, pandas as pd
import xml.etree.ElementTree as ET
from io import BytesIO
from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedLayout, QMainWindow, QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent

from api import API


class MapWidget(QWidget):
    """
    Loads a folium map of gpx file onto a widget
    """    
    def __init__(self, gpx_data : BytesIO):
        """Creates map widget from gpx

        Args:
            gpx_data (BytesIO): In memory gpx file for activity
        """        
        super().__init__()

        ##Default layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        ##Line properties - make customisable in future
        line_options = {
            'color' : 'red',
            'weight' : 5,
            'opacity' : 0.5,
        }

        ##Create folium map with gpxplotter
        route_map = create_folium_map(tiles = "stamenterrain")
        for track in read_gpx_file(gpx_data):
            print(track)
            for _, segment in enumerate(track['segments']):
                add_segment_to_map(route_map, segment, line_options = line_options)
        
        ##Save map to bytes
        data = BytesIO()
        route_map.save(data, close_file = False)

        ##Load map onto widget
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

class WeeklyActivitySummaryWidget(QWidget):
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
            self.add_label(frame, f"{index} of {self.num_frames}")

            ##Add layout to widget then stack
            frame_widget = QWidget()
            frame_widget.setLayout(frame)
            self.stack_layout.addWidget(frame_widget)
        
        ##Add stack to widget layout
        stack_widget = QWidget()
        stack_widget.setLayout(self.stack_layout)
        self.layout.addWidget(stack_widget)



        
    def add_label(self, frame : QVBoxLayout, text : str):
        """Adds a label to a specified layout frame

        Args:
            frame (QVBoxLayout): Frame to add label to
            text (str): Text for label
        """             
        ##May need to set maximum width for label
        label = QLabel()
        label.setText(text)
        font = label.font()
        font.setPointSize(8)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        frame.addWidget(label)

    def add_location(self, frame : QVBoxLayout, gpx_data : BytesIO):
        """Adds location title for an activity

        Args:
            frame (QVBoxLayout): Frame to add location label to
            gpx_data (BytesIO): In memory gpx file for activity
        """    
        tree = ET.parse(gpx_data)
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
        act_data = pd.read_csv(csv_data)
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

class WeeklyViewWidget(QWidget):

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
            self.layout.addWidget(WeeklyActivitySummaryWidget(api, date))
    
    def week_dates(self):
        """Generator creating dates for the days in the given week

        Yields:
            datetime: Dates of days
        """        
        for n in range(int((self.end - self.start).days)):
            yield self.start + timedelta(n)


'''
For single activity view:
Have a map widget
Have an info widget with distance, time, elevation, pace, hr, cadence
Have a widget with lap times
Info widget shows info for whole activity, or for selected lap
'''

'''
For weekly activity view
Arrange WeeklyActivitySummary widgets horizontally
For days with multiple activities, put activities in a stack
'''








class TestMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        ##Default layout
        layout = QVBoxLayout()
        layout.setContentsMargins(5,5,5,5)

        ##Get data
        api = API()
        api.setup("euanoturner@gmail.com", "C@nbera1")

        start = datetime.strptime("2022-05-01", "%Y-%m-%d")
        end = start + timedelta(weeks = 1)

        widg = WeeklyViewWidget(api, start, end)

        layout.addWidget(widg)

        ##Adding to centre
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestMainWindow()
    window.show()
    app.exec()
