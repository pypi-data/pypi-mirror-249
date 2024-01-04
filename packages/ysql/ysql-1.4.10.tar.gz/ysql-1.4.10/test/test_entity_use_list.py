# -*- coding:utf-8 -*-
import os
from dataclasses import dataclass

import pytest

from ysql import Dao, MetaDatabase
from ysql.entity import Entity, Constraint as cs


@Entity
@dataclass
class Student:
    name: str
    score: list = cs.ignore


@Dao(Student)
class DaoStudent:
    pass


class Database(MetaDatabase):
    dao = DaoStudent()


def test_entity_use_list():
    db_path = f"db_folder/{os.path.basename(__file__).split('.')[0]}.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = Database(db_path)
    db.connect()
    db.create_tables()


if __name__ == '__main__':
    pytest.main(["-vv",
                 "--capture=no",
                 __file__])
