# -*- coding:utf-8 -*-
import pytest


def test_create_tables(init_db):
    """建库"""
    db = init_db
    db.create_tables()


def test_create_with_comment(init_db):
    """注释功能"""
    db = init_db
    db.dao_student_info._create_table()


if __name__ == '__main__':
    pytest.main(["-v", __file__])
