import json
import csv
import requests
import datetime
import time
import argparse
import os
import us
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Global Entry Appointment Finder')
valid_state_codes = list(map(lambda s: s.abbr, us.states.STATES))
parser.add_argument('--states', required=True, nargs='+', type=str, help='List of two letter state codes to search')
parser.add_argument('--interval', required=False, type=int, default=.25, help='Interval between API calls in seconds')
parser.add_argument('--output', required=True, type=str, help='Path to output CSV file')

args = parser.parse_args()


def make_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


for state in args.states:
    if state not in valid_state_codes:
        print(f"Invalid state code: {state}")
        exit(1)

available_locations = []

for state in args.states:
    current_date = datetime.date.today()
    end_of_year = datetime.date(current_date.year, 12, 31)
    print(f"=====BEGIN LOCATION SEARCH IN {state}======")
    progress_bar = tqdm(total=(end_of_year - current_date).days + 1)
    while current_date <= end_of_year:
        api_url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots/asLocations?minimum=1&filterTimestampBy=on&timestamp={current_date}&serviceName=Global%20Entry"
        data = make_api_request(api_url)
        locations = list(filter(lambda p: p["state"] == state, data))
        if len(locations) > 0:
            csv_row = {
                'Date': str(current_date),
                'State': state,
                'Locations': ', '.join([loc['name'] for loc in locations])
            }
            available_locations.append(csv_row)
        current_date += datetime.timedelta(days=1)
        time.sleep(args.interval)
        progress_bar.update(1)
    progress_bar.close()

if len(available_locations) > 0:
    output_path = os.path.expanduser(args.output)
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'State', 'Locations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(available_locations)
    print(f"Available locations saved to: {output_path}")
else:
    print("No available locations found.")
