# 3  Requests
# 3.3 Метод requests.get()
""""""

import requests

response = requests.get(url='http://httpbin.org/')
print(type(response))
# # <class 'requests.models.Response'>
"""
переменная  response стала экземпляром класса requests, и в нее передали атрибут = url.
Мы можем    передавать этому классу и другие аргументы:

url         Передает ссылку - цель, куда будет отправлен запрос. (Обязательный)
params      Cловарь или байты, которые будут отправлены в строке запроса. (Необязательный)
headers     Cловарь HTTP-заголовков, отправляемых с запросом.  (Необязательный)
cookies     Объект Dict или CookieJar для отправки с запросом.  (Необязательный)
auth        AuthObject для включения базовой аутентификации HTTP.  (Необязательный)
timeout     Число с плавающей запятой, описывающее тайм-аут запроса.(Необязательный)
allow_redirects     Логическое значение. Установите значение True, если разрешено перенаправление. (Необязательный)
proxies     Протокол сопоставления словаря с URL-адресом прокси.  (Необязательный)
stream      Удерживает соединение открытым, пока не получен весь Response.content (Необязательный)
"""


""""""
# Заголовки headers=
"""
Заголовки отправляются вместе с запросом и возвращаются с ответом. 
Они нужны, чтобы клиент и сервер понимали, 
как интерпретировать данные, отправляемые и получаемые в запросе и ответе.
"""

# пример отправляемого нашим скриптом заголовка.
response = requests.get(url='http://httpbin.org/user-agent')
print(response.text)
# {
#   "user-agent": "python-requests/2.31.0"
# }


"""
Для того, чтобы замаскировать свой запрос под запрос браузера, 
будем использовать .get() запрос с именованным атрибутом и передадим в него словарь headers.
"""
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}

response = requests.get(url='http://httpbin.org/user-agent', headers=headers)
print(response.text)
# {
#   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
# }


import time
from random import choice
import requests

url = 'http://httpbin.org/user-agent'

with open('user_agent.txt') as file:
    lines = file.read().split('\n')

for line in lines:
    user_agent = {'user-agent': choice(lines)}
    response = requests.get(url=url, headers=user_agent)
    print(response.text)
    time.sleep(3)  # когда сервер банит за спам-запросы

"""
Этот код последовательно подставляет user-agent из файла и делает запрос на наш url. 
Обратите внимание, что в этом примере использовался модуль random 
и его метод choice для случайного выбора user_agent из файла.
"""


""""""
# Библиотека fake_useragent
"""
импорт 
from fake_useragent import UserAgent
или
import fake_useragent
Экземпляр класса создаётся двумя способами. Оба эти способа будут работать одинаково.
ua = fake_useragent.UserAgent() или ua = UserAgent()  во втором примере мы используем укороченную запись.
"""
from fake_useragent import UserAgent
import requests

url = 'http://httpbin.org/user-agent'
ua = UserAgent()

for x in range(10):
    fake_ua = {'user-agent': ua.random}
    response = requests.get(url=url, headers=fake_ua)
    print(response.text)


""""""
# Прокси proxies=

import re
from random import choice
import requests

# url = 'http://httpbin.org/ip'
#
# with open('03 Requests/proxy.txt') as file:
#     proxy_file = file.read().split('\n')
#     for _ in range(1000):
#         try:
#             ip = choice(proxy_file).strip()
#             proxy = {
#                 'http': f'http://{ip}',
#                 'https': f'https://{ip}'
#             }
#             response = requests.get(url=url, proxies=proxy)
#             print(response.json(), 'Success connection')
#         except Exception as _ex:
#             continue


url = 'http://httpbin.org/ip'
proxies = []
amount_of_proxies = 10

with open('03 Requests/proxy.txt') as file:
    proxy_file = file.read().split('\n')
    while len(proxies) < amount_of_proxies and len(proxy_file) > 0:
        try:
            ip = proxy_file.pop(proxy_file.index(choice(proxy_file))).strip()
            if not re.fullmatch(r'([0-2]?\d{2}\.){3}([0-2]?\d{2})\:\d+', ip):
                continue
            proxy = {
                'http': f'http://{ip}',
                'https': f'https://{ip}'
            }
            response = requests.get(url=url, proxies=proxy, timeout=30)
            if response.status_code != 200:
                print(f'{ip}: response {response.status_code}. Bad connection')
            else:
                print(response.json(), 'Success connection')
                proxies.append(ip)
        except Exception as _ex:
            print(f'{ip}: {_ex}')

print(proxies)


""""""
# Таймаут timeout=
"""
Когда мы делаем запрос к сайту, наш парсер должен дождаться ответа от сервера, 
прежде чем двигаться дальше. Если ваши запросы используют прокси, 
то время ожидания каждого запроса может существенно возрасти. 
По умолчанию requests будет ждать ответа неопределенное время, 
поэтому вы почти всегда должны указывать продолжительность тайм-аута. 
"""

import requests
import time

url = 'http://httpbin.org/get'

proxies = {
    'http': 'http://200.12.55.90:80',
    'https': 'http://200.12.55.90:80'
}
start = time.perf_counter()
try:
    requests.get(url=url, proxies=proxies)
except Exception as _ex:
    print(time.perf_counter() - start)
# # 21.045187100000476

"""
Время ожидания ответа на запрос - 21 секунда.
Чтобы сократить время этого ожидания до 1 секунды, напишем тот же код, только с атрибутом timeout=1 .
А если timeout=None, будем ждать ответ вечно.
"""

import requests
import time

url = 'http://httpbin.org/get'

proxies = {
    'http': 'http://200.12.55.90:80',
    'https': 'http://200.12.55.90:80'
}
start = time.perf_counter()
try:
    requests.get(url=url, proxies=proxies, timeout=1)
except Exception as _ex:
    print(_ex)
    print(time.perf_counter()- start)
# 1.0147352999993018

"""
Во втором примере метод .get() ожидает ответ от сервера ровно 1 секунду, 
затем печатает исключение с таймаутом, а затем и время выполнения скрипта, 
где мы видим, что на всё потребовалось 1.0147352999993018 сек.
"""


""""""
# Передача параметров в URL params=

"""
Часто вам может понадобиться отправить какие-то данные в строке запроса URL. 
Если вы настраиваете URL вручную, эти данные будут представлены в нем в виде пар ключ/значение после знака вопроса. 
Например, httpbin.org/get?key=val. 
Requests позволяет передать эти аргументы в качестве словаря, используя аргумент params=. 
Если вы хотите передать key1=value1 и key2=value2 ресурсу httpbin.org/get, вы должны использовать следующий код:
"""

import requests

param = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('https://httpbin.org/get', params=param)
print(r.url)
# https://httpbin.org/get?key1=value1&key2=value2


""""""
# Загружаем видео при помощи requests
"""
Когда возникает потребность скачать видео с сайта, мы прибегаем к помощи библиотеки requests, 
она делает эту задачу максимально простой.
У метода .get()  есть подходящий параметр для этих целей  stream=True
stream=True - Позволяет удерживать соединение  пока мы не получили весь требуемый контент. 
Этот параметр используется при скачивании тяжеловесных файлов
"""
import requests
url = "https://parsinger.ru/video_downloads/videoplayback.mp4"

response = requests.get(url=url, stream=True)
with open('file.mp4', 'wb') as file:
    file.write(response.content)


"""
Если файл очень большой,  или вы не хотите ждать пока файл скачает полностью , 
то рекомендуется использовать .iter_content() , это метод, который позволяет совершать итерацию по response.content.  
Для .iter_content() мы должны определить размер скачиваемой части файла. 
Параметром chunk_size=1000000 где цифра, это размер в байтах.
"""
import requests
url = "https://parsinger.ru/video_downloads/videoplayback.mp4"
response = requests.get(url=url, stream=True)
with open('file.mp4', 'wb') as video:
    for piece in response.iter_content(chunk_size=10000):
        video.write(piece)

