import json
import datetime
import sqlalchemy as sa
from sqlalchemy.ext.mutable import Mutable, MutableComposite


class TimeStamp(sa.types.TypeDecorator):
    impl = sa.types.DateTime
    LOCAL_TIMEZONE = datetime.datetime.now(datetime.UTC).astimezone().tzinfo

    def process_bind_param(self, value: datetime.datetime, dialect):
        if value is not None:
            if value.tzinfo is None:
                value = value.astimezone(self.LOCAL_TIMEZONE)

            return value.astimezone(datetime.timezone.utc)
        else:
            return value

    def process_result_value(self, value, dialect):
        if value is not None:
            if value.tzinfo is None:
                return value.replace(tzinfo=datetime.timezone.utc)

            return value.astimezone(datetime.timezone.utc)
        else:
            return value


class HexString(sa.types.TypeDecorator):
    impl = sa.types.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = value.hex()

        return value


class JSONEncodedDict(sa.types.TypeDecorator):
    impl = sa.types.Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value, ensure_ascii=False)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)

        return value


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


JSONType = MutableDict.as_mutable(JSONEncodedDict)


# 可以定义加密字段，自动的加密和解密，使用的密钥来自于外部的配置
class EncryptString(sa.types.TypeDecorator):
    impl = sa.types.String
    cache_ok = True

    def __init__(self, key):
        self.key = key

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = self.key.encrypt(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = self.key.decrypt(value)

        return value


class Point(MutableComposite):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __composite_values__(self):
        return self.x, self.y

    def __setattr__(self, name, value) -> None:
        object.__setattr__(self, key, value)

        self.changed()

    def __eq__(self, other) -> bool:
        return isinstance(other, Point) and other.x == self.x and other.y == self.y

    def __ne__(self, other):
        return not self.__eq__(other)


class Node(object):
    pass


class Edge(object):
    pass


class Viewport(object):
    pass


class Graph(Mutable, dict):

    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()
