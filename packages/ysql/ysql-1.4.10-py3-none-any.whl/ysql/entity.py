# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Union


# ====================================================================================================================
# 模块常量
@dataclass
class _Constraint:
    """内部维护的约束类，存储实际约束"""
    constraint: tuple


_PRIMARY_KEY = _Constraint(constraint=("PRIMARY KEY",))
_AUTO_PRIMARY_KEY = _Constraint(constraint=("PRIMARY KEY AUTOINCREMENT",))
_NOT_NULL = _Constraint(constraint=("NOT NULL",))
_UNIQUE = _Constraint(constraint=("UNIQUE",))
_IGNORE = _Constraint(constraint=("ignore",))

_NO_ACTION = 'NO ACTION'
_RESTRICT = 'RESTRICT'
_CASCADE = 'CASCADE'
_SET_NULL = 'SET NULL'
_SET_DEFAULT = 'SET DEFAULT'

_ENABLED_TYPES = (int, str, float, bytes, bool, type(None))
_ENABLED_UNION = Union[_ENABLED_TYPES]
_ENTITY_INIT = "__entity_init__"


# ====================================================================================================================
def Entity(check_type: bool = False):
    """数据类dataclass的装饰器。

    在定义dataclass时，同时将约束条件和默认值赋予类属性。
    通过改造原生dataclass的init方法和getattribute方法，实现sql建表时约束条件的解析，以及正常使用被装饰dataclass时属性值的获取。

    Args:
        check_type(bool): 传入True -> 实例化dataclass时检查属性值和类型注释是否一致，不一致将触发类型错误。否则不检查。

    Example1:

        @Entity
        @dataclass
        class Student:  # 类名即表名，不区分大小写
            name: str  # 字段名以及字段类型
            score: float = 100

    Example2:

        @Entity(check_type=True)  # 启用类型检查
        @dataclass
        class Student:
            name: str  # 字段名以及字段类型
            score: float = 100.0
            # Example1中的score属性虽然注释为float，而实际默认值为int，但仍然可以正常工作（由于python和sqlite都是宽松的类型约束）。
            # 若使用check_type，将进行严格的检查，类型不一致的情况（如Example1）会抛出异常。

    !Note:
        在实用角度上@dataclass应该合并到@Entity内部，这样定义数据类时只需要使用一个装饰器，并且不需要初级使用者关心什么是dataclass，
        但经过测试发现，如果不显式的使用@dataclass装饰器，在实例化数据类时Pycharm将无法给出代码提示，这是不可忍受的。
        并且经过测试发现只有Pycharm2020及之前的版本可以正确给出代码提示，高于2020版存在代码提示的bug，详见:
        https://intellij-support.jetbrains.com/hc/en-us/community/posts/4421575751442-Code-Completion-doesn-t-work-for-class-functions-decorated-with-decorators-that-return-inner-functions

    """

    def decorator(cls):
        orig_get_attr = cls.__getattribute__
        orig_init = cls.__init__

        def get_attr(self, name):
            """重写被装饰dataclass的取值方法"""
            # 只有访问定义的属性时才进一步处理
            orig_value = orig_get_attr(self, name)
            if name in set(attr_name for attr_name, attr_type in cls.__annotations__.items()):
                return _parse_attr_value(orig_value)
            # 访问内部属性则返回原始值
            return orig_value

        def init_and_check_type(self, *args, **kwargs):
            """重写被装饰dataclass的初始化方法"""
            orig_init(self, *args, **kwargs)
            for attr_name, attr_type in cls.__annotations__.items():
                # 再检查属性值的类型与类型注解是否一致
                attr_value = get_attr(self, attr_name)
                # 不检查默认值为None的属性
                if attr_value is None:
                    continue
                elif type(attr_value) != attr_type:
                    raise TypeError(
                        f"实例化'{cls.__name__}'类时,"
                        f"'{attr_name}'属性的类型应该是 '{attr_type.__name__}' ,"
                        f"但得到的是 '{type(attr_value).__name__}'")

        # 由于无参装饰器的特性，在无参使用该装饰器时，check_type的值被覆盖为cls，因此必须显式的与True进行判断
        if check_type == True:  # noqa
            cls.__init__ = init_and_check_type
        setattr(cls, _ENTITY_INIT, orig_init)
        cls.__getattribute__ = get_attr
        return cls

    # 无参使用该装饰器时
    if callable(check_type):
        return decorator(cls=check_type)  # noqa

    return decorator


def is_entity(obj):
    return hasattr(obj, _ENTITY_INIT)


class Constraint:
    """对外开放的各种字段约束。

    Example:

        @Entity
        @dataclass
        class Student:
            name: str  # 可以不使用约束
            score: float = 100  # 可以只赋予默认值
            address: str = 'HIT', Constraint.not_null  # 同时使用默认值和约束，需要以逗号分隔开
            student_id: int = Constraint.auto_primary_key, Constraint.not_null  # 同时使用多条约束，需要以逗号分隔开

    !Note:
        建议导入Constraint类时使用别名，可以有效简化存在大量约束的使用场景。

        Example:

            from ysql import Constraint as cs

            @Entity
            @dataclass
            class Student:
                name: str
                score: float = 100
                address: str = 'HIT', cs.not_null
                student_id: int = cs.auto_primary_key, cs.not_null

    """

    # =================================================================================================================
    # 1.可直接使用的约束常量
    primary_key = _PRIMARY_KEY  # 主键
    auto_primary_key = _AUTO_PRIMARY_KEY  # 自增主键
    not_null = _NOT_NULL  # 非空
    unique = _UNIQUE  # 唯一

    # 非sql的特殊约束
    ignore = _IGNORE  # 用于建表时忽略某字段/属性

    # 针对外键的约束
    no_action = _NO_ACTION
    cascade = _CASCADE
    set_null = _SET_NULL
    restrict = _RESTRICT
    set_default = _SET_DEFAULT

    # =================================================================================================================
    # 2.需要外部传值的约束
    @staticmethod
    def default(default_value: _ENABLED_UNION):
        """默认值约束

        Args:
            default_value: 该字段在sql中的默认值，与定义数据类时使用默认值作用类似。

        Example:

            @Entity
            @dataclass
            class Student:
                name: str
                score1: float = 100
                score2: float = Constraint.default(100)  # score1和score2的作用类似
                student_id: int = Constraint.auto_primary_key

        """
        if type(default_value) in _ENABLED_TYPES:
            return _Constraint(constraint=(f'DEFAULT {default_value}',))  # noqa
        raise TypeError(
            f"dataclass属性默认值允许的数据类型: 'int', 'str', 'float', 'bytes',"
            f"但得到的是 '{type(default_value).__name__}'"
        )

    @staticmethod
    def check(check_condition: str):
        """条件约束

        Args:
            check_condition: 具体条件

        Example:

            @Entity
            @dataclass
            class Student:
                name: str
                score: float = Constraint.check('score > 60')  # 需要填写字段的字符形式名称
                student_id: int = Constraint.auto_primary_key

        """
        if type(check_condition) == str:
            return _Constraint(constraint=(f'CHECK({check_condition})',))  # noqa
        raise TypeError(
            f"对dataclass属性使用条件约束时，允许的数据类型: 'str',"
            f"但得到的是 '{type(check_condition).__name__}'")

    @staticmethod
    def foreign_key(entity, field, delete_link=None, update_link=None):
        """外键约束

        Args:
            entity: 外键所在的数据类（父表）
            field: 外键对应的数据类属性
            delete_link: 级联删除方式
            update_link: 级联更新方式

        Example:

            @Entity
            @dataclass
            class Student:  # 父表
                name: str = Constraint.not_null
                student_id: int = Constraint.auto_primary_key

            @Entity
            @dataclass
            class Score:  # 子表
                score: float
                score_id: int = Constraint.auto_primary_key
                # 对student_id字段设置外键关联
                student_id: int = Constraint.foreign_key(entity=Student,
                                                         field='student_id',
                                                         delete_link=Constraint.cascade,
                                                         update_link=Constraint.cascade)

        """
        return _Constraint(constraint=((entity.__name__.lower(), field, delete_link, update_link),))  # noqa

    @staticmethod
    def comment(comment: str):
        """字段注释

        Args:
            comment: 具体注释。注意，在sqlite中只能通过DDL(Data Definition Language)查看。

        Example:

            @Entity
                @dataclass
                class Student:
                    name: str = Constraint.comment('学生姓名')
                    student_id: int = Constraint.auto_primary_key, Constraint.comment('学生id')

        """
        if type(comment) == str:
            # 目前仅支持sqlite的注释格式
            return _Constraint(constraint=(f'-- {comment}\n',))  # noqa
        raise TypeError(
            f"对dataclass属性使用sql注释时，允许的数据类型: 'str',"
            f"但得到的是 '{type(comment).__name__}'")


# ====================================================================================================================
# 模块方法
def _parse_constraints(attr_value) -> list[str, tuple]:
    """从属性原始值中解析出约束条件。
    Args:
        attr_value: 属性原始值(同时包含默认值和约束条件，但仅在定义数据类时有效，实例化后不再包含约束条件)，如Student.name

    Returns:
        list[约束1, 约束2, 约束3, ...]

    Example:

        @Entity
        @dataclass
        class Student:
            name: str = Constraint.comment('学生姓名')
            student_id: int = Constraint.auto_primary_key, Constraint.comment('学生id')

        print(parse_constraints(Student.name))  # output: ['-- 学生姓名\n']
        print(parse_constraints(Student.student_id))  # output: ['PRIMARY KEY AUTOINCREMENT', '-- 学生id\n']

    """
    # 无约束
    constraints = []
    # 是单约束
    if isinstance(attr_value, _Constraint):
        constraints = list(attr_value.constraint)
    # 包含多约束
    elif isinstance(attr_value, tuple):
        for item in attr_value:
            if not isinstance(item, _Constraint):
                continue

            if item in constraints:
                raise TypeError(
                    f"重复使用了约束条件: {item.constraint}")

            constraints.append(item.constraint[0])

    return constraints


def _parse_attr_value(attr_value) -> _ENABLED_UNION:
    """从属性原始值中过滤约束条件，解析出真正的属性值。并不负责检查值是否匹配类型。

    Args:
        attr_value: 属性原始值(同时包含默认值和约束条件，但仅在定义数据类时有效，实例化后不再包含约束条件)，如Student.name

    Returns:
        真正的属性值

    Example:

        @Entity
        @dataclass
        class Student:
            name: str
            student_id: int = Constraint.auto_primary_key

        bob = Student(name='Bob')
        print(parse_attr_value(bob.name))  # output: 'Bob'
        print(parse_attr_value(bob.student_id))  # output: None

    !Note:
        如果对数据类的某个属性使用了约束，且未指定默认值，而在实例化时不传入该属性的值。这不会引发实例化错误，该属性会存在一个默认的None值。
        因此在实例化时请仔细检查是否对每个需要赋值的属性都完成了赋值，避免遗漏某个属性的赋值。

        Example:

            @Entity
            @dataclass
            class Student:
                name: str
                student_id: int = Constraint.auto_primary_key  # 不指定默认值

            bob = Student(name='Bob')  # 实例化时不对student_id传值
            print(bob.student_id)  # output: None

    """

    # 是单个约束
    if isinstance(attr_value, _Constraint):
        return None

    # 多约束
    elif isinstance(attr_value, tuple):
        parsed_value = []

        for item in attr_value:
            if isinstance(item, _Constraint):
                continue
            parsed_value.append(item)

        # 仅多个约束
        if len(parsed_value) == 0:
            return None
        # 包含单个值
        elif len(parsed_value) == 1:
            return parsed_value[0]
        # tuple类型的值
        return tuple(parsed_value)

    return attr_value
