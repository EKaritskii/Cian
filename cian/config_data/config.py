import os
from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

API_KEY = os.getenv('api_key')
header = {
        "Authorization": "Bearer " + str(API_KEY)
    }
url_1 = 'https://public-api.cian.ru/v1/get-order'
url_2 = 'https://public-api.cian.ru/v1/get-search-coverage'
url_3 = 'https://public-api.cian.ru/v1/get-views-statistics-by-days'
