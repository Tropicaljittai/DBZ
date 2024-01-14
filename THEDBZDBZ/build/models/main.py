from .auth import Auth
from .database import Database

class Model:
    def __init__(self):
        self.database = Database('data.db')
        self.database.create_table()
        self.auth = Auth(self)