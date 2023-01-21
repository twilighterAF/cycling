
class DatabaseError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'DatabaseError - {self.message}'
        else:
            return 'Database connection error'


class TablesError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'TablesError - {self.message}'
        else:
            return 'Cant connect to tables'
