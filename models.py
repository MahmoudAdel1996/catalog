import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, index=True)
    email = Column(String(250), nullable=False)
    picture = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'username': self.username,
            'id': self.id,
            'email': self.email,
            'picture': self.picture,
        }

class Store(Base):
    __tablename__ = 'stor'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    address = Column(String(250))
    picture = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'address': self.address,
            'picture': self.picture,
        }


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    productName = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    type_of = Column(String(250))
    picture = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'productName': self.productName,
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'type_of': self.type_of,
            'picture': self.picture
        }