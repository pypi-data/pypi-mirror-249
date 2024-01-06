"""
require:
    pyco_sqlalchemy(current)
"""
import re
import json
from datetime import datetime
from collections import OrderedDict
from sqlalchemy import types as sqltypes

__package__ = "pyco_sqlalchemy"

from . import utils
from . import regex
from ._errors import PycoSqlError

##; 兼容旧代码
types = sqltypes
CustomParameterError = PycoSqlError(errno=40071)
PycoSqlColumnError = PycoSqlError(errno=40072)


class EnumInt(sqltypes.TypeDecorator):
    impl = sqltypes.SmallInteger
    cache_ok = True

    @property
    def python_type(self):
        return int

    def process_bind_param(self, value, dialect):
        return utils.parse_int(value, default_value=0)


class CoInt32(sqltypes.TypeDecorator):
    impl = sqltypes.Integer
    cache_ok = True

    @property
    def python_type(self):
        return int

    def process_bind_param(self, value, dialect):
        return utils.parse_int(value, default_value=0)

    def process_result_value(self, value, dialect):
        return utils.parse_int(value, default_value=0)


class CoInt64(sqltypes.TypeDecorator):
    impl = sqltypes.BigInteger
    cache_ok = True

    @property
    def python_type(self):
        return int

    def process_bind_param(self, value, dialect):
        return utils.parse_int(value, default_value=0)

    def process_result_value(self, value, dialect):
        return utils.parse_int(value, default_value=0)


class DateTime(sqltypes.TypeDecorator):
    """
    # sample 1:
    @declared_attr
    def created_time(self):
        return db.Column(DateTime, default=datetime.utcnow)
    ## note: DateTime 不校验时区, 使用`datetime.utcnow`容易得到错误的时间戳, 需要在后端业务代码重新处理 tz_offset

    # sample 2:
    updated_time = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)
    ## 如果有国际化需求, 建议使用时间戳替代日期, 或者统一使用 `DatetimeTZUtc`
    """
    impl = sqltypes.DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime):
            return value
        elif isinstance(value, str):
            return utils.parse_datestr(value)
        elif isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
        else:
            return value


class DateTimeTZLocal(sqltypes.TypeDecorator):
    """
    # sample 1:
    @declared_attr
    def created_time(self):
        return db.Column(DateTime, default=utils.now)

    # sample 2:
    updated_time = db.Column(DateTime, default=utils.now, onupdate=utils.now)
    """
    impl = sqltypes.DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return utils.parse_date(value, tz=utils.TZ_LOCAL)


class DatetimeTZUtc(sqltypes.TypeDecorator):
    impl = sqltypes.DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return utils.parse_date(value, tz=utils.TZ_UTC)


class BoolField(sqltypes.TypeDecorator):
    ##; NOTE: origin `sqltypes.Boolean` use _strict_bools = frozenset([None, True, False])
    impl = sqltypes.Boolean
    cache_ok = True
    ## @formatter:off
    BoolStrings = {
        ""     : False,
        "0"    : False,
        "false": False,
        "null" : False,
        "none" : False,
        "no"   : False,
        "n"    : False,
        "f"    : False,

        ### 支持部分英文单词语义化
        "error"  : False,
        "not_ok" : False,
        "not ok" : False,
        "invalid" : False,
        "incorrect" : False,
        "undefined" : False,

        ### 支持部分中文语义化
        "无"    : False,
        "否"    : False,
        "错"    : False,
        "空"    : False,
        "错误"    : False,
        "无效"    : False,
        "空白"    : False,
        # "1"    : True,
        # "true" : True,
        # "yes"  : True,
        # "ok"   : True,
        # "y"    : True,
        # "t"    : True,
    }
    ## @formatter:on
    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            v = value.strip().lower()
            return self.BoolStrings.get(v, True)
        else:
            return bool(value)


class TrimString(sqltypes.TypeDecorator):
    impl = sqltypes.String
    cache_ok = True

    def __init__(self, *args, collation='utf8mb4_general_ci', default="", **kwargs):
        self._default_value = default
        # super().__init__(*args, collation=collation, **kwargs)
        super(TrimString, self).__init__(*args, collation=collation, **kwargs)
        self.collation = collation

    def process_bind_param(self, value, dialect):
        if value is None:
            return ""
        elif not isinstance(value, str):
            print(f"[INFO] TrimString: {type(value)} => {value}")
            return str(value)
        value = value.strip()
        if len(value) > self.impl.length:
            print(f"[WARN] TrimString: {value}[-{self.impl.length}:{len(value)}]")
            value = value[-self.impl.length:]
        return value

    def process_result_value(self, value, dialect):
        if not value:
            return self._default_value
        return value.strip()


class LabelString(TrimString):
    """
    ##; MySQL数据库的varchar类型在5.0.3以下的版本中的最大长度限制为255，其数据范围可以是0~255。
    ##; 在MySQL5.0.3及以上的版本中，varchar数据类型的长度支持到了65535，也就是说可以存放65532个字节的数据，起始位和结束位占去了3个字节
    ###; 不允许用分隔符","
    """
    impl = sqltypes.String
    cache_ok = True
    _reserved_chars = (",",)
    _safety_char = "|"

    def __init__(self, *args, collation='utf8mb4_general_ci', default="", reserved_chars=_reserved_chars, **kwargs):
        self._default_value = default
        self._reserved_chars = reserved_chars
        super().__init__(*args, collation=collation, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is None:
            return ""
        elif not isinstance(value, str):
            print(f"[INFO] LabelString: {type(value)} => {value}")
            return str(value)
        assert isinstance(value, str)
        if len(value) > self.impl.length:
            print(f"[WARN] TrimString: {value}[-{self.impl.length}:{len(value)}]")
            value = value[-self.impl.length:]
        for c in self._reserved_chars:
            value = value.replace(c, self._safety_char)
        return value


class UkeyField(sqltypes.TypeDecorator):
    ##; CHAR:  0-255
    impl = sqltypes.CHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return utils.ts_rnd_key(4)
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, str):
            return regex.snake_case(str(value))
        else:
            raise CustomParameterError(f"invalid ${type(value)}:'{value}', Column<UkeyField> require [0-9a-zA-Z_]")


class SnakeField(sqltypes.TypeDecorator):
    impl = sqltypes.String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return ""
        elif isinstance(value, (str, int)):
            return regex.snake_case(str(value))
        else:
            raise PycoSqlColumnError(f"invalid ${type(value)}:'{value}', Column<SnakeField> require [0-9a-zA-Z_]")


class RegexField(sqltypes.TypeDecorator):
    ##; CHAR:  0-255
    impl = sqltypes.CHAR
    cache_ok = True
    _regex_patten = "*"

    def __init__(self, regex=_regex_patten, collation='utf8mb4_general_ci', **kwargs):
        super().__init__(**kwargs)
        self.collation = collation
        self._regex_patten = regex

    def process_bind_param(self, value, dialect):
        if not value or not isinstance(value, str):
            raise PycoSqlError(
                msg=f"invalid ${type(value)}:'{value}', require [{self._regex_patten}]",
                errno=40074,
            )

        m = re.match(self._regex_patten, value)
        if not m:
            raise PycoSqlError(
                msg=f"invalid ${type(value)}:'{value}', unmatch [{self._regex_patten}]",
                errno=40075,
            )
        return value


class VersionField(sqltypes.TypeDecorator):
    ##; CHAR:  0-255
    impl = sqltypes.CHAR
    cache_ok = True
    _regex_patten = "\d+(?:\.\d+)*"

    def __init__(self, regex=_regex_patten, collation='utf8mb4_general_ci', **kwargs):
        super().__init__(**kwargs)
        self.collation = collation
        self._regex_patten = regex


class StringTags(sqltypes.TypeDecorator):
    impl = sqltypes.String
    cache_ok = True
    _char_sep = ","

    def __init__(self, sep=",", default="", **kwargs):
        super().__init__(**kwargs)
        self._char_sep = sep
        self._default_value = default

    def process_bind_param(self, value, dialect):
        if value and isinstance(value, str):
            return self._char_sep.join(map(lambda x: x.strip(), value.split(self._char_sep)))
        if isinstance(value, (list, tuple, set)):
            return self._char_sep.join(map(str, value))
        return self._default_value

    def process_result_value(self, value, dialect):
        if value:
            if isinstance(value, str):
                return value.split(self._char_sep)
            elif isinstance(value, (list, tuple, set)):
                return value
            else:
                return [value]
        else:
            return []


class StringTagsSnaked(StringTags):
    def process_bind_param(self, value, dialect):
        vs = super().process_bind_param(value, dialect)
        ks = []
        for v in vs:
            v2 = regex.snake_case(str(v))
            if v2 and (v2 not in ks):
                ks.append(v2)
        return self._char_sep.join(ks)


################################
## JSON Text


class JsonText(sqltypes.TypeDecorator):
    impl = sqltypes.Text
    cache_ok = True

    def __init__(self, collation='utf8mb4_general_ci', **kwargs):
        super().__init__(**kwargs)
        self.collation = collation

    def process_bind_param(self, value, dialect):
        if value is None:
            return ""
        elif isinstance(value, str):
            return value
        return utils.json_dumps(value)

    def process_result_value(self, value, dialect):
        return utils.parse_json(value)


class JsonTextDict(JsonText):
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        elif value == "":
            return {}
        else:
            return utils.parse_json(value)


class JsonTextOrdered(sqltypes.TypeDecorator):
    impl = sqltypes.Text
    cache_ok = True
    json_encoder = utils.BaseJSONEncoder()
    json_decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

    def process_bind_param(self, value, dialect):
        return self.json_encoder.encode(value)

    def process_result_value(self, value, dialect):
        return self.json_decoder.decode(value)


################################
## JSON 
class MyJSON(sqltypes.TypeDecorator):
    # NOTE: actually it supports `sqltypes.JSON`
    # NOTE: failed if use `impl = _asJsonImpl`
    # https://docs.sqlalchemy.org/en/13/core/custom_types.html#sqlalchemy.types.TypeDecorator
    impl = sqltypes.JSON
    cache_ok = True

    def process_bind_param(self, value, dialect):
        # NOTE: double-encoded if return string
        # value 可能含有日期等类型的字段, 所以需要先 json_format
        return utils.parse_json(utils.json_dumps(value, indent=0))


class SortedTagsArray(sqltypes.TypeDecorator):
    impl = sqltypes.JSON
    cache_ok = True
    _char_sep = ","

    def __init__(self, sep=",", **kwargs):
        super().__init__(**kwargs)
        self._char_sep = sep

    def process_bind_param(self, value, dialect):
        if isinstance(value, (list, tuple, set)):
            return sorted(set(map(str, value)))
        elif isinstance(value, str):
            return sorted(set(map(lambda x: x.strip(), value.split(self._char_sep))))
        elif not value:
            return []
        else:
            return [str(value)]


class OrderedJson(sqltypes.TypeDecorator):
    impl = sqltypes.JSON
    cache_ok = True
    json_decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

    def process_result_value(self, value, dialect):
        if isinstance(value, str):
            return self.json_decoder.decode(value)
        return value


class JsonList(sqltypes.TypeDecorator):
    impl = sqltypes.JSON
    cache_ok = True

    def process_bind_param(self, value, dialect):
        v = utils.parse_json(value)
        if not v:
            return []
        if not isinstance(v, list):
            msg = f'{self.__class__.__name__}:invalid ${type(value)}:"{value}"'
            raise PycoSqlError(msg, errno=40005)
        return v

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        elif value == "":
            return []

        vs = utils.parse_json(value)
        if not isinstance(vs, list):
            return [vs]
        return vs


class JsonIntArray(JsonList):
    impl = sqltypes.JSON
    cache_ok = True

    def process_result_value(self, value, dialect):
        vs = super(JsonIntArray, self).process_result_value(value, dialect)
        us = list(map(utils.parse_int, vs))
        return us
