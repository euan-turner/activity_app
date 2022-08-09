import sys, io, pandas as pd
import xml.etree.ElementTree as ET
from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMainWindow, QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt

from api import API

class MapWidget(QWidget):
    """Loads a folium map of gpx file onto a widget
    """    
    def __init__(self, gpx_data : io.BytesIO):
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
        data = io.BytesIO()
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

    def __init__(self, activity_csv : io.BytesIO, activity_gpx : io.BytesIO):
        super().__init__()

        self.csv = activity_csv
        self.gpx = activity_gpx

        self.categories = ["Location", "Time", "Distance", "Elevation Gain", "Avg Pace", "Avg HR"]
        
        ##Arrange widgets vertically
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(5,5,5,5)
        self.layout.setSpacing(5)

        ##Add location label from gpx
        self.add_location()

        ##Add data from csv
        self.add_csv_data()

        
    def add_label(self, text : str):
        """Makes an activity data label
        Adds label to widget layout

        Args:
            text (str): Activity data
        """        
        ##May need to set maximum width for label
        label = QLabel()
        label.setText(text)
        font = label.font()
        font.setPointSize(8)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(label)

    def add_location(self):
        """Retrieves name(location) of activity from garmin gpx
        Adds label to widget layout
        """        
        tree = ET.parse(self.gpx)
        root = tree.getroot()

        namespace = {"gpx" : "http://www.topografix.com/GPX/1/1"}
        location = root.find(".//gpx:name", namespace)

        self.add_label(str(location.text))
    
    def add_csv_data(self):
        """Retrieves data from csv
        Adds a label for each category
        """        
        act_data = pd.read_csv(self.csv)
        summary = act_data.tail(1)

        for cat in self.categories[1::]:
            val = summary[cat].values[0]
            self.add_label(str(val))
        




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
        activity = api.garmin.get_activities_by_date('2022-05-02', '2022-05-02', 'running')[0]
        act_id = activity["activityId"]
        gpx = api.get_gpx_data(act_id)
        csv = api.get_csv_data(act_id)

        ##In program storage
        gpx_data = io.BytesIO(gpx)
        csv_data = io.BytesIO(csv)

        layout.addWidget(WeeklyActivitySummaryWidget(csv_data, gpx_data))

        ##Adding to centre
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestMainWindow()
    window.show()
    app.exec()
