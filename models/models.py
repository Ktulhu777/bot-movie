from datetime import datetime
from sqlalchemy import Column, String, Integer, TIMESTAMP, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    """Таблица пользователя"""
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    telegram_user_id: int = Column(BigInteger)
    date_added: datetime.utcnow = Column(TIMESTAMP, default=datetime.utcnow())


class Movie(Base):
    __tablename__ = "movies"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    movie_code: int = Column(Integer, unique=True)
    title: str = Column(String)
    date_added: datetime.utcnow = Column(TIMESTAMP, default=datetime.utcnow())


class Admin(Base):
    __tablename__ = "admins"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_super_user: int = Column(BigInteger)
