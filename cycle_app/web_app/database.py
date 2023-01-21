from playhouse.postgres_ext import *

from .exceptions import TablesError

database = PostgresqlExtDatabase('cycles', user='postgres', password='1111', host='localhost')


class BaseModel(Model):
    class Meta:
        database = database
        order_by = 'users'


class User(BaseModel):
    users = IntegerField(unique=True, index=True, primary_key=True)
    cycles_started = BooleanField()


class Cycle(BaseModel):
    users = ForeignKeyField(User, unique=True, on_delete='CASCADE', backref='cycles')
    cycles = BinaryJSONField()


class TablesHandler:

    def __init__(self, db: PostgresqlExtDatabase, **kwargs):
        self._tables = kwargs['tables'] if kwargs['tables'] else None
        logger.info(f'{self._tables}')
        self.user_table = User()
        self.cycle_table = Cycle()
        self.database = db

        if not self._tables:
            raise TablesError('no tables were connected')

    def create_tables(self):
        with database:
            database.create_tables([table for table in self._tables])

    def delete_tables(self):
        with database:
            database.drop_tables([table for table in self._tables])

    def insert(self, user: int, cycles_started: bool, cycles: json):
        self.user_table.insert(users=user, cycles_started=cycles_started) \
            .on_conflict(conflict_target=User.users, preserve=User.users,
                         update={User.cycles_started: cycles_started}).execute()

        self.cycle_table.insert(users=user, cycles=cycles) \
            .on_conflict(conflict_target=Cycle.users, preserve=Cycle.users,
                         update={Cycle.cycles: cycles}).execute()

    def get_user(self, user: int) -> Model:
        return self.user_table.get(users=user)

    def get_active_cycles(self) -> Model:
        return self.user_table.select(User.users, Cycle.cycles).join(Cycle, on=(Cycle.users == User.users)) \
            .where(User.cycles_started == True).dicts().execute()

    def get_all_users(self) -> Model:
        return self.user_table.select()


table_handler = TablesHandler(database, tables=(User, Cycle))
