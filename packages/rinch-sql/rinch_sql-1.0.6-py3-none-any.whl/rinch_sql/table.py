from .mysql import Mysql


class Table:
    db_config: dict[str] = None

    @classmethod
    def db(cls, db_config: dict[str] = None):
        db_config = db_config or Table.db_config or cls.db_config
        db = Mysql(db_config, cls)
        return db
