from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)
from io import BytesIO
from datetime import datetime

class API():

    def setup(self, username : str, password : str):
        """Initialises the garmin connect API instance and logs in

        Args:
            username (str): Given username, typically email
            password (str): Given password, in plaintext

        Returns:
            bool: Login success
        """        
        try:
            self.garmin = Garmin(username, password)
            result = self.garmin.login()
            return True
        except GarminConnectAuthenticationError:
            return False
    
    def get_activities_by_date(self, start_date : datetime, end_date : datetime, activity_type : str = "running"):
        """Retrieves multiple activities within a date range from Garmin API

        Args:
            start_date (datetime): Start of date range
            end_date (datetime): End of date range
            activity_type (str, optional): Activity type in garmin. Defaults to "running".

        Returns:
            list: JSON descriptions of activities within range
        """        
        ##Strip text format of date
        start = start_date.strftime("%Y-%m-%d")
        end = end_date.strftime("%Y-%m-%d")
        activities = self.garmin.get_activities_by_date(start, end, activity_type)
        ##Sort into chronological order
        activities.sort(key = lambda activity : datetime.strptime(activity["startTimeLocal"], "%Y-%m-%d %H:%M:%S"))
        
        return activities 

    def get_csv_data(self, activity_id : str):
        """Gets the csv data for an activity from Garmin Connect API

        Args:
            activity_id (str): Activity ID

        Returns:
            str: Activity data in csv format
        """    
        csv_data = self.garmin.download_activity(activity_id, dl_fmt = self.garmin.ActivityDownloadFormat.CSV)
        return csv_data

    def get_gpx_data(self, activity_id : str, as_string : bool = False):
        """Gets the gpx data for an activity from Garmin Connect API

        Args:
            activity_id (str): Activity ID
            as_string (bool): Whether bytes-type should be converted to string-type

        Returns:
            bytes (or str): Activity data in gpx (XML) format
        """    
        gpx_data = self.garmin.download_activity(activity_id, dl_fmt = self.garmin.ActivityDownloadFormat.GPX)
        if as_string:
            return gpx_data.decode(encoding = 'utf-8')
        else:
            return BytesIO(gpx_data)

    def get_tcx_data(self, activity_id : str, as_string : bool = False):
        """Gets the tcx data for an activity from Garmin Connect API

        Args:
            activity_id (str): Activity ID
            as_string (bool): Whether bytes-type should be converted to string-type

        Returns:
            bytes (or str): Activity data in tcx (XML) format
        """    
        tcx_data = self.garmin.download_activity(activity_id, dl_fmt = self.garmin.ActivityDownloadFormat.TCX)
        if as_string:
            return tcx_data.decode(encoding = 'utf-8')
        else:
            return BytesIO(tcx_data)

    def save_data(self, data, activity_id : str, suffix : str):  
        """Saves activity data to a file
        May not be needed if data can be processed within the program

        Args:
            data (): Data from garmin connect
            activity_id (str): Activity ID
            suffix (str): filetype suffix
        """     
        output_file = f"./src/app/activity_files/{str(activity_id)}.{suffix}"
        with open(output_file, "wb") as of:
            of.write(data)


if __name__ == "__main__":
    api = API()
    api.setup("euanoturner@gmail.com", "C@nbera1")
    #activities = api.garmin.get_activities_by_date('2022-05-02', '2022-05-02', 'running')
    start = datetime.strptime('2022-05-01', "%Y-%m-%d")
    end = datetime.strptime('2022-05-07', "%Y-%m-%d")
    activities = api.get_activities_by_date(start, end)
 
