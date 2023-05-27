import requests
import datetime
import time


states = ["CA", "UT", "AZ"]


def make_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


for state in states:
    current_date = datetime.date.today()
    end_of_year = datetime.date(current_date.year, 12, 31)
    print(f"=====BEGIN LOCATION SEARCH IN {state}======")
    while current_date <= end_of_year:
        api_url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots/asLocations?minimum=1&filterTimestampBy=on&timestamp={current_date}&serviceName=Global%20Entry"
        data = make_api_request(api_url)
        locations = list(filter(lambda p: p["state"] == state, data))
        if len(locations) > 0:
            names = list(map(lambda loc: f'NAME: {loc["name"]}, LOCATION: {loc["city"]}, {loc["state"]}', locations))
            print(f"APPOINTMENTS AVAILABLE ON {current_date}")
            print(f"LOCATIONS: {names}")
            print("==========================================")
        current_date += datetime.timedelta(days=1)
        time.sleep(.25)
