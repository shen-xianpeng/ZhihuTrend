# -*- coding: utf-8 -*-
from db import Base

from db import engine

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer


class User(Base):
    ''' 用户 '''
    __tablename__ = "user"

    id                 = Column(String(100), primary_key=True)
    name               = Column(String(80), unique=True)
    avatar             = Column(String(1000))
    description        = Column(String(1000))
    follower           = Column(Integer())
    def as_dict(self):
        return dict(
            id          = self.id,
            name        = self.name,
            avatar      = self.avatar or "",
        )