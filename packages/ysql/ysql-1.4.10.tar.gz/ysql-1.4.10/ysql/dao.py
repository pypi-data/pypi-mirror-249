# -*- coding: utf-8 -*-
import copy
from collections import namedtuple
from dataclasses import make_dataclass, dataclass

from ysql.entity import Constraint, _parse_constraints, _ENABLED_TYPES, is_entity

# ====================================================================================================================
# 模块常量
TABLE_SUBSTITUTE = '__'  # 约定的表名代替符，内部可自动替换。
FETCH_FLAG = ('limit 1', 'limit 1;')
_DATACLASS = 'dataclass'
_RECORD = 'Record'
_ENABLED_BASIC_TYPES = (int, str, float, bytes, bool)


# ====================================================================================================================
# 装饰器方法
def Dao(entity, return_type=tuple, auto_fetch_one: bool = True, enable_substitute: bool = True):
    """对数据访问类使用的装饰器，用于绑定数据类和数据访问类。

    Args:
        entity: 该数据访问类对应的数据类。
        return_type: 应属于[tuple, dict, dataclass, namedtuple, your_entity, int, str, float, bytes, bool]
                    设置查询结果中 !单条记录! 的数据类型。
        auto_fetch_one: 如果语句结尾包含 'limit 1' 将自动识别并直接返回单条记录，否则默认返回以列表形式存储的任意条记录。
        enable_substitute: 启用表名替代符 '__' ，在sql语句中凡是涉及表名的，均可使用 '__' ，内部会自动转换为绑定entity的类名。

    Example:

        @Entity
        @dataclass
        class Student:  # 定义一个数据类
            name: str
            score: float

        @Dao(Student)  # 通过Dao装饰器绑定对应的数据类
        class DaoStudent:  # 定义一个数据访问类
            ...

    """

    def decorator(cls):
        # 新增属性
        cls.cursor = None
        cls.entity = entity
        cls.auto_fetch_one = auto_fetch_one
        cls.enable_substitute = enable_substitute
        cls.return_type = return_type if return_type != dataclass else _DATACLASS
        # 新增方法
        cls.execute = execute
        cls.update_cursor = update_cursor
        cls._create_table = _create_table
        cls._generate_sql_create_table = _generate_sql_create_table
        return cls

    return decorator


def Sql(sql: str, return_type=None, fetch_one: bool = False):
    """执行sql语句的装饰器，传入sql语句的同时会自动实现被装饰函数。

    Args:
        sql: 固定字符串sql语句。
        return_type: 应属于[tuple, dict, dataclass, namedtuple, your_entity, int, str, float, bytes, bool]
                    设置查询结果中 !单条记录! 的数据类型，若Dao和Sql同时设置该参数，则遵循Sql的return_type。
        fetch_one: 设置是否直接返回单条记录，否则默认返回以列表形式存储的任意条记录，若Dao和Sql同时设置该参数，则遵循Sql的fetch_one。

    Return:
        使用select时，将结合return_type自动返回指定格式的查询结果。

    Example:

        # 对于固定的sql语句可以直接传入Sql装饰器。
        # 此段代码无法直接运行，需要首先连接数据库并插入记录才可运行。

        @Entity
        @dataclass
        class Student:
            name: str
            score: float
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent:

            @Sql("select * from student where student_id=?;")
            def get_student(self, student_id):
                pass  # 此处并非以pass示意省略，而是Sql装饰器会自动实现该函数，因此实际使用时均只需要pass即可。

        dao = DaoStudent()
        result = dao.get_student(student_id=1)

        # 将以列表形式返回查询结果，其中每条记录的数据格式默认为dataclass格式。
        # result1: [Record(name, score, student_id), ...]
        # 查询部分字段时，仅以查询的字段生成相应的dataclass。

    !Note:
        1.对于固定的静态sql语句，通过Sql装饰器传递sql语句，被装饰器函数传递数据。
        2.对于复杂的动态sql语句，不应使用Sql装饰器，应使用dao.execute方法。

    """

    def decorator(func):  # noqa

        def wrapper(self, *args, **kwargs):
            if not type(sql) == str:
                raise ValueError(
                    f"传入的sql参数应该是 'str' 类型，但得到的是 '{type(sql).__name__}'类型")

            final_sql = __check_substitute(sql=sql,
                                           entity=self.entity,
                                           enable_substitute=self.enable_substitute)

            self.cursor.execute(final_sql, (*args, *kwargs.values()))
            return __fetch_result(self=self,
                                  sql=final_sql,
                                  cursor=self.cursor,
                                  return_type=return_type,
                                  fetch_one=fetch_one)

        return wrapper

    if callable(sql):
        raise ValueError(
            f"Sql装饰器需要传入一个 'str' 类型的参数")

    return decorator


def Insert(func):  # noqa
    """执行插入功能的装饰器，会自动生成插入sql语句，以及自动实现被装饰函数。

    Returns:
        自动返回刚插入记录的自增主键（如果使用自增主键）。

    Example:

        # 此段代码无法直接运行，需要首先连接数据库才可运行。

        @Entity
        @dataclass
        class Student:
            name: str
            score: float
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent:

            @Insert  # 无需传递任何参数或者sql语句。
            def insert(self, entity):
                pass  # 此处并非以pass示意省略，而是Insert装饰器会自动实现该函数，因此实际使用时均只需要pass即可。

        dao = DaoStudent()
        # 插入单条记录
        student = Student(name='Bob', score=95.5)  # 将整条记录以数据类的形式插入数据库，避免了同时使用多个参数的麻烦。
        dao.insert(entity=student)
        # 批量插入多条记录
        students = [Student(name='Bob', score=i) for i in range(100)]
        dao.insert(entity=students)
    """

    def wrapper(self, entity):
        """entity参数是传入的数据类实例（对象），而self.entity是定义的数据类（类）"""
        # 获取entity类的属性名和类型
        fields = [field_name for field_name, _ in self.entity.__annotations__.items()]

        # 定义需过滤的属性
        ignore_fields = {Constraint.auto_primary_key.constraint[0],
                         Constraint.ignore.constraint[0]}
        ignore_fields = {field_name for field_name in fields
                         if ignore_fields & set(_parse_constraints(attr_value=getattr(self.entity, field_name, None)))}
        # 过滤属性
        filtered_fields = [field_name for field_name in fields
                           if field_name not in ignore_fields]

        sql = f"insert into {self.entity.__name__} " \
              f"({', '.join(field_name for field_name in filtered_fields)}) " \
              f"values ({', '.join('?' for _ in filtered_fields)});"

        if type(entity) in (list, tuple):
            values = ([getattr(item, field_name) for field_name in filtered_fields]
                      for item in entity)
            self.cursor.executemany(sql, values)
            return

        cls_fields = set(field_name for field_name, _ in entity.__annotations__.items()
                         if field_name not in ignore_fields)
        if cls_fields == set(filtered_fields):
            values = [getattr(entity, field_name) for field_name in filtered_fields]
            self.cursor.execute(sql, values)
            return self.cursor.lastrowid

        else:
            raise TypeError(
                f"Insert的被装饰函数的参数类型应该是:\n"
                f"1.绑定的Entity数据类的实例\n"
                f"2.包含多个数据类的序列，'list' or 'tuple' "
                f"但得到的是 {type(entity).__name__}")

    return wrapper


# ====================================================================================================================
# 提前实现了一些可用方法的功能类，建议继承。
class DaoFunc:
    """
    Example:
        @Entity
        @dataclass
        class Student:
            name: str
            score: float
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent(DaoFunc):
            pass

    """

    @Insert
    def insert(self, entity):
        """插入单条或多条数据记录

        Args:
            entity: 数据类的实例，或包含多个数据类的序列。

        Returns:
            自动返回刚插入记录的自增主键（如果使用自增主键）。

        """
        pass

    def execute(self, sql: str, args=None, return_type=None, fetch_one: bool = False):
        """执行sql语句

        Args:
        self: 自动传递
        sql: 固定字符串sql语句。
        args: 执行该sql需要的参数。
        return_type: 应属于[tuple, dict, dataclass, namedtuple, your_entity, int, str, float, bytes, bool]
                    设置查询结果中 !单条记录! 的数据类型，若Dao和execute同时设置该参数，则遵循execute的return_type。
        fetch_one: 设置是否直接返回单条记录，否则默认返回以列表形式存储的任意条记录，若Dao和execute同时设置该参数，则遵循execute的fetch_one。

        Returns:
            使用select时，将结合return_type自动返回指定格式的查询结果。

        """
        pass


# ====================================================================================================================
# Dao类新增的方法
def execute(self, sql: str, args=None, return_type=None, fetch_one: bool = False):
    """执行sql语句"""
    sql = __check_substitute(sql=sql,
                             entity=self.entity,
                             enable_substitute=self.enable_substitute)
    if args is None:
        self.cursor.execute(sql)
    elif type(args) in _ENABLED_TYPES:
        self.cursor.execute(sql, (args,))
    elif type(args) in (list, tuple):
        self.cursor.execute(sql, __flatten_args(args))

    return __fetch_result(self=self, sql=sql, cursor=self.cursor, return_type=return_type, fetch_one=fetch_one)


def _create_table(self):
    """依据entity创建表"""
    sql = self._generate_sql_create_table()
    self.cursor.execute(sql)


def update_cursor(self, cursor):
    """更新dao中的游标"""
    self.cursor = cursor


def _generate_sql_create_table(self):
    """自动生成建表语句"""
    table_name = self.entity.__name__.lower()
    # 获取字段名称和类型的字典
    fields = self.entity.__annotations__

    field_definitions = []
    foreign_key_constraints = []

    for field_name, field_type in fields.items():
        # 获取字段的约束条件
        constraints = _parse_constraints(attr_value=getattr(self.entity, field_name, None))
        # 跳过忽略属性
        if Constraint.ignore.constraint[0] in constraints:
            continue

        foreign_key_constraint = [item for item in constraints
                                  if isinstance(item, tuple)]
        constraints = [item for item in constraints
                       if item not in foreign_key_constraint]
        # 有外键
        if len(foreign_key_constraint) == 1:
            foreign_key_constraint = __generate_sql_foreign_key(field_name=field_name,
                                                                constraint=foreign_key_constraint[0])
            foreign_key_constraints.append(foreign_key_constraint)

        elif len(foreign_key_constraint) > 1:
            raise TypeError(
                '一个属性只能指定一个外键')

        # 合并其他约束条件
        constraint = " ".join(constraints)
        # 获取字段的SQL类型
        sql_type = __convert_to_sql_type(field_type)
        # 拼接字段定义
        field_definition = f"{field_name} {sql_type} {constraint}"
        field_definitions.append(field_definition)
    # 将外键约束列表添加到字段定义列表的末尾
    field_definitions.extend(foreign_key_constraints)
    # 默认为严格的数据类型约束
    sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(field_definitions)});"
    return sql_create_table


# ====================================================================================================================
# 模块内的静态方法
def __convert_to_sql_type(python_type):
    """转换python注释类型为sql类型"""
    if python_type == int:
        return "INTEGER"
    elif python_type == str:
        return "TEXT"
    elif python_type == float:
        return "REAL"
    elif python_type == bool:
        return "BOOL"
    elif python_type == bytes:
        return "BLOB"

    raise ValueError(
        f"ysql不支持该python数据类型: {python_type}")  # noqa


def __generate_sql_foreign_key(constraint: tuple, field_name: str):
    """生成外键约束的sql语句"""
    foreign_key_entity, foreign_key_name, foreign_key_delete_link, foreign_key_update_link = constraint

    if foreign_key_delete_link is None and foreign_key_update_link is None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name})"

    # 存在表关联的情况
    elif foreign_key_delete_link is not None and foreign_key_update_link is None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) ON DELETE {foreign_key_delete_link}"
    elif foreign_key_delete_link is None and foreign_key_update_link is not None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) ON UPDATE {foreign_key_update_link}"
    elif foreign_key_delete_link is not None and foreign_key_update_link is not None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) " \
               f"ON DELETE {foreign_key_delete_link} ON UPDATE {foreign_key_update_link} "


def __check_substitute(sql: str, entity, enable_substitute):
    """检查并替换表名代替符"""
    if enable_substitute:
        return sql.replace(TABLE_SUBSTITUTE, entity.__name__.upper())
    return sql


def __flatten_args(args):
    """一维展开不定参数，并返回元组形式"""

    def flatten_args(arg):
        if type(arg) in (list, tuple):
            # 如果是列表或元组，递归展开每个元素
            return [item for sublist in map(flatten_args, arg) for item in sublist]
        elif type(arg) == dict:
            # 如果是字典，取出所有值并递归展开
            return flatten_args(list(arg.values()))
        elif type(arg) in _ENABLED_TYPES:
            # 否则返回单个值
            return [arg]
        else:
            raise ValueError(
                f"args参数的类型应该是 'list' or 'tuple' or 'dict' ,但得到的是 '{type(arg).__name__}'"
            )

    return tuple(flatten_args(args))


# --------------------------------------------------------------------------------------------------------------------
# 设置返回结果格式
def __return_entity(entity, cursor, result, is_list=True):
    """返回查询结果为传入的entity数据类"""
    cursor_fields = [column[0] for column in cursor.description]
    entity_fields = [attr_name for attr_name, _ in entity.__annotations__.items()]
    reordered_row = [None] * len(entity_fields)

    # 检查是否所有cursor字段都在entity中
    if not all(field in entity_fields for field in cursor_fields):
        raise ValueError("查询的值超过了传入entity的属性范围。")

    def create_entity_fast(row):
        _entity = entity.__new__(entity)
        entity.__entity_init__(_entity, *row)
        return _entity

    def create_entity(row):
        inner_row = reordered_row[:]
        # 根据 order 中的位置重排列row元素
        for i, position in enumerate(field_order):
            inner_row[position] = row[i]

        _entity = entity.__new__(entity)
        entity.__entity_init__(_entity, *inner_row)
        return _entity

    if cursor_fields == entity_fields:
        create = create_entity_fast
    else:
        # 映射cursor字段到entity字段
        field_order = [entity_fields.index(field) for field in cursor_fields]
        create = create_entity

    if is_list:
        return [create(row) for row in result]
    return create(result)


def __return_dataclass(cursor, result, is_list=True):
    """返回询结果为dataclass"""
    fields = [column[0] for column in cursor.description]
    Record = make_dataclass(_RECORD, fields)
    if is_list:
        return [Record(*row) for row in result]
    return Record(*result)


def __return_dict(cursor, result, is_list=True):
    """返回查询结果为字典"""
    fields = [column[0] for column in cursor.description]
    if is_list:
        return [dict(zip(fields, item)) for item in result]
    return dict(zip(fields, result))


def __return_namedtuple(cursor, result, is_list=True):
    """返回查询结果为具名元组"""
    fields = [column[0] for column in cursor.description]
    Record = namedtuple(_RECORD, fields)
    if is_list:
        return [Record._make(row) for row in result]  # noqa
    return Record._make(result)  # noqa


def __return_one_field(result, return_type, is_list=True):
    """提取出单字段并返回，并处理bool类型"""
    if return_type != bool:
        if is_list:
            return [item[0] if item is not None else item
                    for item in result]
        return result[0] if result is not None else result
    else:
        if is_list:
            return [bool(item[0]) if item is not None else item
                    for item in result]
        return bool(result[0]) if result is not None else result


def __is_auto_fetch_one(sql: str, auto_fetch_one: bool) -> bool:
    """判断是否仅取一条记录"""
    return auto_fetch_one and any([sql.endswith(flag) for flag in FETCH_FLAG])


def __fetch_result(self, sql, cursor, return_type, fetch_one: bool):
    """确定返回类型"""
    lower_sql = sql.lower()

    _return_type = copy.deepcopy(self.return_type)
    if return_type is not None:
        _return_type = return_type

    if __is_auto_fetch_one(lower_sql, self.auto_fetch_one) or fetch_one:
        is_list = False
        result = cursor.fetchone()
    else:
        is_list = True
        result = cursor.fetchall()

    # 不做转换
    if not result or _return_type == tuple:
        return result

    elif is_entity(_return_type):
        return __return_entity(entity=_return_type, cursor=cursor, result=result, is_list=is_list)

    elif _return_type in _ENABLED_BASIC_TYPES:
        return __return_one_field(result=result, return_type=_return_type, is_list=is_list)

    elif _return_type == _DATACLASS:
        return __return_dataclass(cursor=cursor, result=result, is_list=is_list)

    elif _return_type == dict:
        return __return_dict(cursor=cursor, result=result, is_list=is_list)

    elif _return_type == namedtuple:
        return __return_namedtuple(cursor=cursor, result=result, is_list=is_list)

    else:
        raise TypeError(
            f"Dao的查询结果格式设置错误，应该属于: 'tuple' 'dict' 'dataclass' 'entity'，但得到的是: {_return_type}")
