import argparse
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Obtain the api key from the environment variable
API_KEY = os.getenv('API_KEY')

# Obtain the api key that was passed in from the command line (overrides .env)
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default=API_KEY)
args = parser.parse_args()

# Use the API key from command line arguments or the .env file
API_KEY = args.api_key

# Sport key
SPORT = 'upcoming'

# Bookmaker regions
REGIONS = 'us'

# Odds markets
MARKETS = 'h2h,spreads'

# Odds format
ODDS_FORMAT = 'decimal'

# Date format
DATE_FORMAT = 'iso'

# First get a list of in-season sports
sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
    'api_key': API_KEY
})

if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
else:
    sports_data = sports_response.json()
    # Save sports data to a JSON file with indentation for readability
    with open('sports_data.json', 'w') as f:
        json.dump(sports_data, f, indent=4)

# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
    'api_key': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
})

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
else:
    odds_data = odds_response.json()
    # Save odds data to a JSON file with indentation for readability
    with open('odds_data.json', 'w') as f:
        json.dump(odds_data, f, indent=4)

    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])
