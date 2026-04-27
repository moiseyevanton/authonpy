from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base


class Employer(Base):
    __tablename__ = "employers"
    ID_employer = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)


class Store(Base):
    __tablename__ = "stores"
    ID_store = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    ID_employer = Column(Integer, ForeignKey("employers.ID_employer"))


class Administrator(Base):
    __tablename__ = "administrators"
    ID_administrator = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    ID_employer = Column(Integer, ForeignKey("employers.ID_employer"))


class Worker(Base):
    __tablename__ = "workers"
    ID_worker = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    ID_store = Column(Integer, ForeignKey("stores.ID_store"))
    ID_administrator = Column(Integer, ForeignKey("administrators.ID_administrator"))


class AdministratorStore(Base):
    __tablename__ = "administrator_store"
    ID_administrator = Column(Integer, ForeignKey("administrators.ID_administrator"), primary_key=True)
    ID_store = Column(Integer, ForeignKey("stores.ID_store"), primary_key=True)