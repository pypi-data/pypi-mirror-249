"""
require:
    pymysql
"""
from contextlib import contextmanager
from urllib.parse import urlparse
from urllib.parse import parse_qsl
import pymysql


def parse_mysql_uri(db_uri: str):
    # @db_uri: eg "mysql://username:password@host:3306/database"
    parsed_uri = urlparse(db_uri)
    query_dict = dict(parse_qsl(parsed_uri.query))
    return dict(
        user=parsed_uri.username,
        password=parsed_uri.password,
        database=parsed_uri.path[1:],  ## ignore '/'
        host=parsed_uri.hostname,
        port=parsed_uri.port if parsed_uri.port else 3306,
        charset=query_dict.get("charset", "utf8mb4")
    )


@contextmanager
def db_cursor_maker(db_uri, auto_commit=True, auto_close=True):
    """
    :param db_uri: eg "mysql://username:password@host:3306/database"
    ##; pysql的cursor事务不会自动提交。
    ##; 上下文管理器确保了光标的正确关闭和异常处理，但并不处理事务提交。
    ##; 需要在执行事务后，显式地调用 commit() 方法。
    """
    options = parse_mysql_uri(db_uri)
    connection = pymysql.connect(**options)
    ##; 这个不适合于 执行多个操作作为一个单一事务时
    ## connection.autocommit(True)
    try:
        with connection.cursor() as cursor:
            ##; usage sample
            # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            # cursor.execute(sql, ('webmaster@python.org',))
            # result = cursor.fetchone()
            # print(result)
            ##; 在 pymysql中，并没有一个官方的、文档化的方式来从光标直接获取连接对象
            setattr(cursor, "connection", connection)
            yield cursor

        if auto_commit:
            connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

    finally:
        if auto_close:
            connection.close()
