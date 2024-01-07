#！/usr/bin/env python3
# -*- coding:utf-8 -*-

from . import exec
from .loader import Loader


class Param:

    def __init__(self, sql_exec, *args, **kwargs):
        self.sql_exec = sql_exec
        self.args = args
        self.kwargs = kwargs

    def execute(self) -> int:
        """
        sqlexec.sql('INSERT INTO person(name, age) VALUES(?, ?)').param('张三', 18).execute()
        """
        return self.sql_exec.execute(*self.args, **self.kwargs)

    def save(self, select_key: str):
        """
        sqlexec.sql('INSERT INTO person(name, age) VALUES(?, ?)').param('张三', 18).save('SELECT LAST_INSERT_ID()')
        """
        return self.sql_exec.save(select_key, *self.args, **self.kwargs)

    def get(self):
        """
        sqlexec.sql('SELECT count(1) FROM person WHERE name=? and age=? limit 1').param('张三', 18).get()
        """
        return self.sql_exec.get(*self.args, **self.kwargs)

    def select(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).select()
        """
        return self.sql_exec.select(*self.args, **self.kwargs)

    def select_one(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=? limit 1').param('张三', 18).select_one()
        """
        return self.sql_exec.select_one(*self.args, **self.kwargs)

    def query(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).query()
        """
        return self.sql_exec.query(*self.args, **self.kwargs)

    def query_one(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=? limit 1').param('张三', 18).query_one()
        """
        return self.sql_exec.query_one(*self.args, **self.kwargs)

    def to_csv(self, file_name: str, delimiter=',', header=True, encoding='utf-8'):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).to_csv('test.csv')
        """
        self.sql_exec.load(*self.args, **self.kwargs).to_csv(file_name, delimiter, header, encoding)

    def to_df(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).to_df()
        """
        return self.sql_exec.load(*self.args, **self.kwargs).to_df()

    def to_json(self, file_name: str, encoding='utf-8'):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).to_json('test.json')
        """
        self.sql_exec.load(*self.args, **self.kwargs).to_json(file_name, encoding)


class SqlExec:

    def __init__(self, sql, executor):
        self.sql = sql
        self.executor = executor

    def execute(self, *args, **kwargs) -> int:
        """
        Execute sql return effect rowcount

        sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
             INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.execute(self.sql, *args, **kwargs)

    def save(self, select_key: str, *args, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param args:
        :return: Primary key
        """
        return self.executor.save_sql(select_key, self.sql, *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
             SELECT count(1) FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.get(self.sql, *args, **kwargs)

    def select(self, *args, **kwargs):
        """
        execute select SQL and return unique result or list results(tuple).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.select(self.sql, *args, **kwargs)

    def select_one(self, *args, **kwargs):
        """
        Execute select SQL and return unique result(tuple), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.select_one(self.sql, *args, **kwargs)

    def query(self, *args, **kwargs):
        """
        Execute select SQL and return list results(dict).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.query(self.sql, *args, **kwargs)

    def query_one(self, *args, **kwargs):
        """
        execute select SQL and return unique result(dict), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.query_one(self.sql, *args, **kwargs)

    def do_execute(self, *args):
        """
        Execute sql return effect rowcount

        sql: insert into person(name, age) values(?, ?)  -->  args: ('张三', 20)
        """
        return self.executor.do_execute(None, self.sql, *args)

    def do_save_sql(self, select_key: str, *args):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param args:
        :return: Primary key
        """
        return self.executor.do_save_sql(select_key, self.sql, *args)

    def do_get(self, *args):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
        """
        return self.executor.do_get(self.sql, *args)

    def do_select(self, *args):
        """
        execute select SQL and return unique result or list results(tuple).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.executor.do_select(self.sql, *args)

    def do_select_one(self, *args):
        """
        Execute select SQL and return unique result(tuple), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
        """
        return self.executor.do_select_one(self.sql, *args)

    def do_query(self, *args):
        """
        Execute select SQL and return list results(dict).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.executor.do_query(self.sql, *args)

    def do_query_one(self, *args):
        """
        execute select SQL and return unique result(dict), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
        """
        return self.executor.do_query_one(self.sql, *args)

    def batch_execute(self, *args):
        """
        Batch execute sql return effect rowcount

        sql: insert into person(name, age) values(?, ?)  -->  args: [('张三', 20), ('李四', 28)]

        :param args: All number must have same size.
        :return: Effect rowcount
        """
        return self.executor.batch_execute(self.sql, *args)

    def load(self, *args, **kwargs) -> Loader:
        """
        sqlexec.sql('select id, name, age from person WHERE name = :name').load(name='张三')
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name = :name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.load(self.sql, *args, **kwargs)

    def do_load(self, *args) -> Loader:
        """
        sqlexec.sql('select id, name, age from person WHERE name = ?').do_load('张三')
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.executor.do_load(self.sql, *args)

    def param(self, *args, **kwargs) -> Param:
        """
        sqlexec.sql('select id, name, age from person WHERE name = :name').param(name='张三')
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name = :name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return Param(self, *args, **kwargs)


def sql(sql_text: str) -> SqlExec:
    sql_text = sql_text.strip()
    assert sql_text, "Parameter 'sql' must not be none"
    return SqlExec(sql_text, exec)
