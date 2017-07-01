from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer , primary_key=True)
    username = Column(String(20), unique=True , index=True)
    password = Column(String(10))
    email = Column(String(50), index=True)
    registered_on = Column(DateTime, default=datetime.datetime.utcnow)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class OauthUser(Base):
    __tablename__ = 'oauth_user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(120), nullable=True)
    # password = Column(String(120), nullable=True)
    picture = Column(String(250))


class Catalog(Base):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    oauth_user_id = Column(Integer, ForeignKey('oauth_user.id'))
    oauth_user = relationship(OauthUser)
    users_id = Column(Integer, ForeignKey('user.id'))
    users = relationship(User)
    menu_item = relationship('MenuItem', cascade='all,delete', backref='catalog')

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }

class MenuItem(Base):
    __tablename__ = 'menu_item'


    title =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    oauth_user_id = Column(Integer, ForeignKey('oauth_user.id'))
    oauth_user = relationship(OauthUser)
    users_id = Column(Integer, ForeignKey('user.id'))
    users = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'title'         : self.title,
           'description'         : self.description,
           'id'         : self.id,
       }



engine = create_engine('sqlite:///catalogmenu.db')


Base.metadata.create_all(engine)
