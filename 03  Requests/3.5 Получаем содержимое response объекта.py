# 3.5 Получаем содержимое response объекта
""""""
from pprint import pprint

"""
Содержимое ответа  response  .json() .text .content
"""
import requests
from pprint import pprint

response = requests.get(url='https://jsonplaceholder.typicode.com/todos/')
pprint(response.json())


response = requests.get(url='https://jsonplaceholder.typicode.com/todos/')
pprint(response.text)

"""
.text и .json() вернут одну и ту же информацию. Но на самом деле это не так. 
какой нам выбрать способ для парсинга? 
Метод .json() мы используем в случае, когда мы знаем, что сайт отдает нам информацию в формате JSON. 
Как найти и получить ссылку, по которой мы могли бы получить данные в этом формате, мы знаем дальше.
 
Атрибут.text мы будем использовать в тех случаях, когда будем парсить HTML при помощи BeautifulSoup

Если мы посмотрим на type() ответа каждого из запросов, 
мы обнаружим, что в случае с .json() мы получаем тип <class 'list'>, 
а в случае с .text мы получаем тип <class 'str'>
"""

import requests

response = requests.get(url='http://httpbin.org/')
print(response.text)  # Выводит Html документ


'''
Атрибут .content  нужен нам для загрузки медиа-файлов, картинок, всех форматов аудио и видео.
'''
import requests

response = requests.get(url='http://httpbin.org/image/jpeg')
print(response.content)
# Если мы выполним этот код без менеджера контекста with, мы увидим длинную байтовую строку:
# b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x02\x00\x1c\x00\x1c\x00\x00\xff\xfe\x005 ........


# Для того, чтобы скачать медиа-файл, используйте менеджер контекста with.
import requests

response = requests.get(url='http://httpbin.org/image/jpeg')
with open('image.jpeg', 'wb') as file:  # флаг 'wb', означает ‘write byte’, т.е., запись байтов
    file.write(response.content)


#
#  *  *  *   Задачи   *  *  *
#

"""
Перейдите на сайт http://parsinger.ru/img_download/index.html
На 1-ной из 160-ти картинок написан секретный код
Напишите код, который поможет вам скачать все картинки
В скачанных картинках найдите вручную секретный код
Вставьте код в поле для ответа
# 6759632
"""

import requests
from tqdm import tqdm  # прогресс бар

for el in tqdm(range(1, 11)):
    url = f"https://parsinger.ru/img_download/img/ready/{el}.png"
    name = f"03  Requests/media/image_{el}.png"
    pic = requests.get(url=url)
    with open(name, 'wb') as file:
        file.write(pic.content)

# 6759632

