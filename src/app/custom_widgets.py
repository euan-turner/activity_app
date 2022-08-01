import sys, io
from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView

from api import api_setup, get_gpx_data

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






class TestMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        ##Default layout
        layout = QVBoxLayout()
        layout.setContentsMargins(5,5,5,5)

        ##Get gpx data
        api = api_setup("euanoturner@gmail.com", "C@nbera1")
        activity = api.get_activities_by_date('2022-05-02', '2022-05-02', 'running')[0]
        act_id = activity["activityId"]
        gpx = get_gpx_data(api, act_id)

        ##In program storage
        data = io.BytesIO(gpx)

        layout.addWidget(MapWidget(data))

        ##Adding to centre
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet('''QWidget { font-size : 35px;}''')
    window = TestMainWindow()
    window.show()
    app.exec()
