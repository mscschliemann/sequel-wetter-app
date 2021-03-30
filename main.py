import requests as req
import re, os, json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#from boto.s3.connection import S3Connection

data = {'time': [],
        'max': [],
        'min': []}

uris = ['https://www.wetter.de/deutschland/wetter-berlin-18228265.html?q=berlin',
        'https://www.wetter.de/deutschland/wetter-stuttgart-18224193.html?q=stuttgart',
        'https://www.wetter.de/usa/wetter-springfield-18820972/wetterprognose.html?q=Springfield,%20Missouri,%20Vereinigte%20Staaten%20von%20Amerika']


def create_keyfile_dict():
    variables_keys = {
        "type": os.environ.get("SHEET_TYPE"),
        "project_id": os.environ.get("SHEET_PROJECT_ID"),
        "private_key_id": os.environ.get("SHEET_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("SHEET_PRIVATE_KEY"),
        "client_email": os.environ.get("SHEET_CLIENT_EMAIL"),
        "client_id": os.environ.get("SHEET_CLIENT_ID"),
        "revoke_uri": os.environ.get("SHEET_AUTH_URI"),
        "token_uri": os.environ.get("SHEET_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("SHEET_CLIENT_X509_CERT_URL")
    }
    return variables_keys

key_dict = create_keyfile_dict()
print(key_dict)


for uri in uris:
    html = req.get(uri)

    pattern_max = re.compile("<div class=\"weather-daybox__minMax__max\">")
    pattern_min = re.compile("<div class=\"weather-daybox__minMax__min\">")

    temp = pattern_max.search(html.text).end()
    max_temp = int(html.text[temp:temp+2].replace('°', ''))


    temp = pattern_min.search(html.text).end()
    min_temp = int(html.text[temp:temp+2].replace('°', ''))

    loc = uri.split('=')[1].capitalize().split(',')[0]

    city_name = loc
    API_key = os.environ.get("open_weather_api_key")
    unit = 'metric'
    lang = 'de'

    api_url = f'http://api.openweathermap.org/data/2.5/weather?\
q={city_name}&\
appid={API_key}&\
units={unit}&\
lang={lang}'

    response = req.get(api_url).json()
    status =  response['weather'][0]['description']


    print(f'{loc} Temperatur {str(datetime.datetime.now())}')
    print(f'max: {max_temp}')
    print(f'min: {min_temp}')
    print(f"status: {status}")
    print()

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    print("A")
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    print("B")
    gc = gspread.authorize(credentials)
    sh = gc.open("data")
    worksheet = sh.get_worksheet(0)

    new_row = [str(datetime.datetime.now()), max_temp, min_temp, loc, status]
    worksheet.append_row(new_row)




      
##if not os.path.exists('data.json'):
##    with open('data.json', 'w') as f:
##        json.dump(data, f)
##
##
##with open('data.json', 'r') as f:
##    data = json.load(f)
##
##data['time'].append(str(datetime.datetime.now()))
##data['max'].append(max_temp)
##data['min'].append(min_temp)
##
##with open('data.json', 'w') as f:
##    json.dump(data, f, indent=4)
