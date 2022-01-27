from typing import Union, List, Dict, Tuple

from ..version import __version__


def indent(s, n):
    return ('\n' + ' ' * n).join(s.split('\n'))


class Entity:
    def __init__(self, name: str, pk: Union[str, List[str]], sql: str = None):
        """

        Args:
            name: 如果sql是None，那么name表示table name，否则name表示根据sql新建的view name
            pk: (str or list of str) 主键
            sql: 如果sql不是None，那么根据sql生成一个新的view
        """
        self.version = __version__
        self.name = name
        if isinstance(pk, str):
            pk = [pk]
        elif isinstance(pk, list):
            for _pk in pk:
                assert isinstance(_pk, str), '{} is not a str'.format(_pk)
        else:
            raise TypeError('pk should be str or list, but got {}'.format(type(pk)))
        self.pk = pk
        self._sql = sql

    @property
    def sql(self):
        if self._sql is None:
            return self.name
        else:
            return self._sql

    @property
    def pk_unique_assertion_sql(self):
        """判别主键唯一的sql"""
        sql = """select
    assert_true(cnt=d_cnt)
from (
    select
        count({pk}) cnt,
        count(distinct {pk}) d_cnt
    from
        {table}"""
        sql = sql.format(pk=', '.join(self.pk), table=self.name)
        return sql


class Relationship:
    def __init__(self,
                 left_name: str,
                 right_name: str,
                 right_fields: List[str],
                 on: Union[str, List[str]] = None,
                 left_on: Union[str, List[str]] = None,
                 right_on: Union[str, List[str]] = None,
                 time_conds: List[Tuple[str, str, Union[int, None], Union[int, None]]] = None):
        """

        Args:
            left_name: 左表名
            right_name: 有表名
            on: (str or list of str)同名关联字段
            left_on: (str or list of str)坐标不同名关联字段，需要与right_on长度相同
            right_on: (str or list of str)右表不同名关联字段，需要与left_on长度相同
            time_conds: (list of tuple of four strings)时间关联条件，[(左表字段，右表字段，时间左边界（天），时间右边界（天）)]
                    例如 （tim1, tim2, 1, 2)
                    date_sub(tim1, 1) < tim2 < date_add(tim1, 2)
        Returns:

        """
        self.version = __version__
        self.left_name = left_name
        self.right_name = right_name
        self.right_fields = right_fields

        def format_on(x):
            if isinstance(x, str):
                x = [x]
            elif x is None:
                x = []
            assert isinstance(x, list)
            return x

        on = format_on(on)
        left_on = on + format_on(left_on)
        right_on = on + format_on(right_on)
        assert len(left_on) == len(right_on)
        self.left_on = left_on
        self.right_on = right_on
        self.time_conds = time_conds

    def gen_sql(self, left_pk: List[str]):
        """join两张表"""
        sql = "select"
        for pk in left_pk:
            sql += '\n    a.{},'.format(pk)
        sql += '\n    struct('
        for right_field in self.right_fields:
            sql += '\n        b.{},'.format(right_field)
        sql = sql[:-1]

        sql += """\n    ) {}\n""".format(self.right_name)
        sql += """from
    {left_table} a
    inner join
    {right_table} b
    on """
        on_conds = []
        for left_on, right_on in zip(self.left_on, self.right_on):
            on_conds.append('a.{} = b.{}'.format(left_on, right_on))
        for left_time, right_time, lower_day, upper_day in self.time_conds:
            if lower_day is None:
                on_conds.append('a.{} <= b.{}'.format(left_time, right_time))
            else:
                on_conds.append('date_sub(a.{}, {}) <= b.{}'.format(left_time, lower_day, right_time))
            if upper_day is None:
                on_conds.append('b.{} < a.{}'.format(right_time, left_time))
            else:
                on_conds.append('b.{} < date_add(a.{}, {})'.format(right_time, left_time, upper_day))
        on_conds = '\n    and '.join(on_conds)
        sql += on_conds

        group_by_sql = """select"""
        for pk in left_pk:
            group_by_sql += '\n    {},'.format(pk)
        group_by_sql += '\n    collect_list({right_name}) {right_name}\nfrom (\n    '.format(right_name=self.right_name)
        group_by_sql += indent(sql, 4)
        group_by_sql += '\n)\ngroup by'
        for pk in left_pk:
            group_by_sql += '\n    {},'.format(pk)
        return group_by_sql[:-1]


class EntitySet:
    """
    根据定义好的ER图，生成json取数和校验数据一致性的sql
    """
    def __init__(self):
        self.version = __version__
        self.entities: Dict[str, Entity] = {}
        self.relationships: Dict[str, Dict[str, Relationship]] = {}

    def get_entity(self, name) -> Entity:
        return self.entities[name]

    def get_relationship(self, left_name, right_name) -> Relationship:
        return self.relationships[left_name][right_name]

    def add_entity(self, name, *args, **kwargs):
        assert name not in self.entities
        self.entities[name] = Entity(name, *args, **kwargs)
        self.relationships[name] = {}

    add_entity.__doc__ = Entity.__init__.__doc__

    def reset_entity(self, name, *args, **kwargs):
        assert name in self.entities
        del self.entities[name]
        return self.add_entity(name, *args, **kwargs)

    reset_entity.__doc__ = reset_entity.__doc__

    def add_rs(self, left_name, right_name, right_fields, on=None, left_on=None, right_on=None, time_conds=None):
        assert left_name in self.entities
        assert right_name in self.entities
        self.relationships[left_name][right_name] = Relationship(
            left_name=left_name, right_name=right_name, right_fields=right_fields, on=on, left_on=left_on,
            right_on=right_on, time_conds=time_conds
        )

    add_rs.__doc__ = Relationship.__init__.__doc__

    def _gen_sql(self, left_name):
        left_entity = self.get_entity(left_name)
        if len(self.relationships[left_name]) == 0:
            return left_entity.sql

        sql = 'select'
        for pk in left_entity.pk:
            sql += '\n    {},'.format(pk)
        sql += '\n    struct('
        for right_name in self.relationships[left_name]:
            sql += '\n        {},'.format(right_name)
        sql = sql[:-1] + '\n    )\nfrom (\n    {}\n) l'.format(indent(left_entity.sql, 4))
        for i, right_name in enumerate(self.relationships[left_name]):
            right_entity = self.get_entity(right_name)
            sql += '\n    left join (\n    {}\n) r{}\n    on {}'.format(
                indent(self._gen_sql(right_name), 4), i,
                '\n    and '.join('l.{field} = r{i}.{field}'.format(field=field, i=i) for field in left_entity.pk)
            )

        return sql

    def join(self, left_name):
        output_df = self._join(left_name)
        print(output_df)
        return output_df.withColumn(left_name, F.to_json(left_name))
