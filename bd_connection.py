# Функция для работы с БД
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
db = "postgresql://postgres:991073@localhost:5432/postgres"
engine = sq.create_engine(db, pool_pre_ping=True)

Session = sessionmaker(bind=engine)
connection = engine.connect()


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

Base.metadata.create_all(engine)


def send_data_to_bd(user, list_data, allusers_photostock, command):
        cc = command
        with Session() as session:
          oneuser_photostock = {}

          if cc == "save":         # сохранение данных в БД

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



