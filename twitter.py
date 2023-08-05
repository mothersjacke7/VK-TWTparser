import time
import tweepy
import datetime
import PySimpleGUI as sg
from colorama import Fore
import json as js
import os

print('\033c')

# Получение текущей даты и времени
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H-%M-%S")
sg.theme('Default 1')
# Создание пути к папке с текущей датой
folder_path = os.path.join(".", "data", date)

# Создание папки с текущей датой, если она не существует
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Создание папки с текущим числом внутри папки с текущей датой
current_day_folder = os.path.join(folder_path, current_time)
os.makedirs(current_day_folder)

layout = [
    [sg.Text('Данная программа сравнивает подписчиков двух пользователей Twitter, выводит их в файлы и показывает статистику.')],
    [sg.Text('Имя первого пользователя (без @):'), sg.InputText(key='first_username')],
    [sg.Text('Имя второго пользователя (без @):'), sg.InputText(key='second_username')],
    [sg.Button('Start'), sg.Button('Exit')]
]
window = sg.Window('[Twitter] Поиск общих пользователей.', layout)
while True:
    event, values = window.read()
    if event == 'Start':
        first_screen_name = values['first_username']
        second_screen_name = values['second_username']
        settings = open('config.json') 
        config = js.load(settings)
        consumer_key1 = config['consumer_key']
        consumer_secret1 = config['consumer_secret']
        access_token1 = config['access_token']
        access_token_secret1 = config['access_token_secret']
        auth = tweepy.OAuth1UserHandler(
            consumer_key=consumer_key1,
            consumer_secret=consumer_secret1,
            access_token=access_token1,
            access_token_secret=access_token_secret1
        )
        api = tweepy.API(auth, wait_on_rate_limit=True)

        # Путь к папке с текущим числом
        current_day_folder = os.path.join(folder_path, current_time)

        f = open(os.path.join(current_day_folder, 'first_follower_ids.txt'), 'w')
        f.close()
        f = open(os.path.join(current_day_folder, 'second_follower_ids.txt'), 'w')
        f.close()
        first_follower_ids = []
        for page in tweepy.Cursor(api.get_follower_ids, screen_name=first_screen_name, count=5000).pages():
            first_follower_ids.extend(page)
            f = open(os.path.join(current_day_folder, 'first_follower_ids.txt'), 'a')
            for i in page:
                f.write(str(i) + '\n')
            f.close()
            dateTimeObj = datetime.datetime.now()
            timestampStr = dateTimeObj.strftime("%H:%M:%S")
            for j in range(10):
                print(f'{Fore.GREEN}[{timestampStr}] [Успех!] Ждем {10 - j} секунд и ищу дальше.'
                    f'Записали данные в файл first_follower_ids.txt {len(first_follower_ids)} шт подписчиков для пользователя {first_screen_name}{Fore.RESET}',
                    end='\r')
                time.sleep(1)

        second_follower_ids = []
        for page in tweepy.Cursor(api.get_follower_ids, screen_name=second_screen_name, count=5000).pages():
            second_follower_ids.extend(page)
            f = open(os.path.join(current_day_folder, 'second_follower_ids.txt'), 'a')
            for i in page:
                f.write(str(i) + '\n')
            f.close()
            dateTimeObj = datetime.datetime.now()
            timestampStr = dateTimeObj.strftime("%H:%M:%S")
            for j in range(10):
                print(f'{Fore.GREEN}[{timestampStr}] [Успех!] Ждем {10 - j} секунд и ищу дальше. '
                    f'Записали данные в файл second_follower_ids.txt {len(second_follower_ids)} шт подписчиков для пользователя {second_screen_name}{Fore.RESET}',
                    end='\r')
                time.sleep(1)

        common_follower_ids = set(first_follower_ids) & set(second_follower_ids)
        unique_first_follower_ids = set(first_follower_ids) - set(second_follower_ids)
        unique_second_follower_ids = set(second_follower_ids) - set(first_follower_ids)

        f = open(os.path.join(current_day_folder, 'common_follower_ids.txt'), 'w')
        for i in common_follower_ids:
            f.write(str(i) + '\n')
        f.close()

        f = open(os.path.join(current_day_folder, 'unique_first_follower_ids.txt'), 'w')
        for i in unique_first_follower_ids:
            f.write(str(i) + '\n')
        f.close()

        f = open(os.path.join(current_day_folder, 'unique_second_follower_ids.txt'), 'w')
        for i in unique_second_follower_ids:
            f.write(str(i) + '\n')
        f.close()
        sg.popup(f'{len(common_follower_ids)} общих подписчиков между {first_screen_name} и {second_screen_name}\n'
         f'{len(unique_first_follower_ids)} Уникальны для {first_screen_name}\n'
         f'{len(unique_second_follower_ids)} Уникальны {second_screen_name}\n'
         f'Совпадение подписчиков пользователя {first_screen_name} - {round(len(common_follower_ids) / len(first_follower_ids) * 100, 2)}%\n'
         f'Совпадение подписчиков пользователя {second_screen_name} - {round(len(common_follower_ids) / len(second_follower_ids) * 100, 2)}%\n'
         f'ID общих подписчиков записаны в файл common_follower_ids.txt')
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()
print('\033c')