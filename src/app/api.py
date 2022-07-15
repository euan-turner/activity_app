from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)

def get_csv_data(api : Garmin, activity_id : str):
    """Gets the csv data for an activity id from Garmin Connect API

    Args:
        api (Garmin): API instance from garminconnect
        activity_id (str): Activity ID

    Returns:
        str: Activity data in csv format
    """    
    csv_data = api.download_activity(activity_id, dl_fmt = api.ActivityDownloadFormat.CSV)
    return csv_data

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



api = Garmin("euanoturner@gmail.com", "C@nbera1")
api.login()
activities = api.get_activities_by_date('2022-05-02', '2022-05-02', 'running')
for activity in activities:
    activity_id = activity["activityId"]
    data = get_csv_data(api, activity_id)

