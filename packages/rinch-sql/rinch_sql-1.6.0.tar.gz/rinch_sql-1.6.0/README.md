# Introduction

a simple orm in python based on [mysql,dataclass].



# Install

```
pip install rinch-sql
```



# Use

## dict

- table

  - \_\_init\_\_.py
  - user.py
  - table2.py

- task.py

  

## user.py

```python
import datetime
from dataclasses import dataclass


@dataclass
class User:
    field_list_unique = ["name"]  # must, can be []

    name: str
    age: int

    id: int = None  # must
    create_time: datetime = None
    update_time: datetime = None

```

## \_\_init\_\_.py

```python
from rinch_sql import Mysql

# please use every key with current name. dont use it autocommit(always True).
MYSQL_SERVER_DATABASE = {
    "host": "",
    "port": 3306,
    "user": "",
    "password": "",
    "database": "",
    "pool_size": 32,
}

from .user import User

# it will create pool immediately
mysql_user = Mysql(MYSQL_SERVER_DATABASE, User)


# or creat it when use
def mysql_user_():
    return Mysql(MYSQL_SERVER_DATABASE, User)

```

## task.py

```python
from rinch_sql import Sql, SqlStatic
from table import mysql_user, User

# select all
user_list = mysql_user.select("")


# select with where
user_list = mysql_user.select("id = 1")

# select with complex sql
sql = "SELECT id,t1.name,age from user as t1 right join tb_mail as t2 on t1.name=t2.name group by t1.name"
values = ["id", "name", "age"]  # "id,name,age".split(",")
user_record_list = mysql_user.execute(sql)
user_list = [mysql_user._values_2_obj(i, values) for i in user_record_list]

# or you can use Sql or SqlStatic driect
sql_update = SqlStatic.update("user", ["name", "age"])
user = User(id=2)
mysql_user.execute(sql_update, ["name_new", 100])

```



# Advice

when you have any advice, please issue in https://github.com/rinch-wu/rinch_sql