# VK group info
import requests
import config

# ---------------------
url = 'https://api.vk.com/method/'
group_name = 'gk_yoga'
access_token = config.TOKEN


# ------------------------------------------
# Работа с группой
# ------------------------------------------
# Получение списка пользователей группы
# Получение количества пользователей в группе


def m_count(name):
    response = requests.get(url + 'groups.getMembers', params={
        'group_id': name,
        'v': 5.124,
        'access_token': access_token
    })
    return response.json()['response']['count']


# Количество пользователей в группе

# Получение списка пользователей группы
def memb(name, members_count):
    result = []
    for i in range(members_count // 1000 + 1):
        response = requests.get(url + 'groups.getMembers', params={
            'lang': 0,
            'group_id': name,  # Наименование группы
            'v': 5.124,  # Версия API
            'access_token': access_token,  # Токен
            'offset': i * 1000,  # Смещение
            'count': 1000  # Количество пользователей
        })
        result.extend(response.json()['response']['items'])
    return result



# ------------------------------------------
# Работа с членами группы
# ------------------------------------------
# Пользователи с открытыми профилями
# Перевод телефона в формат

def format_phone(phone):
    new_phone = ''
    for char in phone.strip():
        if char in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            new_phone += char
    if len(new_phone) != 11:
        return ''
    if new_phone[0] == '8' or new_phone[0] == '7':
        new_phone = '+7' + new_phone[1:]
    if new_phone[2] == '8':
        return ''
    return new_phone


# ----------
def open_membs(members):
    open_members = []
    for i in range(len(members) // 100 + 1):
        response = requests.get(url + 'users.get', params={
            'lang': 0,
            'user_ids': ','.join(list(map(str, members[i * 100:(i + 1) * 100]))),  # Наименование группы
            'v': 5.124,  # Версия API
            'access_token': access_token,  # Токен
            'fields': 'city, bdate, sex, contacts'
        })
        for user in response.json()['response']:
            try:
                if not user['is_closed']:
                    user['mobile_phone'] = format_phone(user['mobile_phone'])
                    user['home_phone'] = format_phone(user['home_phone'])
                    open_members.append(user)
            except:
                pass

    # Пользователи с открытым профилем
    # print(len(open_members))
# ------------------------------------------
# Пользователи с номерами телефонов
def phone_memb(open_members):
    phone_members = []

    for user in open_members:
        try:
            if user['mobile_phone'] != '' or user['home_phone'] != '':
                phone_members.append(user)
        except:
            pass
    # phone_members.sort(key=lambda x: (x['sex'], x['first_name']))

    # print(len(phone_members)) # пользователи указавшие номер телефона

# ОСНОВНАЯ ФУНКЦИЯ
# -------------------------------------------------------
def get_info(group_name):
    result = {'name': group_name}

    members_count = m_count(group_name)
    result['members_count'] = members_count

    members = memb(group_name, members_count)  # Список пользователей группы
    # TEMP
    # print(members_count)  # Количество пользователей в группе
    return result
