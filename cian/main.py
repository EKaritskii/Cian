import requests
import json
import datetime
from requests.exceptions import ConnectTimeout
from config_data.config import header, url_1, url_2, url_3


def validate(date_text):
    try:
        date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
        if str(date - datetime.datetime.today())[0] != '-' or str(date - datetime.datetime.today())[0] == '-1 ':
            return 0
        return 1
    except ValueError:
        return 0


def custom_key(diction):
    return diction['externalId']


def request_to_api(url, headers, querystring=''):
    try:
        response = requests.request(
            "GET", url, headers=headers, params=querystring
        )
        if response.status_code == requests.codes.ok:
            return response
    except ConnectTimeout:
        print("данные не коррестны!")
        return


decision = int(input('Выбор даты: самостоятельный ввод(1)/ вчерашний день(2)\nВыберите вариант (1/2): '))
try:
    if decision == 1:
        date = str(input('Введите дату (YYYY-MM-DD / DD.MM.YYYY):\n '))

        if date[4] == '-' and validate(date) == 1:
            date_1 = date
        elif date[2] == '.':
            date_spl = date.split('.')
            date = '{2}-{1}-{0}'.format(date_spl[0], date_spl[1], date_spl[2])
            if validate(date) == 1:
                date_1 = date
            else:
                date_1 = datetime.date.today() - datetime.timedelta(days=1)
        else:
            date_1 = datetime.date.today() - datetime.timedelta(days=1)
    else:
        date_1 = datetime.date.today() - datetime.timedelta(days=1)
except IndexError:
    date_1 = datetime.date.today() - datetime.timedelta(days=1)
response = request_to_api(url_1, header)
data = json.loads(response.text)
data_end = []


all_views = 0

for i in data['result']["offers"]:
    off_id = i['offerId']
    params = 'dateTo={0}&dateFrom={0}&offerId={1}'.format(date_1, off_id)
    response = request_to_api(url_2, header, params)
    data_2 = json.loads(response.text)
    params = 'offerId={1}&dateFrom={0}&dateTo={0}'.format(date_1, off_id)
    response = request_to_api(url_3, header, params)
    data_3 = json.loads(response.text)
    all_views += int(data_2['result']['searchesCount'])
    add_dict = {'externalId': str(i['externalId']), 'offerId': str(i['offerId']),
                'url': 'https://kvadrat48.ru/offers/object/{}'.format(i['externalId']),
                'status': str(i['status']), 'errors': str(i['errors']),  'warnings': str(i['warnings']),
                'searchesCount': str(data_2['result']['searchesCount']),
                'showsCount': str(data_2['result']['showsCount']),
                'viewsByDays': "", 'phoneShowsByDays': "", 'average_views%': ""}
    if len(data_3['result']['viewsByDays']) != 0:
        add_dict['viewsByDays'] = str(data_3['result']['viewsByDays'][0]['views'])
    if len(data_3['result']['phoneShowsByDays']) != 0:
        add_dict['phoneShowsByDays'] = str(data_3['result']['phoneShowsByDays'][0]['phoneShows'])
    data_end.append(add_dict)

data_end = sorted(data_end, key=lambda x: (data_end[0]['externalId']))
average_views = round(all_views / len(data_end) + 1, 1)
for i in data_end:
    i['average_views_%'] = str(round(int(i['searchesCount']) * 100 / average_views, 1)) + ' %'
    print(i)

csv_str = ''
for i in data_end[0].items():
    string = i[0]
    string += ';'
    csv_str += string

for i_1 in data_end:
    csv_str += '\n'
    for i_2 in i_1.items():
        string = i_2[1].replace('"', '""')
        string += ';'
        csv_str += string
print(csv_str)
with open('cain.csv', 'w', encoding='utf-8') as file:
    file.write(csv_str)
