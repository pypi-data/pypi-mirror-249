from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    pool_size: int = 1
    database: str = ""
    # autocommit: bool = True  # 强制行为
