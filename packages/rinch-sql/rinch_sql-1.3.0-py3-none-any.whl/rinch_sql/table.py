from functools import cache

from .mysql import Mysql
from .db_config import DbConfig


class Table:
    db_config: DbConfig = None
    field_list_unique: list[str]

    @classmethod
    @cache
    def db(cls, db_config: DbConfig = None):
        db_config = db_config or cls.db_config
        db = Mysql(cls, db_config)
        return db
