from dataclasses import dataclass, field
from mysql.connector.pooling import MySQLConnectionPool
from functools import cache


@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    pool_size: int = 1
    database: str = None
    autocommit: bool = field(init=True)
    # autocommit: bool = True  # 强制行为

    @cache
    def pool(self) -> MySQLConnectionPool:
        return MySQLConnectionPool(**self.__dict__)
