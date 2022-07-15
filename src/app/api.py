from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)

def get_csv_data(api : Garmin, activity_id : str):
    """Gets the csv data for an activity from Garmin Connect API

    Args:
        api (Garmin): API instance from garminconnect
        activity_id (str): Activity ID

    Returns:
        str: Activity data in csv format
    """    
    csv_data = api.download_activity(activity_id, dl_fmt = api.ActivityDownloadFormat.CSV)
    return csv_data

def get_gpx_data(api : Garmin, activity_id : str):
    """Gets the gpx data for an activity from Garmin Connect API

    Args:
        api (Garmin): API instance from garminconnect
        activity_id (str): Activity ID

    Returns:
        str: Activity data in gpx (XML) format
    """    
    gpx_data = api.download_activity(activity_id, dl_fmt = api.ActivityDownloadFormat.GPX)
    return gpx_data.decode(encoding = 'utf-8')

def get_tcx_data(api : Garmin, activity_id : str):
    """Gets the tcx data for an activity from Garmin Connect API

    Args:
        api (Garmin): API instance from garminconnect
        activity_id (str): Activity ID

    Returns:
        str: Activity data in tcx (XML) format
    """    
    tcx_data = api.download_activity(activity_id, dl_fmt = api.ActivityDownloadFormat.TCX)
    return tcx_data.decode(encoding = 'utf-8')

def save_data(data, activity_id : str, suffix : str):  
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

def api_setup(username : str, password : str):
    """Initialises the API instance for a user

    Args:
        username (str): 
        password (str): 

    Returns:
        Garmin: Garmin API instance from garminconnect
    """    
    api = Garmin(username, password)
    api.login()
    return api



api = api_setup("euanoturner@gmail.com", "C@nbera1")
activities = api.get_activities_by_date('2022-05-02', '2022-05-02', 'running')
for activity in activities:
    activity_id = activity["activityId"]
    data = get_tcx_data(api, activity_id)
    print(data)

