import requests
import re, os, json, sys
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

data = {'time': [],
        'max': [],
        'min': []}

cities = ['Berlin', 'Stuttgart', 'Springfield']
c_keys = [2950159, 2825297, 4409896]

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

def create_keyfile_dict():
    variables_keys = {
        "type": os.environ.get("SHEET_TYPE"),
        "project_id": os.environ.get("SHEET_PROJECT_ID"),
        "private_key_id": os.environ.get("SHEET_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("SHEET_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.environ.get("SHEET_CLIENT_EMAIL"),
        "client_id": os.environ.get("SHEET_CLIENT_ID"),
        "auth_uri": os.environ.get("SHEET_AUTH_URI"),
        "token_uri": os.environ.get("SHEET_TOKEN_URI"),
        "revoke_uri": os.environ.get("SHEET_REVOKE_URI"),
        "auth_provider_x509_cert_url": os.environ.get("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("SHEET_CLIENT_X509_CERT_URL")
    }
    return variables_keys

credentials = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(), scopes=scope)
#credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scopes=scope)

gc = gspread.authorize(credentials)
sh = gc.open("data")
worksheet = sh.get_worksheet(0)

API_key = 'bfc32c79f0c822551acce09747b834d3'
unit = 'metric'
lang = 'de'

for city_id in c_keys:

    uri = f'http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_key}&units={unit}&lang={lang}'
    response = requests.get(uri).json()
        
    print('rain: ', response['rain'], file=sys.stderr)

    status = response['weather'][0]['description']
    temp = response['main']['temp']
    press = response['main']['pressure']
    humid = response['main']['humidity']
    wind = response.get('wind', {'speed': 'na'})['speed']
    cloudy = response.get('clouds', {'all': 'na'})['all']
    rain = response.get('rain', {'rain.1h': 'na'})['rain.1h']
    loc = response['name']

    time = response['dt']

##    print(city_id)
##    print()
##    print(status)
##    print(temp)
##    print(press)
##    print(humid)
##    print(wind)
##    print(cloudy)
##    print(rain)
##    print(loc)
##    print(time)


    new_row = [str(datetime.datetime.now()), temp, press, humid, wind, cloudy, rain, loc, status]
    worksheet.append_row(new_row)

