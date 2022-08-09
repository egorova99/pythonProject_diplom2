# Класс для поиска пар

import vk_api
import datetime
from datetime import date
from collections import OrderedDict

import bd_connection

# Токен для авторизации как пользователь
token2 = '........'                     # Необходимо проставить токен
vk_session2 = vk_api.VkApi(token=token2)
api = vk_session2.get_api()

class Couple:
    def find_couple(user, answer):
        allusers_photostock = {}
        bdate = ''
        ask = {}

        if 'city' not in user[0]:
            if answer == 'всех':
                user[0]['city'] = 'всех'
                CITY = ''
                answer = ''
            else:
                ask['ask'] = "city"
                return ask
        elif user[0]['city'] == 'всех':
            CITY = ''
        else:
            CITY = user[0]['city']['id']

        if 'bdate' not in user[0]:
            if answer.isnumeric() == True:
                user[0]['bdate'] = answer
                age = answer
                answer = ''
            else:
                ask['ask'] = "bdate"
                return ask
        elif user[0]['bdate'].isnumeric() == False:
            age = Couple.birthday(user)
        elif user[0]['bdate'].isnumeric() == True:
            age = user[0]['bdate']
        AGE_FROM = age
        AGE_TO = age

        if user[0]['sex'] == '':
            if answer.isnumeric() == True:
                SEX = answer
                answer = ''
            else:
                ask['ask'] = "sex"
                return ask
        else:
            user_sex = user[0]['sex']
            if user_sex == 1:
                SEX = 2
            elif user_sex == 2:
                SEX = 1

        if user[0]['relation'] == 0:
            if answer == '':
                ask['ask'] = "relation"
                return ask
            else:
                STATUS = answer
        else:
            STATUS = user[0]['relation']


        rs = api.users.search(age_from=AGE_FROM, age_to=AGE_TO, city=CITY, sex = SEX, status = STATUS, has_photo=1)

        list_users = [x for x in rs['items'] if x != True]
        list_data = []
        for lu in list_users:    # Проверяем страницы найденной пары на отсутствие блокировки\скрытости
            try:
                if lu['is_closed'] == False:
                    list_data.append(lu['id'])
            except:
                pass

        for i in list_data:
            photostock = {}
            user_photos = api.photos.get(owner_id=i, album_id='profile', extended=1)
            for l in user_photos['items']:             #цикл для подсчет рейтинга фото
                j = l['id']
                rate = l['likes']['count'] + l['comments']['count']
                if j not in photostock:
                   photostock[j] = rate

            s = (OrderedDict(sorted(photostock.items(), key=lambda t: t[1], reverse=True)))    # выбор 3х популярных фото пользователя
            sorted_fotos = list(s)[0:3]

            if i in allusers_photostock.keys():
               allusers_photostock[i] += sorted_fotos
            else:
               allusers_photostock[i] = sorted_fotos

        command = "save"
        bd = bd_connection.send_data_to_bd(user, list_data, allusers_photostock, command)            # записать найденные пары в БД
        return allusers_photostock

    # Функция для расчета возраста пользователя.
    def birthday(user):
        if 'bdate' in user[0]:
            a = user[0]['bdate']
            if a != '':
                a = a.split('.')
                days_in_year = 365.2425
                age = int((date.today() - (datetime.date(int(a[2]), int(a[1]), int(a[0])))).days / days_in_year)
        else:
            age = ''
        return age


