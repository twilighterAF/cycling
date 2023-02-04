from typing import Iterable, Callable

from loguru import logger
from playhouse.postgres_ext import *

from cycle_bot.config import SQL_USER, SQL_PASSWORD, HOST
from cycle_bot.exceptions import DatabaseError


try:
    DATABASE = PostgresqlExtDatabase('cycles', user=SQL_USER, password=SQL_PASSWORD,
                                     host=HOST)

except Exception as e:
    raise DatabaseError(f'Cannot connect to postgres') from e


class BaseModel(Model):
    class Meta:
        database = DATABASE
        order_by = 'users'


class User(BaseModel):
    users = IntegerField(unique=True, index=True, primary_key=True)
    cycles_started = BooleanField()


class Cycle(BaseModel):
    users = ForeignKeyField(User, unique=True, on_delete='CASCADE', backref='cycles')
    cycles = BinaryJSONField()


class TablesHandler:

    @staticmethod
    def context_atomic(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            with DATABASE.atomic():
                result = func(*args, **kwargs)
            return result
        return wrapper

    @classmethod
    @context_atomic
    def sql_insert(cls, user: int, cycles_started: bool, cycles: json):
        User.insert(users=user, cycles_started=cycles_started) \
            .on_conflict(conflict_target=User.users, preserve=User.users,
                         update={User.cycles_started: cycles_started}).execute()

        Cycle.insert(users=user, cycles=cycles) \
            .on_conflict(conflict_target=Cycle.users, preserve=Cycle.users,
                         update={Cycle.cycles: cycles}).execute()

    @classmethod
    @context_atomic
    def sql_get_user(cls, user: int) -> Iterable:
        return User.select(User.users, User.cycles_started, Cycle.cycles).join(Cycle, on=(Cycle.users == User.users)) \
            .where(User.users == user).dicts().execute()

    @classmethod
    @context_atomic
    def sql_get_active_cycles(cls) -> Iterable:
        return User.select(User.users, Cycle.cycles).join(Cycle, on=(Cycle.users == User.users)) \
            .where(User.cycles_started == True).dicts().execute()

    @classmethod
    @context_atomic
    def sql_delete_all_users(cls):
        User.delete().execute()
