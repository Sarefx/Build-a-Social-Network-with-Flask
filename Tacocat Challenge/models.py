import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('tacos.db')


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=50)
    #id = AutoField()

    class Meta:
        database = DATABASE
    def get_tacos(self):
        return Taco.select().where(Taco.user == self)

    def get_stream(self):
      return Taco.select().where(Taco.user == self)

    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists")

class Taco(Model):
    protein = CharField(max_length=255)
    shell = CharField(max_length=255)
    cheese = BooleanField(default=True)
    extras = CharField(max_length=255)
    # user = ForeignKeyField(User, backref='tacos')
    user = ForeignKeyField(rel_model=User, related_name='tacos')

    @classmethod
    def create_taco(cls, user, protein, shell, cheese, extras):
        cls.create(
            user=user,
            protein=protein,
            shell=shell,
            cheese=cheese,
            extras=extras)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()