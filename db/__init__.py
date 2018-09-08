
import os
import random
import string

import sqlalchemy
from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base
from .models import init_models


class DB(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config):
        self.config = config
        self.model = declarative_base()
        self.engine = create_engine(self.config.dburi)
        self.session = orm.sessionmaker(bind=self.engine, autocommit=True)()
        init_models(self)

    def create_all(self):
        self.model.metadata.create_all(self.engine)
