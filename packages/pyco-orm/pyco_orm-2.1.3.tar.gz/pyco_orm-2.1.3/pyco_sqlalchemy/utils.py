"""
require:
    python-dateutil>=2.8.0
"""
import json
import uuid
import time
import random
from pprint import pformat
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse as parse_datestr

TZ_UTC = timezone.utc
TZ_LOCAL = timezone(timedelta(seconds=-time.timezone))
simple_lowercase = 'abcdefghjkmnpqrstuvwxy'  # !loiz


def now(tz=None):
    ##; 使用datetime.now, 使得到的日期, 不管时间区是多少, 时间戳都是一致的.
    ##; 返回等同于: datetime.utcnow().replace(tz_info=TZ_UTC)
    ##; eg: now(TZ_UTC).timestamp() == now(TZ_LOCAL).timestamp())
    if not tz:
        tz = TZ_LOCAL
    return datetime.now(tz=tz)


def NowStr(fmt="%Y%m%d_%H%M%S"):
    return now().strftime(fmt)


def ts_rnd_key(size=4, fmt="%-y%m%d%H%M%S"):
    tag = datetime.now().strftime(fmt)
    rnd = ''.join(random.choice(simple_lowercase) for i in range(size))
    return f'{tag}{rnd}'


K_ParseStr2Int_base_map = {
    "default": 10,
    "0o": 8,
    "0O": 8,
    "0b": 2,
    "0B": 2,
    "0x": 16,
    "0X": 16,
    "0+": 36,  ##; 36进制自定义的前缀:[0-10]+[a/A-z/Z] 不区分大小写
    "0|": 36,  ##; 36进制自定义的前缀:[0-10]+[a/A-z/Z] 不区分大小写
    ##; python int base [2, 36]
    "0#": 62,  ##; 62进制自定义的前缀:[0-10]+[AZ]+[az] 区分大小写
    "0&": 62,  ##; 62进制自定义的前缀:[0-10]+[AZ]+[az] 区分大小写
}


def parse_int(value, default_value=0):
    if isinstance(value, int):
        return value
    elif isinstance(value, float):
        return int(value)
    elif value is True:
        return 1
    elif value is False:
        return 0
    elif value:
        if isinstance(value, str):
            p = value[:2]
            base = K_ParseStr2Int_base_map.get(p, 10)
            v = int(value, base)
            return v
        else:
            v = int(value)
            return v
    else:
        return default_value


def parse_date(val, nullable=True, tz=TZ_LOCAL, **parse_kws):
    v = None
    if isinstance(val, datetime):
        v = val.timestamp()
    elif isinstance(val, str):
        v = parse_datestr(val, **parse_kws).timestamp()
    elif isinstance(val, (int, float)):
        v = val

    if v:
        return datetime.fromtimestamp(v, tz=tz)
    elif nullable:
        return None
    raise ValueError(f"Unknown DateValue{val}")


def parse_json(data):
    if isinstance(data, str) and data.startswith('"') and data.endswith('"'):
        try:
            obj = json.loads(data)
            return obj
        except:
            return data
    else:
        return data


class BaseJSONEncoder(json.JSONEncoder):
    jsonify_handles = [
        ""
    ]

    @classmethod
    def stringify(cls, obj, strict=False):
        if isinstance(obj, datetime):
            # default use TZ-LOCAL, eg: "2021-03-22 20:32:02.271068+08:00"
            return str(obj.astimezone())
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif hasattr(obj, 'to_json') and callable(obj.to_json):
            return obj.to_json()
        elif hasattr(obj, 'to_dict') and callable(obj.to_dict):
            return obj.to_dict()
        elif hasattr(obj, 'json'):
            if callable(obj.json):
                return obj.json()
            else:
                return obj.json

        text = pformat(obj, indent=2)
        msg = f"{type(obj)}::{text}"
        if not strict:
            return msg
        else:
            raise TypeError(f"BaseJSONEncoder: Object is not serializable. \n{msg}")

    def default(self, obj):
        return self.stringify(obj, strict=True)


###
def json_dumps(data, indent=2, autoflat=True, cls=BaseJSONEncoder, ensure_ascii=False, **kwargs):
    if isinstance(data, str) and autoflat:
        data = parse_json(data)
    return json.dumps(
        data, indent=indent,
        cls=cls, ensure_ascii=ensure_ascii, **kwargs
    )


##; json_stringify 总能返回字符串结果, 不会抛出 TypeError
json_stringify = lambda obj: json.dumps(obj, indent=2, default=BaseJSONEncoder.stringify)
