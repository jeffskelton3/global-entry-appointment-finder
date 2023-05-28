import csv
import json

import requests
import datetime
import time
import argparse
import os
import us
import concurrent.futures
from tqdm import tqdm

API_URL = f"https://ttp.cbp.dhs.gov/schedulerapi/slots/asLocations?minimum=1&filterTimestampBy=on&timestamp={current_date}&serviceName=Global%20Entry"
valid_state_codes = list(map(lambda s: s.abbr, us.states.STATES))

parser = argparse.ArgumentParser(description='Global Entry Appointment Finder')
parser.add_argument('--states', required=True, nargs='+', type=str, help='List of two-letter state codes to search')
parser.add_argument('--interval', required=False, type=int, default=.25, help='Interval between API calls in seconds')
parser.add_argument('--output', required=True, type=str, help='Path to output CSV file')
parser.add_argument('--enddate', required=False, type=str, default='', help='End date for search in MM-DD-YYYY format')

args = parser.parse_args()
now = datetime.date.today()
end_date = datetime.date(now.year, 12, 31)

if args.enddate:
    try:
        end_date = datetime.datetime.strptime(args.enddate, '%m-%d-%Y').date()
        if end_date < now:
            print("End date must be in the future.")
            exit(1)
    except ValueError:
        print("Invalid end date format. Please use DD-MM-YYYY format.")
        exit(1)


def make_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


def search_locations_for_state(state):
    if state not in valid_state_codes:
        print(f"Invalid state code: {state}")
        exit(1)
    available_locations = []
    current_date = now
    progress_bar = tqdm(total=(end_date - current_date).days + 1, desc=f"=Searching {state}",
                        postfix='', bar_format='{desc}: {bar} {percentage:3.0f}%|{bar}')
    while current_date <= end_date:
        data = make_api_request(API_URL)
        locations = list(filter(lambda p: p["state"] == state, data))
        if len(locations) > 0:
            for loc in locations:
                csv_row = {
                    'ID': loc['id'],
                    'Date': str(current_date),
                    'State': state,
                    'Name': loc['name'],
                    'Address': f'{loc["address"]} {loc["addressAdditional"]}',
                    'City': loc['city'],
                    'Zip': loc['postalCode'],
                    'Phone': loc['phoneNumber'],
                }
                available_locations.append(csv_row)
        current_date += datetime.timedelta(days=1)
        time.sleep(args.interval)
        progress_bar.update(1)
    progress_bar.close()
    return available_locations


def main():
    available_locations = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for state in args.states:
            futures.append(executor.submit(search_locations_for_state, state))

        for future in concurrent.futures.as_completed(futures):
            available_locations.extend(future.result())

    if len(available_locations) > 0:
        output_path = os.path.expanduser(args.output)
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Date', 'State', 'Name', 'Address', 'City', 'Zip', 'Phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(available_locations)
        print(json.dumps(available_locations, indent=4, sort_keys=True))
        print(f"Available locations saved to: {output_path}")
    else:
        print("No available locations found.")


if __name__ == '__main__':
    main()
