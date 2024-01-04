# -*- coding:utf-8 -*-
import time
from dataclasses import asdict

import pytest

from test.model import Student, Score, Database, Student2

# 测试用例
test_cases = [
    ("SELECT column1 FROM table1", True),  # 仅选择一个字段
    ("SELECT column1, column2 FROM table1", False),  # 选择多个字段
    ("SELECT column1, column2, column3 FROM table1", False),  # 选择多个字段
    ("SELECT DISTINCT column1 FROM table1", True),  # 使用 DISTINCT
    ("SELECT column1 FROM table1 WHERE column2 = 42", True),  # 包含 WHERE 子句
    ("SELECT column1 FROM table1 JOIN table2 ON table1.id = table2.id", True),  # 包含 JOIN
    ("SELECT column1 FROM (SELECT column2 FROM table1) AS subquery", True),  # 包含子查询
    ("SELECT * FROM table1", False),  # 选择所有字段
    ("SELECT COUNT(*) FROM table1", False),  # 使用聚合函数
    ("SELECT column1, column2 FROM table1 WHERE column3 = (SELECT MAX(column4) FROM table2)", False),  # 复杂查询
    ("INSERT INTO table1 (column1, column2) VALUES (value1, value2)", False),  # 插入语句
    ("UPDATE table1 SET column1 = value1 WHERE column2 = value2", False),  # 更新语句
    ("DELETE FROM table1 WHERE column1 = value1", False),  # 删除语句
    ("SELECT MIN(column1) FROM table1", False),  # 使用 MIN() 聚合函数
    ("SELECT MAX(column1) FROM table1", False),  # 使用 MAX() 聚合函数
    ("SELECT AVG(column1) FROM table1", False),  # 使用 AVG() 聚合函数
    ("SELECT SUM(column1) FROM table1", False),  # 使用 SUM() 聚合函数
    ("SELECT column1, column2 FROM table1 GROUP BY column1", False),  # 使用 GROUP BY 子句
    ("SELECT column1 FROM table1 HAVING COUNT(*) > 10", False),  # 使用 HAVING 子句
]


def generate_students(start, end):
    return [
        Student(name=f'李华{i}', age=i, phone=123456789,
                weight=50.0, height=100.0 + i, address=f'hit{i}',
                student_id=i)
        for i in range(start, end)
    ]


student_num = 100
students = [
    Student(name=f'李华{i + 1}', age=i + 1, phone=123456789,
            weight=50.0, height=100.0 + i + 1, address=f'hit{i + 1}',
            student_id=i + 1)
    for i in range(0, student_num)
]


@pytest.mark.order(1)
def test_dao_create_table(init_db: Database):
    """创建表"""
    db = init_db
    db.dao_student._create_table()
    db.dao_score._create_table()
    db.dao_student_info._create_table()
    db.commit()


@pytest.mark.order(2)
def test_insert(init_db):
    """插入数据"""
    db = init_db
    for student in students:
        record_id = db.dao_student.insert(entity=student)
        db.commit()

        result = db.dao_student.select_student_by_id(record_id)
        result = result[0]
        assert asdict(result) == asdict(students[result.student_id - 1])


def test_select_all(init_db):
    """查询全部"""
    db = init_db
    results = db.dao_student.select_all()

    for result in results:
        assert asdict(result) == asdict(students[result.student_id - 1])


def test_select_all_with_substitute(init_db):
    """使用表名替代符"""
    db = init_db
    results = db.dao_student.select_all_with_substitute()

    for result in results:
        assert asdict(result) == asdict(students[result.student_id - 1])


def test_select_student_by_id(init_db):
    """具体查询"""
    db = init_db
    select_id = 50
    result = db.dao_student.select_student_by_id(student_id=select_id)
    assert asdict(result[0]) == asdict(students[select_id - 1])


def test_update_name(init_db):
    """更新"""
    db = init_db
    select_id = 50
    new_name = '好家伙'
    db.dao_student.update_name_by_id(name=new_name, student_id=select_id)
    db.commit()
    result = db.dao_student.select_student_by_id(select_id)
    assert result[0].name == new_name


def test_update_name_with_substitute(init_db):
    """使用表名替代符更新"""
    db = init_db
    select_id = 50
    new_name = '好家伙'
    db.dao_student.update_name_by_id_with_substitute(name=new_name, student_id=select_id)
    db.commit()
    result = db.dao_student.select_student_by_id(select_id)
    assert result[0].name == new_name


def test_multiple_table_substitute(init_db: Database):
    """复杂sql中同时使用多个表名替代符"""
    db = init_db
    result = db.dao_student.select_last_student_with_substitute()
    assert result
    assert result[0].student_id == student_num


def test_foreign_key_cascade(init_db):
    """外键"""
    db = init_db
    db.execute("PRAGMA foreign_keys = ON;")
    select_id = 50
    score = Score(150.0, student_id=select_id)
    db.dao_score.insert(score)
    db.dao_student.delete_student_by_id(student_id=select_id)
    db.commit()

    result = db.dao_score.get_score(select_id)
    assert len(result) == 0


def test_ignore(init_db: Database):
    """数据类的忽略属性在建表时"""
    db = init_db
    db.dao_student2._create_table()
    db.commit()
    db.dao_student2.cursor.execute("PRAGMA table_info(student2);")
    # 获取所有列信息
    columns = db.dao_student2.cursor.fetchall()

    # 提取并打印所有字段名
    columns = set(column[1] for column in columns)
    entity_fields = set(attr_name for attr_name, attr_type in Student2.__annotations__.items())
    ignore_fields = {'score', 'address'}
    entity_fields_without_ignore = set(filter(lambda item: item not in ignore_fields, entity_fields))

    assert entity_fields != columns
    assert entity_fields_without_ignore == columns


def test_insert_ignore(init_db: Database):
    """数据类的忽略属性在插入记录时"""
    db = init_db
    student2 = Student2(name='张三', score=100, address='hit')
    db.dao_student2.insert(student2)
    db.commit()


def test_insert_many(init_db: Database):
    """批量插入"""
    db = init_db
    start = 101
    end = 200
    students2 = generate_students(start=start, end=end)
    db.dao_student.insert(entity=students2)
    db.commit()

    for i in range(start, end):
        result = db.dao_student.select_student_by_id(i)
        result = result[0]
        assert asdict(result) == asdict(students2[i - start])


# ====================================================================================================================

def test_fetchone(init_db: Database):
    """查询单记录"""
    db = init_db
    select_id = 90
    result1 = db.dao_student.select_student_by_id(select_id)
    result2 = db.dao_student.select_student_by_id_limit1(select_id)
    assert isinstance(result1, list)
    assert asdict(result1[0]) == asdict(result2)


def test_fetchone_no_record(init_db: Database):
    """查询不存在的单记录"""
    db = init_db
    select_id = 90
    db.dao_student.delete_student_by_id(student_id=select_id)
    result1 = db.dao_student.select_student_by_id(select_id)
    result2 = db.dao_student.select_student_by_id_limit1(select_id)
    assert not result1
    assert result2 is None


# ====================================================================================================================

def test_execute_sql(init_db: Database):
    """执行sql方法"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_one_student(student_id=select_id)
    assert isinstance(result, list)
    assert list
    assert asdict(result[0]) == asdict(students[select_id - 1])


def test_execute_sql_with_substitute(init_db: Database):
    """执行sql方法，使用替代符"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_one_student_with_substitute(student_id=select_id)
    assert asdict(result) == asdict(students[select_id - 1])


def test_execute_sql_with_limit(init_db: Database):
    """执行sql方法，使用limit"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_one_student_with_limit(student_id=select_id)
    assert asdict(result) == asdict(students[select_id - 1])


def test_execute_sql_with_substitute_and_limit(init_db: Database):
    """执行sql方法，使用替代符和limit"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_one_student_with_substitute_and_limit(student_id=select_id)
    assert asdict(result) == asdict(students[select_id - 1])


# ====================================================================================================================

def test_execute_sql_without_dao_func(init_db: Database):
    """执行sql方法"""
    db = init_db
    select_id = 10
    result = db.dao_student3.select_one_student(student_id=select_id)
    assert isinstance(result, list)
    assert list
    assert asdict(result[0]) == asdict(students[select_id - 1])


def test_execute_sql_with_substitute_without_dao_func(init_db: Database):
    """执行sql方法，使用替代符"""
    db = init_db
    select_id = 10
    result = db.dao_student3.select_one_student_with_substitute(student_id=select_id)
    assert asdict(result) == asdict(students[select_id - 1])


def test_execute_sql_with_limit_without_dao_func(init_db: Database):
    """执行sql方法，使用limit"""
    db = init_db
    select_id = 10
    result = db.dao_student3.select_one_student_with_limit(student_id=select_id)
    assert asdict(result) == asdict(students[select_id - 1])


def test_execute_sql_with_substitute_and_limit_without_dao_func(init_db: Database):
    """执行sql方法，使用替代符和limit"""
    db = init_db
    select_id = 10
    result = db.dao_student3.select_one_student_with_substitute_and_limit(student_id=select_id)
    assert asdict(result) == asdict(students[select_id - 1])


def test_execute_sql_with_conditions(init_db: Database):
    """执行sql方法，使用替代符和limit"""
    db = init_db
    select_id = 10
    result = db.dao_student.select_student_with_conditions(student_id=select_id, age=select_id)
    assert asdict(result) == asdict(students[select_id - 1])


# ====================================================================================================================
def test_row_factory(init_db: Database):
    db = init_db
    start = time.time()
    students = generate_students(1000, 100000)
    print(f'\n生成耗时：{time.time() - start}')

    start = time.time()
    db.dao_student.insert(students)
    db.commit()
    end = time.time() - start
    print(f'插入耗时：{end}')

    # 默认数据类
    start = time.time()
    results2 = db.dao_student.select_all2()
    end = time.time() - start
    print(f'entity_auto耗费时间：{end}, 查询结果数量；{len(results2)}')

    start = time.time()
    results3 = db.dao_student.select_all_full()
    end = time.time() - start
    print(f'entity_full_fast耗费时间：{end}, 查询结果数量；{len(results3)}')

    start = time.time()
    results4 = db.dao_student.select_all_part()
    end = time.time() - start
    print(f'entity_part耗费时间：{end}, 查询结果数量；{len(results4)}')

    start = time.time()
    results5 = db.dao_student.select_all_full_no_order()
    end = time.time() - start
    print(f'entity_full_not_order耗费时间：{end}, 查询结果数量；{len(results5)}')

    start = time.time()
    result6 = db.dao_student.select_all_part_and_no_order()
    end = time.time() - start
    print(f'entity_part_and_no_order耗费时间：{end}, 查询结果数量；{len(results4)}')
    assert results4 == result6
    assert results2 == results3 == results5

    start = time.time()
    results_dataclass = db.dao_student.select_all()
    end = time.time() - start
    print(f'dataclass耗费时间：{end}, 查询结果数量；{len(results_dataclass)}')

    start = time.time()
    results_dict = db.dao_student_dict.select_all()
    end = time.time() - start
    print(f'dict耗费时间：{end}, 查询结果数量；{len(results_dict)}')

    start = time.time()
    results_tuple = db.dao_student_tuple.select_all()
    end = time.time() - start
    print(f'tuple耗费时间：{end}, 查询结果数量；{len(results_tuple)}')

    start = time.time()
    results_namedtuple = db.dao_student.select_all_namedtuple()
    end = time.time() - start
    print(f'namedtuple耗费时间：{end}, 查询结果数量；{len(results_namedtuple)}')

    for item_dataclass, item_dict, item_tuple, item_namedtuple in zip(results_dataclass,
                                                                      results_dict,
                                                                      results_tuple,
                                                                      results_namedtuple):
        assert item_dict == item_namedtuple._asdict()
        assert item_tuple == item_namedtuple
        assert item_namedtuple._asdict() == asdict(item_dataclass)


# def test_row_factory_get_memory(init_db: Database):
#     db = init_db
#     start = time.time()
#     students = generate_students(1000, 1000000)
#     print(f'\n生成耗时：{time.time() - start}')
#
#     tracemalloc.start()
#     start = time.time()
#     db.dao_student.insert(students)
#     db.commit()
#     end = time.time() - start
#     current_memory, peak_memory = tracemalloc.get_traced_memory()
#     tracemalloc.stop()
#     print(f'插入耗时：{end}，内存占用：{peak_memory}')
#
#
#     # 默认数据类
#     tracemalloc.start()
#     start = time.time()
#     results = db.dao_student.select_all()
#     end = time.time() - start
#     current_memory, peak_memory = tracemalloc.get_traced_memory()
#     tracemalloc.stop()
#     print(f'dataclass耗费时间：{end}, 查询结果数量；{len(results)}，内存占用：{peak_memory}')
#
#     # 字典
#     tracemalloc.start()
#     start = time.time()
#     results = db.dao_student_dict.select_all()
#     end = time.time() - start
#     current_memory, peak_memory = tracemalloc.get_traced_memory()
#     tracemalloc.stop()
#     print(f'dict耗费时间：{end}, 查询结果数量；{len(results)}，内存占用：{peak_memory}')
#
#     # 元组
#     tracemalloc.start()
#     start = time.time()
#     results = db.dao_student_tuple.select_all()
#     end = time.time() - start
#     current_memory, peak_memory = tracemalloc.get_traced_memory()
#     tracemalloc.stop()
#     print(f'tuple耗费时间：{end}, 查询结果数量；{len(results)}，内存占用：{peak_memory}')
def test_dao_return_type_default_list(init_db: Database):
    db = init_db
    student = students[2]
    result = db.dao_student.select_student_by_id(student.student_id)
    assert result
    assert isinstance(result[0], Student)
    assert result[0] == student


def test_dao_return_type_default(init_db: Database):
    db = init_db
    student = students[2]
    result = db.dao_student.select_student_by_id_limit1(student.student_id)
    assert isinstance(result, Student)
    assert result == student


def test_dao_return_type_dict_list(init_db: Database):
    db = init_db
    student = students[2]
    result = db.dao_student_dict.select_student_by_id2(student.student_id)
    assert result
    assert isinstance(result[0], dict)
    assert result[0] == asdict(student)


def test_dao_return_type_dict(init_db: Database):
    db = init_db
    student = students[2]
    result = db.dao_student_dict.select_student_by_id(student.student_id)
    assert isinstance(result, dict)
    assert result == asdict(student)


def test_dao_return_type_tuple_list(init_db: Database):
    db = init_db
    student = students[2]
    result = db.dao_student_tuple.select_student_by_id2(student.student_id)
    assert result
    assert isinstance(result[0], tuple)
    assert result[0] == tuple(asdict(student).values())


def test_dao_return_type_tuple(init_db: Database):
    db = init_db
    student = students[2]
    result = db.dao_student_tuple.select_student_by_id(student.student_id)
    assert isinstance(result, tuple)
    assert result == tuple(asdict(student).values())


def test_select_single_field(init_db: Database):
    db = init_db
    student = students[3]

    s1 = db.dao_student.select_name_by_id_without_single_field(student.student_id)
    s2 = db.dao_student.select_name_by_id_with_single_field(student.student_id)
    assert s1.name == student.name
    assert s2 == student.name

    result1 = db.dao_student.select_name_by_id_without_single_field_list()
    result2 = db.dao_student.select_name_by_id_with_single_field_list()
    for item1, item2 in zip(result1, result2):
        assert type(item1.name) == str
        assert type(item2) == str


def test_bool(init_db: Database):
    db = init_db
    result1 = db.dao_student.select_bool()
    result2 = db.dao_student.select_bool_no_return_bool()
    assert type(result1) == bool
    assert type(result2.if_aged) == int


def test_sql_fetch_one(init_db: Database):
    db = init_db
    select_id = 3
    result1 = db.dao_student.select_student_by_id(select_id)
    result2 = db.dao_student.select_student_by_id_use_fetch_one(select_id)
    assert type(result1) == list
    assert type(result2) == Student
    assert result1[0] == result2


if __name__ == '__main__':
    pytest.main(["-vv",
                 "--capture=no",
                 __file__])
