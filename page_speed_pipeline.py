import datetime
import gspread
import google.auth
import requests
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz

# Set the scope for the Google Sheets and Drive APIs
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']

# Load the service account credentials from the JSON key file
creds = ServiceAccountCredentials.from_json_keyfile_name("your/path/to/creds.json", scope)

api_key = 'INSERT_API_KEY_HERE'

api_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'

# Authorize the client using the service account credentials
client = gspread.authorize(creds)

# Open the "Page Speed Reporting" spreadsheet
spreadsheet = client.open("INSERT THE NAME OF YOUR GOOGLE SPREADSHEET HERE")

# Get the "Home Page" sheet
home_page = spreadsheet.worksheet("INSERT THE NAME OF YOUR GOOGLE SHEET HERE")

# Get the current date
today = datetime.datetime.now()

# List of URLs to test
urls = ['INSERT URL FOR PAGE SPEED HERE']

def test_page_speed(url, strategy):
  params = {
    'url': url,
    'key': api_key,
    'strategy': strategy
  }

  response = requests.get(api_url, params=params)
  if response.status_code != 200:
    print(f'Error: {response.status_code}')
    return

  data = response.json()

  if 'error' in data:
    print(f'Error: {data["error"]["message"]}')
    return

  page_speed_score = data["lighthouseResult"]["categories"]["performance"]["score"]
  return page_speed_score


# Test the page speed of each URL
for url in urls:
  mobile_speed = test_page_speed(url, 'mobile')
  desktop_speed = test_page_speed(url, 'desktop')

  year = today.strftime('%y')
  month = today.strftime('%m')
  day = today.strftime('%d')

  # Get the current time in PST
  pacific = pytz.timezone('US/Pacific')
  now_pst = datetime.datetime.now(pacific)
  time = now_pst.strftime('%I:%M %p')

  # Insert the data into the first row of the "Home Page" sheet
  home_page.insert_row([year, month, day, time, url, mobile_speed, desktop_speed], index=2)




