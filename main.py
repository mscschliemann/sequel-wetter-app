import requests as req
import re, os, json
import datetime
import gspread

data = {'time': [],
        'max': [],
        'min': []}

uris = ['https://www.wetter.de/deutschland/wetter-berlin-18228265.html?q=berlin',
        'https://www.wetter.de/deutschland/wetter-stuttgart-18224193.html?q=stuttgart',
        'https://www.wetter.de/usa/wetter-springfield-18820972/wetterprognose.html?q=Springfield,%20Missouri,%20Vereinigte%20Staaten%20von%20Amerika']

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
    API_key = 'bfc32c79f0c822551acce09747b834d3'
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

    gc = gspread.service_account()
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
