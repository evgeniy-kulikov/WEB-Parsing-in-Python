# 3.4 Статус коды
""""""

"""
Коды ответа HTTP

Информационные 100 - 199
Успешные 200 - 299
Перенаправления 300 - 399
Клиентские ошибки 400 - 499
Серверные ошибки 500 - 599
"""

# Используя атрибут status_code , мы можем увидеть, какой код мы получили в ответ.
import requests

url = 'http://httpbin.org/'
response = requests.get(url)
print(response.status_code)
# 200


# Также мы можем совершить проверку статус кода. И отталкиваясь от этого строить свой код.
import requests

url = 'http://httpbin.org/'
response = requests.get(url)
if response.status_code == 200:
    print("status_code OK")
else:
    print("status_code NOT OK")
    # status_code OK

"""
Это может пригодиться, когда сервер позволяет совершать определенное количество запросов 
за определенный промежуток времени, и, чтобы наш скрипт не падал,  мы можем добавить ожидание. 
Если статус-код не равен 200, спим 60 секунд, иначе продолжаем выполнение скрипта.
"""
import requests
import time

url = 'http://httpbin.org/'
response = requests.get(url)
if response.status_code != 200:
    time.sleep(60)
else:
    print("status_code OK... Continue execute code...")
# status_code OK... Continue execute code...


#
#  *  *  *   Задачи   *  *  *
#

import requests

for el in range(1, 501):
    url = f'https://parsinger.ru/task/1/{el}.html'
    response = requests.get(url)
    if response.status_code == 200:
        print(url)
        break

# https://parsinger.ru/task/1/333.html
# 9876316843187416358741341687416874165432


# Хорошее решение
import requests
import webbrowser
from bs4 import BeautifulSoup
from tqdm import tqdm  # прогресс бар

for el in tqdm(range(1, 501)):  # for el in tqdm(range(331, 500)):
    url = f'https://parsinger.ru/task/1/{el}.html'
    response = requests.get(url, timeout=1)
    if response.status_code == 200:
        print('\n', url)
        webbrowser.open(url)
        soup = BeautifulSoup(response.text, features="html.parser")
        print(f"Код: {soup.body.text.strip()}")
        break