from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)


class API():

    def setup(self, username : str, password : str):
        """Initialises the API instance for a user

        Args:
            username (str): 
            password (str): 

        Returns:
            Garmin: Garmin API instance from garminconnect
        """    
        try:
            self.garmin = Garmin(username, password)
            self.garmin.login()
        except GarminConnectAuthenticationError as e:
            return e

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
            return gpx_data

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
            return tcx_data

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
    activities = api.garmin.get_activities_by_date('2022-05-02', '2022-05-02', 'running')
    for activity in activities:
        activity_id = activity["activityId"]
        tcx = api.get_tcx_data(activity_id)
        api.save_data(tcx, activity_id, 'tcx')
        gpx = api.get_gpx_data(activity_id)
        api.save_data(gpx, activity_id, 'gpx')
        csv = api.get_csv_data(activity_id)
        api.save_data(csv, activity_id, 'csv')

