
import re
import json
import datetime
from collections import OrderedDict

from . import exceptions
from .templates import get_template


def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return str(obj)


class Device(object):

    def __init__(self, **attrs):
        self.attrs = Attrs(attrs)
        self.template = None

    def init(self):
        if self.attrs.address is None:
            raise exceptions.AttrError('bad address')
        self.template = get_template(self.attrs)
        return self

    def __getattr__(self, item):
        if hasattr(self.template, item):
            return getattr(self.template, item)
        if self.attrs.hasattr(item):
            return getattr(self.attrs, item)
        raise AttributeError("'%s' object has no attribute '%s'" % \
            (self.__class__.__name__, item))

    def __repr__(self):
        return json.dumps(self.to_dict(), default=json_serial)

    def to_dict(self):
        return {
            **self.attrs.to_dict(),
            **{'log': self.adapter.get_log() if self.adapter else None}
        }



class Attrs(object):

    def __init__(self, attrs={}):
        self._address = None
        self._username = None
        self._password = None
        self._model = None
        self._vendor = None
        self._attrs = OrderedDict()
        for attr, value in attrs.items():
            attr = attr.strip().lower()
            if attr in dir(self):
                setattr(self, attr, value)
            else:
                self._attrs[attr] = value

    def __getattr__(self, item):
        if item in dir(self):
            return getattr(self, item)
        return self._attrs.get(item)

    def to_dict(self):
        return {
            'address': self.address.__str__(),
            'vendor': self.vendor,
            'model': self.model,
            'attrs': dict(self._attrs),
        }

    def hasattr(self, item):
        if item in dir(self): return True
        if item in self._attrs: return True
        return False

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value.strip() if value else None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value.strip() if value else None

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value.strip() if value else None

    @property
    def vendor(self):
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        self._vendor = value.strip().lower() if value else None

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value.strip().lower() if value else None
