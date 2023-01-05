from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map
from io import BytesIO
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout


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
            for _, segment in enumerate(track['segments']):
                add_segment_to_map(route_map, segment, line_options = line_options)
        
        ##Save map to bytes
        data = BytesIO()
        route_map.save(data, close_file = False)

        ##Load map onto widget
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)