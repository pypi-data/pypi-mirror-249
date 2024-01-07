from .mysql import Mysql


class Table:
    db_config: dict[str] = None
    field_list_unique: list[str]

    @classmethod
    def db(cls, db_config: dict[str] = None):
        db_config = db_config or cls.db_config
        db = Mysql(cls, db_config)
        return db
