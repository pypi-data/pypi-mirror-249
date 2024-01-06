
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

DbEnginePool = dict()
DbBaseDeclPool = dict()


def get_db_engine(db_url, bind_name="default",
                  pool_size=5,
                  pool_timeout=60,
                  max_overflow=-1,
                  **engine_options
                  ):
    """
    :param max_overflow: The maximum overflow size of the
          pool. When the number of checked-out connections reaches the
          size set in pool_size, additional connections will be
          returned up to this limit. When those additional connections
          are returned to the pool, they are disconnected and
          discarded. It follows then that the total number of
          simultaneous connections the pool will allow is pool_size +
          `max_overflow`, and the total number of "sleeping"
          connections the pool will allow is pool_size. `max_overflow`
          can be set to -1 to indicate no overflow limit; no limit
          will be placed on the total number of concurrent
          connections. Defaults to 10.

    :return: connectable engine
    """
    # ;;'sqlite:///:memory:'
    global DbEnginePool
    dbe = DbEnginePool.get(db_url, None)
    if dbe is None:
        dbe = create_engine(
            db_url,
            pool_size=pool_size,
            pool_timeout=pool_timeout,
            max_overflow=max_overflow,
            **engine_options
        )
        DbEnginePool[db_url] = dbe
        DbEnginePool[bind_name] = dbe
    return dbe


def get_db_base(db_url, bind_name="default", engine=None):
    """
    ; modify global copy of databases for global instances usage
    ; to create only one instance per python interpreter usage
    :param db_url: str
    :return: DatabaseSession
    """
    global DbBaseDeclPool
    # ;;'sqlite:///:memory:'
    dbBase = DbBaseDeclPool.get(db_url, None)
    if dbBase is None:
        dbBase = declarative_base(
            name=bind_name
        )
        DbBaseDeclPool[db_url] = dbBase
        DbBaseDeclPool[bind_name] = dbBase
        # dbBase.metadata.create_all(engine)
        dbBase.engine = dbBase
        setattr(dbBase, "_decl_class_registry", {})
    return dbBase


def register_db_base(dbModel, dbDeclBase, InterfaceModel=None, **kw):
    ##; 创建一个新类，它继承自 dbBaseDecl + InterfaceModel
    db_name = dbModel.__name__
    new_dct = dict(
        dbModel.__dict__, **kw,
        __abstract__=True,
        # _sa_class_manager=None,
        # __mapper__=None,
    )
    _saman = dbModel.__dict__.get("_sa_class_manager", None)
    cls_pars = [dbDeclBase]
    if isinstance(InterfaceModel, (tuple, list)):
        cls_pars.extend(InterfaceModel)
    elif isinstance(InterfaceModel, type):
        cls_pars.append(InterfaceModel)
    elif InterfaceModel is None:
        pass
    else:
        raise TypeError("Invalid BaseClass:", InterfaceModel)
    new_cls = DeclarativeMeta(dbModel.__name__, tuple(cls_pars), new_dct)
    tbl_name = getattr(new_cls, "__tablename__", None)
    ##; 注册类到一个中央注册表，这里简单地将它们注册到 Base 的 _decl_class_registry
    if tbl_name:
        dbDeclBase._decl_class_registry[db_name] = dbModel
        dbDeclBase._decl_class_registry[tbl_name] = new_cls
    return new_cls


@contextmanager
def db_session_maker(auto_commit=False, auto_close=True, db_sess=None, db_engine=None, with_scope=True):
    """
    :param auto_commit: bool 
    :param auto_close: bool 
    :param db_engine: 
            <class 'sqlalchemy.engine.base.Engine'>,
    ;:param db_sess:
     
    :return: 
    """
    ### db.engine
    if db_sess is None:
        SessionFactory = orm.sessionmaker(bind=db_engine)
        if with_scope:
            db_sess = orm.scoped_session(SessionFactory)  # type: orm.scoped_session
        else:
            db_sess = SessionFactory()  # type: orm.Session
    elif db_sess.bind is None:
        db_sess.bind = db_engine
    try:
        yield db_sess
        if auto_commit:
            db_sess.commit()
    except Exception as e:
        print(e)
        db_sess.rollback()
        raise e
    finally:
        if auto_close:
            db_sess.close()


def db_conn_execute(sql_text, db_engine):
    with db_engine.connect() as db_conn:
        try:
            res = db_conn.execute(sa.text(sql_text))  # noqa
            return True, res
        except Exception as e:
            return False, e
