#Дипломный проект_ чат-бот “VKinder”

from random import randrange
import vk_api
import datetime
from datetime import date
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from collections import OrderedDict

from datetime import date, time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Токен для авторизации как сообщество
token = 'vk1.a.eZACjTMg5Byksi-0Jr5iVvTXA04kzx15PRJR_4c0s3uQsnNyHpBeGv6mYfb6YpIUB0FHF2RlTXjg50xlDfIxFi10kO8-oDP4hPtwXnokrxE9BXBKoHfi6micFrTnohE89oCJBw_ZPtSKQyd6tJ-cLJyaLr_tWiNp4nUzy4Iu5HtrOzba5ix8EgKZliFHrVHB'
# Токен для авторизации как пользователь
token2 = 'vk1.a.pk0BpDFpKlYzbeereX8uOoBajTFCGGjTupcRgFeqiuMjkoxjRb_PqDN8DFAx_Pn0-1gCmLsWUO2gL9qjdWvDo2uqsG5hdznsxHvC5whCYdlhs5fZsIauiwzLwhVXEMMNJUuLK-89rATKAcvUiAr3btdDFAIcHKEwO8igZlJ809WW7lOBmGgCDTR8CHUMHwkp'

vk_session = vk_api.VkApi(token=token)
vk_session2 = vk_api.VkApi(token=token2)
longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()
api = vk_session2.get_api()


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

# Функция для расчета возраста пользователя.
def birthday(user_id):
    user = user_data_from_id(user_id)
    if 'bdate' in user[0]:
        a = user[0]['bdate']
        if a != '':
            a = a.split('.')
            days_in_year = 365.2425
            age = int((date.today() - (datetime.date(int(a[2]), int(a[1]), int(a[0])))).days / days_in_year)
    else:
        age = ''
    return age

# Функция для общения с пользователем. Уточнение недостающих данных пользователя.
def ask_user():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request.split()[0] == "возраст":
                    new_age = request.split()[1]
                    if new_age.isnumeric() == True:
                        return new_age
                    else:
                        write_msg(event.user_id, f"не понимаю твой ответ, укажи возраст так:  возраст 30")
                elif request.upper() == "ВСЕХ":
                    CITY = ''
                    return CITY
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
                elif request.upper() == "м":
                    SEX = 1
                    return SEX
                elif request.upper() == "ж":
                    SEX = 2
                    return SEX
                elif request.upper() == "л":
                    SEX = 0
                    return SEX
                else:
                    write_msg(event.user_id, f"сорри.. не понимаю твой ответ")

# Функция для работы с БД
def send_data_to_bd(user, list_data, allusers_photostock, command):
    import sqlalchemy as sq

    Base = declarative_base()
    db = "postgresql://postgres:991073@localhost:5432/postgres"
    engine = sq.create_engine(db, pool_pre_ping=True)

    Session = sessionmaker(bind=engine)
    connection = engine.connect()

    cc = command
    class User(Base):
        __tablename__ = "user"
        id = sq.Column(sq.Integer, primary_key=True)
        user_name = sq.Column(sq.String, nullable=True, unique=False)
        user_vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
        couples = relationship("Couple", secondary="user_to_couple")

    user_to_couple = sq.Table(
        "user_to_couple", Base.metadata,
        sq.Column("user_id", sq.Integer, sq.ForeignKey("user.id")),
        sq.Column("couple_id", sq.Integer, sq.ForeignKey("couple.id")),
        sq.Column("status", sq.Boolean),
    )

    class Couple(Base):
        __tablename__ = "couple"
        id = sq.Column(sq.Integer, primary_key=True)
        couple_name = sq.Column(sq.String, nullable=True, unique=False)
        couple_VK_id = sq.Column(sq.Integer, nullable=False, unique=True)
        users = relationship("User", secondary="user_to_couple")
        photos = relationship("Photo", backref="couple")

    class Photo(Base):
        __tablename__ = "photo"
        id = sq.Column(sq.Integer, primary_key=True)
        photo_uniquecode = sq.Column(sq.String, nullable=False, unique=True)
        photo_VK_id = sq.Column(sq.String, nullable=False, unique=False)
        id_couple = sq.Column(sq.Integer, sq.ForeignKey("couple.id"))

    if __name__ =="__main__":

        with Session() as session:
          oneuser_photostock = {}

          if cc == "save":         # сохранение данных в БД
             Base.metadata.create_all(engine)
             ud = user
             list_data_bd = list_data
             couples_photo_bd = allusers_photostock
             user_id = ud[0]['id']

             user = session.query(User).filter(User.user_vk_id == user_id).scalar()
             if not user:
                 user = User(user_name=ud[0]['first_name'], user_vk_id=ud[0]['id'], )
                 session.add(user)

             photo_list = []
             for c, ph in couples_photo_bd.items():
                 couple_id = c
                 couple = session.query(Couple).filter(Couple.couple_VK_id == couple_id).scalar()
                 if not couple:
                     couple = Couple(couple_VK_id=couple_id)
                     session.add(couple)
                 user.couples.append(couple)
                 for photo in ph:
                     photoanduser = (str(photo) + str(couple_id))
                     photo_1 = session.query(Photo).filter(Photo.photo_uniquecode == photoanduser).scalar()
                     if not photo_1:
                         photo_1 = Photo(photo_uniquecode=photoanduser, photo_VK_id=photo, )
                         session.add(photo_1)
                     photo_1.couple = couple
                     photo_list.append(photo_1)
                 session.add_all(photo_list)

             session.commit()

          elif command == "find":   # поиск пары в БД
                   ud = user
                   find_couple = session.query(user_to_couple, User, Couple).join(User, Couple).filter(User.user_vk_id == ud[0]['id']).all()
                   for fc in find_couple:
                       if fc.status == None:
                           find_photo = session.query(Photo).filter(Photo.id_couple == fc.Couple.id).all()
                           couple_photo = []
                           for photo in find_photo:
                               couple_photo.append(photo.photo_VK_id)
                           oneuser_photostock[fc.Couple.couple_VK_id] = couple_photo

                           f_couple = user_to_couple.update().filter(user_to_couple.c.user_id==fc.user_id, user_to_couple.c.couple_id==fc.couple_id).values(user_id=fc.user_id, couple_id=fc.couple_id, status=True)
                           conn = engine.connect()
                           result = conn.execute(f_couple)
                           break

                   if oneuser_photostock == {}:
                       oneuser_photostock['пары закончились'] = ''
                       command = "save"

                   session.commit()

          return oneuser_photostock

# Класс для поиска пар
class Couple:
    def find_couple(user_id):
        allusers_photostock = {}
        user = user_data_from_id(user_id)
        age = birthday(user_id)
        bdate = ''

        if 'bdate' not in user[0]:
            bdate = 'False'
            write_msg(event.user_id, "У тебя в анкете не указан возраст. Напиши возраст для пары, которую ты ищешь в формате: возраст 30")
            age = ask_user()
        AGE_FROM = age
        AGE_TO = age

        if user[0]['sex'] == '':
            write_msg(event.user_id, "Укажи какого пола люди тебя интересуют: \nж — женщина,\nм — мужчина,\nл — любой.")
            SEX = ask_user()
        else:
            user_sex = user[0]['sex']
            if user_sex == 1:
                SEX = 2
            elif user_sex == 2:
                SEX = 1

        if user[0]['relation'] == '':
            write_msg(event.user_id, "Укажи семейный статус: \n1 — не женат(не замужем),\n2 — встречается,\n3 — помолвлен(-а),\n4 — женат(замужем),\n5 — всё сложно,\n6 — в активном поиске,\n7 — влюблен(-а),\n8 — в гражданском браке.")
            STATUS = ask_user()
        else:
            STATUS = user[0]['relation']

        if 'city' not in user[0]:
            write_msg(event.user_id, "Укажи у себя в настройках анкеты город, чтобы я могла найти людей рядом с тобой. Показать пользователей из разных городов? напиши ВСЕХ если продолжить")
            CITY = ask_user()
        else:
            CITY = user[0]['city']['id']

        rs = api.users.search(age_from=AGE_FROM, age_to=AGE_TO, city=CITY, sex = SEX, status = STATUS, count=5, has_photo=1)

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
        bd = send_data_to_bd(user, list_data, allusers_photostock, command)            # записать найденные пары в БД
        return allusers_photostock

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
                user_data_from_id(user_id)
                photostock = Couple.find_couple(event.user_id)
                if (len(photostock) != 0):
                    write_msg(event.user_id, "Я нашла для тебя интересные пары!) Показать? Напиши ДА чтобы продолжить")

            elif request.upper() == "ДА":
                command = "find"
                list_data = []
                allusers_photostock = {}
                photostock_one = send_data_to_bd(user, list_data, allusers_photostock, command)
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
