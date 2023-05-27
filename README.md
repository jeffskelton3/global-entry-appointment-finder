# Global Entry Appointment Finder

Solves a very specific need I have around finding an available [Global Entry](https://www.cbp.gov/travel/trusted-traveler-programs/global-entry) appointment in my state and the surrounding ones. The default UI is _really_ bad and the only hope of getting an appointment is if one gets cancelled, so I automated the act of checking for open slots.

NOTE: this runs an API request in a loop. I've added a bit of a delay before the next request runs, but be aware you might get rate limited or even blocked if you run this too much. Use responsibly.

### Setup

Make sure you have poetry installed and are running python 3.10.x

### Usage

The script expects a list of two letter state codes to check for appointments in and the path to output your results to. For example, to check for appointments in California, Utah, and Arizona:

`python -m main --states CA UT AZ --output=~/Desktop/results.csv`

The script also accepts an optional `--interval` argument that specifies how long to wait between API requests. The default is 250 ms.


Thats... pretty much it.
