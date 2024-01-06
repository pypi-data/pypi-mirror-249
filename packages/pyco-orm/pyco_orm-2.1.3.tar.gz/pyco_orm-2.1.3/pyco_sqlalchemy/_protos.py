"""
require:
    sqlalchemy
"""
import os
import logging
import datetime as DT
from pprint import pformat
from contextlib import contextmanager
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.schema import Column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.attributes import InstrumentedAttribute, flag_modified
from ._errors import PycoSqlError
from ._types import DateTimeTZLocal, BoolField
from ._base import db_session_maker


class BaseModel():
    __table_args__ = {
        "mysql_collate": "utf8mb4_general_ci",
        "extend_existing": True,
    }
    _primary_column = None
    _X_COL_EXTRA_JSON = "extra_json"  ##; 用来装载非结构化字段的 虚属性
    _X_BIND_SESSION = None
    ##; fields_map: {column_name: alias_name} 
    fields_map = None


    def __init__(self, extra_json=None, **init_kws):
        self.__init_kws = init_kws
        self.__extra_json = extra_json

    @classmethod
    def tablename(cls):
        m = getattr(cls, "__tablename__", cls.__name__)
        return m

    @classmethod
    def _db_session(cls):
        ##; 子类必须实现此功能
        raise NotImplementedError


    @classmethod
    def columns(cls):
        tbl = getattr(cls, "__table__", None)
        if tbl is None:
            name = cls.__name__
            desc = 'Service Unavailable: DbModel<{}> '.format(name)
            msg = "ORM-ERROR:{}\nDbModel<{}> must be subclass of db.Model!".format(desc, name)
            raise PycoSqlError(msg, code="pyco:columns")
        else:
            return tbl.columns

    @classmethod
    def primary_keys(cls):
        tbl = cls.__table__
        pks = [m.name for m in tbl.primary_key.columns]
        return pks

    @classmethod
    def primary_column(cls):
        if cls._primary_column is None:
            col_id = getattr(cls, "id")
            if isinstance(col_id, InstrumentedAttribute):
                cls._primary_column = col_id
            else:
                pk = cls.primary_keys()[0]
                col_pk = getattr(cls, pk)
                cls._primary_column = col_pk
        return cls._primary_column


    @classmethod
    def _immutable_keys(cls):
        # limit columns should not updated by cls.update(form)
        pks = cls.primary_keys()
        return pks

    @classmethod
    def _is_extra_kv(cls, k, v):
        return not k.startswith("_") and not k.startswith(".") and not callable(v)

    @classmethod
    def _dispart_extras(cls, _data: dict, extra_json=None, **kwargs):
        ##; 使用 _data 可以避免有column_name 设置为 "data"
        form = {}
        if extra_json is None:
            extra_json = {}
        if isinstance(_data, dict):
            kwargs.update(_data)
        _extra = _data.pop(cls._X_COL_EXTRA_JSON, {})
        if isinstance(_extra, dict):
            extra_json.update(_extra)
        for k, v in kwargs.items():
            col = getattr(cls, k, None)
            if isinstance(col, (InstrumentedAttribute, Column)):
                form[k] = v
            elif cls._is_extra_kv(k, v):
                # print("_dispart_extras", cls.__name__, k, v, col.__class__)
                extra_json[k] = v
        return form, extra_json

    @classmethod
    def _convert_fields(cls, data: dict, nullable=False, use_column_name=False, _ignore_case=True):
        ##; 因为业务需求，有时前端接口要求返回的字段可能不满足 python 或 MySQL 的命名规范
        cv = {}
        if not cls.fields_map:
            return cv
        if isinstance(cls.fields_map, dict):
            fields_alias_pairs = list(cls.fields_map.items())
        elif isinstance(cls.fields_map, tuple):
            fields_alias_pairs = cls.fields_map
        else:
            raise TypeError(f"assert isinstance(cls.fields_map, (tuple, dict)), but recieve {type(cls.fields_map)}")

        seed = dict((k.lower(), v) for k, v in data.items())

        # for col_name, alias_name in fields_alias_pairs:
        for col_name, alias_name in fields_alias_pairs:
            if use_column_name:
                key, ref = alias_name, col_name
            else:
                key, ref = col_name, alias_name
            v0 = data.pop(key, None)
            v1 = data.get(ref, None)
            if v1 is not None:
                cv[ref] = v1
            elif v0 is not None:
                cv[ref] = data.setdefault(ref, v0)
            else:
                if _ignore_case:
                    v2 = seed.get(key.lower(), None)
                    if v2 is not None:
                        cv[ref] = data.setdefault(ref, v2)
                if not nullable and data.get(ref) is None:
                    raise ValueError(f"require field ${ref}(${key})")
        return cv

    def inspect_relations(self):
        kws = {}
        for key in sa.inspect(self.__class__).relationships.keys():
            if key in self.__dict__:
                kws.setdefault(key, self.__getattribute__(key))
        return kws

    @classmethod
    def strict_form(cls, _data=None, nullable=True, **kwargs):
        if isinstance(_data, dict):
            kwargs.update(_data)
        form = {}
        for k, v in kwargs.items():
            col = getattr(cls, k, None)
            if isinstance(col, (InstrumentedAttribute, Column)):
                if v is None:
                    if nullable:
                        form[k] = v
                elif isinstance(v, (str, int, bool, float, DT.datetime, DT.date, DT.timedelta)):
                    form[k] = v
        return form
        
    @classmethod
    def initial(cls, _data=None, **kwargs):
        form, extra_json = cls._dispart_extras(_data, **kwargs)
        m = cls(**form)
        
        return m

    @classmethod
    def initial_entity(cls, data):
        if isinstance(data, cls):
            return data
        elif isinstance(data, dict):
            return cls.initial(data)
        elif callable(getattr(data, "_asdict", None)):
            ## sqlalchemy.util._collections.result object
            return cls.initial(data._asdict())
        elif isinstance(data, list) and len(data) == 1:
            return cls.initial_entity(data[0])
        else:
            msg = f"UnknownEntity:<{cls.__name__}>:{type(data)}, {data}"
            raise ValueError(msg)


    @classmethod
    def _db_qry(cls, _db_session=None):
        if _db_session is None:
            qry = getattr(cls, "query", None)
            if isinstance(qry, sa.orm.Query):
                return qry
        if isinstance(_db_session, sa.orm.scoping.scoped_session):
            ##; flask-sqlalchemy session
            qry = _db_session.query(cls)
        elif isinstance(_db_session, sa.orm.session.Session):
            qry = _db_session.query(cls)
        else:
            qry = cls._db_session().query(cls)
        return qry  # type: sa.orm.Query

    @classmethod
    def insert(cls, data=None, **kwargs):
        m = cls.initial(data, **kwargs)
        m.save()
        return m

    @classmethod
    def _filter_query(cls, filter_condition=None, _db_query=None, _db_session=None,
                      limit=-1, offset=0, order_by=None, _auto_strict=False, nullable=True,
                      condition=None, **condition_kws
                      ):
        if _db_query is None:
            qry = cls._db_qry(_db_session)
        else:
            qry = _db_query
        if isinstance(filter_condition, dict):
            qry = qry.filter_by(**filter_condition)
        elif isinstance(filter_condition, (tuple, list)):
            ##; 默认为 AND
            qry = qry.filter(*filter_condition)
        elif isinstance(filter_condition, sa.sql.ClauseElement):
            qry = qry.filter(filter_condition)

        if isinstance(condition, dict):
            condition_kws.update(condition)
        if condition_kws:
            if _auto_strict:
                form = cls.strict_form(condition, **condition_kws, nullable=nullable)
                qry = qry.filter_by(**form)
            else:
                qry = qry.filter_by(**condition_kws)

        if isinstance(order_by, (list, tuple)):
            qry = qry.order_by(*order_by)
        elif order_by is not None:
            qry = qry.order_by(order_by)
        if limit > 0:
            qry = qry.limit(limit).offset(offset)
        return qry

    @classmethod
    def _convert_resobj(cls, _as_resobj=1, **kwargs):
        if _as_resobj == 1:
            return lambda d: cls.initial_entity(d)
        elif _as_resobj == 2:
            return lambda d: cls.initial_entity(d).to_dict(**kwargs)
        elif _as_resobj == 3:
            return lambda d: d.values()
        else:
            return lambda d: d

    @classmethod
    def select_many(cls, filter_condition=None, selected_columns=None, _as_resobj=1, _db_query=None, **_filter_kws):
        ##; resobj: {<0:noGen; 1;Entity; 2:Dict; 3:list; 其它:OrmResult}
        qry = cls._filter_query(filter_condition, _db_query=None, **_filter_kws)  # noqa; db.session.query(cls)
        if selected_columns is None:
            resGen = qry.all()
        else:
            resGen = qry.values(*selected_columns)

        if not _as_resobj or _as_resobj < 0:
            return resGen

        res = []
        resCvt = cls._convert_resobj(_as_resobj, **_filter_kws)
        for m1 in resGen:  ## type: sqlalchemy.util._collections.result
            m2 = resCvt(m1)
            res.append(m2)
        return res

    @classmethod
    def select_first(cls, filter_condition=None, *selected_columns, _as_resobj=1, _db_query=None):
        qry = cls._filter_query(filter_condition, _db_query=_db_query)
        resGen = qry.values(*selected_columns)
        resCvt = cls._convert_resobj(_as_resobj)
        for m in resGen:
            return resCvt(m)

    @classmethod
    def select_value(cls, filter_condition, column, _db_query=None):
        qry = cls._filter_query(filter_condition, _db_query=_db_query)
        return qry.value(column)


    @classmethod
    def _strict_query(cls, condition=None, limit=None, offset=None, order_by=None, _db_query=None, nullable=True,
                      **condition_kws
                      ):
        form = cls.strict_form(condition, **condition_kws, nullable=nullable)
        qry = cls.query.filter_by(**form)
        if isinstance(order_by, (list, tuple)):
            qry = qry.order_by(*order_by)
        elif order_by is not None:
            qry = qry.order_by(order_by)
        if isinstance(limit, int) and limit >= 0:
            qry = qry.limit(limit)
            if isinstance(offset, int) and offset >= 0:
                qry = qry.offset(offset)
        return qry

    _make_query = _strict_query

    @classmethod
    def discard(cls, condition=None, limit=1, **condition_kws):
        # In Case of incorrect operation, default limit 1;
        condition = cls.strict_form(condition, **condition_kws)
        with db_session_maker(auto_commit=False) as db_sess:
            # n = cls.query.filter_by(**condition).delete()
            n = db_sess.query(cls).filter_by(**condition).delete()
            if limit > 0 and limit < n:
                db_sess.rollback()
                msg = "You're trying discard {} rows of {}, which is over limit={}".format(n, cls.__name__, limit)
                raise PycoSqlError(msg=msg, errno=50070, condition=condition)
            else:
                db_sess.commit()
            return n

    @classmethod
    def page_items(cls, condition=None, limit=10, offset=0, order_by=None, **condition_kws):
        qry = cls._make_query(condition, **condition_kws)
        pk = cls.primary_keys()[0]
        total = qry.value(func.count(getattr(cls, pk)))
        if isinstance(order_by, (list, tuple)):
            qry = qry.order_by(*order_by)
        elif order_by is not None:
            qry = qry.order_by(order_by)
        if limit > 0:
            items = qry.limit(limit).offset(offset).all()
        elif limit == 0:
            items = []
        else:
            items = qry.all()
        next_offset = offset + len(items)
        has_more = total > next_offset
        return dict(total=total, limit=limit, next_offset=next_offset, has_more=has_more, items=items)

    @classmethod
    def filter_by(cls, condition=None, **condition_kws):
        qry = cls._make_query(condition, **condition_kws)
        ms = qry.all()
        return ms

    @classmethod
    def count(cls, condition=None, **condition_kws):
        # https://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.count
        qry = cls._make_query(condition, **condition_kws)
        pk = cls.primary_keys()[0]
        qry = qry.value(func.count(getattr(cls, pk)))
        return qry

    @classmethod
    def get_or_none(cls, condition=None, **condition_kws):
        cond = cls.strict_form(condition, **condition_kws)
        return cls.query.filter_by(**cond).one_or_none()

    @classmethod
    def upsert_one(cls, condition: dict, **updated_kws):
        m = cls.get_or_none(condition)
        if isinstance(m, cls):
            m.update(updated_kws)
        else:
            m = cls.insert(condition, **updated_kws)
        return m

    def to_dict(self, **kwargs):
        d = dict(_type=self.__class__.__name__)
        columns = self.columns()
        for col in columns:
            name = col.name
            value = getattr(self, name)
            d[name] = value
        d.update(kwargs)
        return d

    def save(self):
        self._db_session().add(self)
        self._db_session().commit()

    def remove(self):
        self._db_session().delete(self)
        self._db_session().commit()


class CoModel(BaseModel):
    fields_map = dict(
        id="ID",
        created_time="CreatedTime",
        updated_time="UpdatedTime",
    )

    @declared_attr
    def created_time(self):
        return sa.Column(
            # sa.DateTime
            DateTimeTZLocal, default=DT.datetime.now, nullable=False,
            server_default=sa.text('CURRENT_TIMESTAMP')
        )

    @declared_attr
    def updated_time(self):
        return sa.Column(
            # sa.DateTime
            DateTimeTZLocal, default=DT.datetime.now, nullable=False,
            onupdate=DT.datetime.now,
            server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
        )


    @classmethod
    def lastOrNone(cls, **kwargs):
        order_by = kwargs.pop("order_by", cls.created_time.desc())
        qry = cls._make_query(kwargs, limit=1, order_by=order_by)
        return qry.one_or_none()

    @classmethod
    def lastOr404(cls, **kwargs):
        m = cls.lastOrNone(**kwargs)
        if isinstance(m, cls):
            return m
        msg = "Data Not Found: {}: {}".format(cls.__name__, pformat(kwargs))
        raise PycoSqlError(msg=msg, errno=40470, kwargs=kwargs)


class BlobModel(CoModel):
    """
    # 注意：dict{<python命名变量：API接口变量>}
    eg: fields_map = dict(
        created_time="CreatedTime",
        updated_time="UpdatedTime",
    )
    """
    fields_map = dict(
        id="ID",
        user_id="UserID",
        project_id="ProjectID",
        created_time="CreatedTime",
        updated_time="UpdatedTime",
        is_deleted="IsDeleted",
        extra_json="ExtraJson",
    )

    @declared_attr
    def is_deleted(self):
        # return db.Column(BoolField(), default=False, nullable=False)
        return sa.Column(BoolField(), default=False, nullable=False)

    @declared_attr
    def extra_json(self):
        # extra_json = deferred(db.Column(db.JSON, default=None))
        # extra_json = db.Column(db.JSON, default=None)
        return sa.orm.deferred(sa.Column(db.JSON, default=None))

    @classmethod
    def initial(cls, data=None, **kwargs):
        form = cls.strict_form(data, **kwargs)
        m = cls(**form)
        for col in cls.columns():
            v = getattr(m, col.name, None)
            if v is None and col.default:
                v = col.default.arg
                if not callable(v):
                    setattr(m, col.name, v)
                else:
                    ## debug default-value 
                    pass
                    # print(v)

        if hasattr(m, "user_id"):
            if not m.user_id:
                m.user_id = 0
        return m

    def to_dict(self, verbose=0, **kwargs):
        d = dict(_type=self.__class__.__name__)
        columns = self.columns()
        for col in columns:
            name = col.name  # type: str
            if verbose == 0 and name == "extra_json":
                pass
            else:
                value = getattr(self, name)
                d[name] = value
        d.update(kwargs)
        return d


class FlexModel(BlobModel):
    def to_dict(self, use_column_name=False, **kwargs):
        m = super().to_dict(**kwargs)
        self._convert_fields(m, nullable=True, use_column_name=use_column_name, _ignore_case=False)
        return m
