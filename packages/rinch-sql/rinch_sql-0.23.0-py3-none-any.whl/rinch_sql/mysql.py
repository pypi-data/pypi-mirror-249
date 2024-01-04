from typing import Type, TypeVar, Generic

import time

import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector.connection import MySQLConnection

from .sql import Sql

T = TypeVar("T")


class Mysql(Generic[T]):
    cls: Type[T]
    sql: Sql
    pool: MySQLConnectionPool

    def __init__(self, mysql_config_pool: dict[str], cls: Type[T]):
        mysql_config_pool = {**mysql_config_pool, "autocommit": True}

        mysql_config_pool_key_min = {
            "host",
            "port",
            "user",
            "password",
            "database",
            "pool_size",
            "autocommit",
        }
        assert mysql_config_pool.keys() >= mysql_config_pool_key_min, mysql_config_pool

        self.cls = cls
        self.sql = Sql(cls)
        self.pool: MySQLConnectionPool = MySQLConnectionPool(**mysql_config_pool)

    def conn(self) -> MySQLConnection:
        total: int = 0
        sleep_time_max = 5 * 60  # 5min
        while True:
            try:
                return self.pool.get_connection()
            except mysql.connector.errors.PoolError:
                sleep_time = min(2**total, sleep_time_max)
                time.sleep(sleep_time)
                total += 1

    def create(self) -> None:
        sql = self.sql.create()
        self.execute(sql)

    def select(self, _where: str) -> list[T]:
        sql, fields = self.sql.select(_where)
        data_list = self.execute(sql)
        obj_list = [self._values_2_obj(fields, i) for i in data_list]
        return obj_list

    def insert(self, obj_list: list[T]) -> None:
        sql, fields = self.sql.insert()
        values_list = [self._obj_2_values(obj, fields) for obj in obj_list]
        self.executemany(sql, values_list)

    def insert_with_duplicate(self, obj_list: list[T], field_list: list[str] = None) -> None:
        field_list = field_list or self.sql.field_list_common

        sql, fields = self.sql.insert_with_duplicate(field_list)
        values_list = [self._obj_2_values(obj, fields) for obj in obj_list]
        self.executemany(sql, values_list)

    def update_many(self, obj: T, field_list: list[str]) -> None:
        sql, fields = self.sql.update(field_list)
        values = self._obj_2_values(obj, fields)
        self.execute(sql, values + [obj.id])

    def update_one_key_with_value(self, obj: T, key: str) -> None:
        self.update_many(obj, [key])

    # def check_field_str(self, data_dict: dict[str]) -> None:
    #     if not hasattr(self, "table_desc"):
    #         self.table_desc: dict[str, dict[str, int]] = {}

    #     desc = self.get_desc()
    #     self.modify_column(desc, data_dict)

    # @staticmethod
    # def to_str(data_str_bytes: [str, bytes]) -> str:
    #     if isinstance(data_str_bytes, str):
    #         return data_str_bytes
    #     elif isinstance(data_str_bytes, bytes):
    #         return data_str_bytes.decode()

    # # 获得表中字符类型的长度
    # def get_desc(self) -> dict[str, int]:
    #     table_name = self.sql.table_name
    #     if table_name not in self.table_desc:
    #         sql = self.sql.desc()
    #         data_list = self.execute(sql)
    #         data_list = [(i[0], self.to_str(i[1])) for i in data_list]
    #         desc = {i[0] : int(i[1][8:-1]) for i in data_list if i[1].startswith("varchar(")}
    #         self.table_desc[table_name] = desc
    #     else:
    #         desc = self.table_desc[table_name]

    #     return desc

    # # 修改字符长度（如果需要的话）
    # def modify_column(self, desc: dict[str, int], final_dict: dict[str]) -> None:
    #     for key, value in final_dict.items():
    #         if not isinstance(value, str):
    #             continue
    #         length = len(value)
    #         if desc[key] >= length:
    #             continue

    #         sql = self.sql.alert_modify(key, f"VARCHAR({length})")
    #         self.execute(sql)
    #         desc[key] = length

    def execute(self, sql, values=[]) -> list:
        with self.conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                data_list = cursor.fetchall()
                return data_list

    def executemany(self, sql, values_list):
        with self.conn() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql, values_list)

    def _values_2_obj(self, fields: list[str], values) -> T:
        data_json = {key: value for key, value in zip(fields, values)}
        obj = self.cls(**data_json)
        return obj

    def _obj_2_values(self, obj: T, fields: list[str]) -> list:
        return [obj.__getattribute__(field) for field in fields]
