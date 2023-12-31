import requests
import time

import PySimpleGUI as sg

def main(public, token):
    version = '5.131'
    url = 'https://api.vk.com/method/'
    print("Поиск пользователей, которые были в сети за последнюю неделю")
    date_format = time.time() - 86400


    # получение id паблика
    def getting_id():
        needed_id = requests.get(url + 'groups.getById', params={
            'access_token': token,
            'v': version,
            'group_id': public
        }).json()
        print(needed_id)
        print("Нашел id паблика " + public + " - " + str(needed_id['response'][0]['id']))
        return needed_id['response'][0]['id']
        


    # получение максимального значения параметра offset для нужного паблика
    def getting_offset():
        public_id = getting_id()
        count_followers = requests.get(url + 'groups.getMembers', params={
            'access_token': token,
            'v': version,
            'group_id': public_id,
            'sort': 'id_desc',
            'offset': 0,
            'fields': 'last_seen'
        }).json()['response']['count']
        print("Нашел количество подписчиков паблика " + public + " - " + str(count_followers))
        return count_followers // 1000


    def get_all_followers():
        public_id = getting_id()
        followers_ids = []
        offset = 0
        maximal_offset = getting_offset()
        while offset < maximal_offset:
            response = requests.get(url + 'groups.getMembers', params={
                'access_token': token,
                'v': version,
                'group_id': public_id,
                'sort': 'id_desc',
                'offset': offset,
                'fields': 'last_seen'
            }).json()['response']
            offset += 1
            for el in response['items']:
                try:
                    if el['last_seen']['time'] >= date_format:
                        followers_ids.append(el['id'])
                except Exception as E:
                    continue
        print("Нашел всех пользователей паблика " + public)
        return followers_ids
        

    with open(f'{public}.txt', 'w') as f:
        for el in get_all_followers():
            f.write("%s\n" % el)

def common_idsf(value1, value2, valuet):
    token = valuet
    public1 = value1
    public2 = value2
    public1 = public1[15:]
    public2 = public2[15:]
    main(public1, token)
    time.sleep(1)
    main(public2, token)
    print("Начинаю поиск общих пользователей")
    with open(f'{public1}.txt', 'r') as f:
        ids1 = f.read().splitlines()
    with open(f'{public2}.txt', 'r') as f:
        ids2 = f.read().splitlines()
    common_ids = list(set(ids1) & set(ids2))
    percent1 =  round(len(common_ids) / len(ids1) * 100, 2)
    percent2 =  round(len(common_ids) / len(ids2) * 100, 2)
    with open('common_ids.txt', 'w') as f:
        for el in common_ids:
            f.write("%s\n" % el)
    print(f'Количество общих пользователей: {len(common_ids)}')
    print("Список общих пользователей, которые были в сети за последнюю неделю, записан в файл common_ids.txt")
    return common_ids, percent1, percent2

def gui():
    sg.theme('Default 1')

    layout = [  [sg.Text('Введите Ваш токен доступа VK')],
                [sg.Text('Можно взять тут -> '),sg.InputText('https://vkhost.github.io/', size=(20, 1))],
                [sg.InputText('', key = 'valuet')],
                [sg.Text('Введите ссылку паблика 1')],
                [sg.InputText('', key = 'public1')],
                [sg.Text('Введите ссылку паблика 2')],
                [sg.InputText('', key ='public2')],
                [sg.Button('Ok', key = "Okay"), sg.Button('Cancel')],
                [sg.Text('', key='-TEXT-')],
                [sg.Output(key='-TEXT_response-', expand_x=True, expand_y = True)]]


    window = sg.Window('Поиск общих пользователей', layout, size=(400, 400))

    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            print("Cancel")
            break
        if event == 'Okay':
            common_ids_output, percent1, percent2 = common_idsf(values["public1"], values["public2"], values["valuet"])
            window['-TEXT-'].update(f'Количество общих пользователей: {len(common_ids_output)}\nПроцент пользователей паблика 1: {percent1}%\nПроцент пользователей паблика 2: {percent2}%\nID пользователей смежных групп:')
            window['-TEXT_response-'].update(common_ids_output)
    window.close()

gui()