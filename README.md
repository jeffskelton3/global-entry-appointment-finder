# Global Entry Appointment Finder

The Global Entry Appointment Finder is a Python script that allows you to search for available Global Entry appointment slots in specific states within a specified date range. It retrieves appointment availability data from the U.S. Customs and Border Protection (CBP) API and outputs the results to a CSV file.

## Prerequisites

- Python 3.10 or above
- Poetry package manager (install instructions: [Poetry Installation Guide](https://python-poetry.org/docs/#installation))

## Usage

1. Clone the repository or download the script file (`main.py`) to your local machine.

2. Open a terminal and navigate to the project directory.

3. Install the project dependencies using Poetry:

   ```
   poetry install
   ```

4. Run the script with the desired command-line arguments:

   ```
   poetry run python main.py --states CA TX --interval 0.5 --output ~/Desktop/available_locations.csv --enddate 12-31-2023
   ```

   **Command-line Arguments:**
    - `--states` (required): Specify the states to search for available appointments. You can provide multiple state codes separated by spaces.
    - `--interval` (optional): Specify the time interval (in seconds) between API requests. Default is 0.25 seconds.
    - `--output` (required): Specify the output file path for saving the available locations. You can use Unix shorthand notation like `~/Desktop`.
    - `--enddate` (optional): Specify the end date for the search in MM-DD-YYYY format. If not provided, it defaults to the end of the current year.

5. The script will start searching for available appointment slots within the specified states and date range. It will display a progress bar indicating the search progress. Once the search is complete, it will save the available locations to the specified output file in CSV format.

## Output

The script outputs the available locations in CSV format. The CSV file contains the following columns:

- `ID`: The ID of the location.
- `Date`: The date of the available appointment slot.
- `State`: The state code where the appointment is available.
- `Name`: The name of the location.
- `Address`: The address of the location.
- `City`: The city of the location.
- `Zip`: The ZIP code of the location.
- `Phone`: The phone number of the location.

## Notes

- The script uses the U.S. Customs and Border Protection (CBP) API to retrieve appointment availability data. The availability and accuracy of the data depend on the API's reliability and updates from CBP. Please note that appointment availability may vary and cannot be guaranteed.
- The script adheres to CBP's rate limits and includes a delay (`--interval`) between API requests to avoid overwhelming the API server. The default interval is 0.25 seconds, but you can adjust it as needed. Be mindful of the rate limits and considerate of the server resources.

## License

This script is licensed under the [MIT License](LICENSE).

## Disclaimer

This script is provided as-is, without any warranty or guarantee. Use it at your own risk. The authors are not responsible for any misuse, unauthorized access, or legal implications arising from the use of this script.
