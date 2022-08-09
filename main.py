#Дипломный проект_ чат-бот “VKinder”

import vk_api
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import bd_connection
import couple_search

# Токен для авторизации как сообщество
token = '......'                        # Необходимо проставить токен

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

# Функция отправки сообщения пользователю по id пользователя ВК
def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })

# Функция отправки сообщения с прикреплением фото пользователю по id пользователя ВК
def write_msg2(user_id, message, photo):
    vk_session.method('messages.send', {"user_id": user_id, "message": message, "attachment": photo, "random_id": 0})

# Функция для получения данные пользователя
def user_data_from_id(user_id):
    user_data = vk.users.get(user_ids=user_id, fields='bdate,city,sex,relation')
    return user_data

def ask_user():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request.upper() == "ВСЕХ":
                    CITY = 'всех'
                    return CITY

                elif request.split()[0] == "возраст":
                    new_age = request.split()[1]
                    if new_age.isnumeric() == True:
                        return new_age
                    else:
                        write_msg(event.user_id, f"не понимаю твой ответ, укажи возраст так:  возраст 30")

                elif request.upper() == "м":
                    SEX = 1
                elif request.upper() == "ж":
                    SEX = 2
                elif request.upper() == "л":
                    SEX = 0
                    return SEX

                elif request.upper() == "1":
                    STATUS = 1
                    return STATUS
                elif request.upper() == "2":
                    STATUS = 2
                    return STATUS
                elif request.upper() == "3":
                    STATUS = 3
                    return STATUS
                elif request.upper() == "4":
                    STATUS = 4
                    return STATUS
                elif request.upper() == "5":
                    STATUS = 5
                    return STATUS
                elif request.upper() == "6":
                    STATUS = 6
                    return STATUS
                elif request.upper() == "7":
                    STATUS = 7
                    return STATUS
                elif request.upper() == "8":
                    STATUS = 8
                    return STATUS

                else:
                    write_msg(event.user_id, f"сорри.. не понимаю твой ответ")

# Функция для общения с пользователем. Основной цикл.
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            u_id = event.user_id
            user = user_data_from_id(u_id)
            user_name = user[0]['first_name']

            if request.upper() == "ПРИВЕТ":
                write_msg(event.user_id, f"Хай, {user_name}")
                write_msg(event.user_id, f"Хочешь найти себе пару? Напиши ХОЧУ ПАРУ чтобы продолжить ")

            elif request.upper()  == "ХОЧУ ПАРУ":
                write_msg(event.user_id, f"Давай поищем. Немного терпения;)")
                user_id = event.user_id
                answer = ''
                user = user_data_from_id(u_id)
                photostock = couple_search.Couple.find_couple(user, answer)

                if 'ask' in photostock:
                    if photostock['ask'] == 'city':
                        write_msg(event.user_id, "Укажи у себя в настройках анкеты город, чтобы я могла найти людей рядом с тобой. Показать пользователей из разных городов? напиши ВСЕХ если продолжить")
                        answer = ask_user()
                        photostock = couple_search.Couple.find_couple(user, answer)

                    if photostock['ask'] == 'bdate':
                        write_msg(user[0]['id'], "У тебя в анкете не указан возраст. Напиши возраст для пары, которую ты ищешь в формате: возраст 30")
                        answer = ask_user()
                        photostock = couple_search.Couple.find_couple(user, answer)

                    if photostock['ask'] == 'relation':
                        write_msg(user[0]['id'], "Укажи семейный статус: \n1 — не женат(не замужем),\n2 — встречается,\n3 — помолвлен(-а),\n4 — женат(замужем),\n5 — всё сложно,\n6 — в активном поиске,\n7 — влюблен(-а),\n8 — в гражданском браке.")
                        answer = ask_user()
                        photostock = couple_search.Couple.find_couple(user, answer)
                if (len(photostock) != 0):
                    write_msg(event.user_id, "Я нашла для тебя интересные пары!) Показать? Напиши ДА чтобы продолжить")

            elif request.upper() == "ДА":
                command = "find"
                list_data = []
                allusers_photostock = {}
                photostock_one = bd_connection.send_data_to_bd(user, list_data, allusers_photostock, command)
                if photostock_one == {'пары закончились': ''}:
                    write_msg(event.user_id,
                              "Аа ты упорный, пересмотрел все пары которые я для тебя нашла, неужели тебе никто не понравился? Чтобы повторить поиск напиши ХОЧУ ПАРУ")
                else:
                    for k, v in photostock_one.items():
                        write_msg(event.user_id, f' Подходящая пара: ссылка - https://vk.com/id{k}')
                        for i in v:
                            photo = f'photo{k}_{i}'
                            write_msg2(event.user_id, f"фото: ", photo)
                        write_msg(event.user_id, "Показать еще? Напиши ДА чтобы продолжить")

            elif request.upper() == "НЕТ":
                write_msg(event.user_id, "Жаль! Тогда до новых встреч(( Если понадоблюсь напиши ПРИВЕТ")
                break

            elif request.upper() == "ПОКА":
                write_msg(event.user_id, "Пока пока!) Если понадоблюсь я здесь")
                break
            else:
                write_msg(event.user_id, "Не поняла твоего ответа(( Повтори, пожалуйста, запрос или можем начать сначала напиши ПРИВЕТ или ХОЧУ ПАРУ")


