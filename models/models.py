from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.sql import func
from db.db import Base


class Employer(Base):
    __tablename__ = "employers"
    ID_employer = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
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
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    ID_employer = Column(Integer, ForeignKey("employers.ID_employer"))


class Worker(Base):
    __tablename__ = "workers"
    ID_worker = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    ID_store = Column(Integer, ForeignKey("stores.ID_store"))
    ID_administrator = Column(Integer, ForeignKey("administrators.ID_administrator"))


class AdministratorStore(Base):
    __tablename__ = "administrator_store"
    ID_administrator = Column(Integer, ForeignKey("administrators.ID_administrator"), primary_key=True)
    ID_store = Column(Integer, ForeignKey("stores.ID_store"), primary_key=True)


class UserIP(Base):
    __tablename__ = "user_ips"
    ID_ip = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), nullable=False)
    login_time = Column(DateTime(timezone=True), server_default=func.now())
    
    ID_employer = Column(Integer, ForeignKey("employers.ID_employer", ondelete="CASCADE", onupdate="CASCADE"))
    ID_administrator = Column(Integer, ForeignKey("administrators.ID_administrator", ondelete="CASCADE", onupdate="CASCADE"))
    ID_worker = Column(Integer, ForeignKey("workers.ID_worker", ondelete="CASCADE", onupdate="CASCADE"))

    __table_args__ = (
        CheckConstraint(
            '("ID_employer" IS NOT NULL AND "ID_administrator" IS NULL AND "ID_worker" IS NULL) OR '
            '("ID_employer" IS NULL AND "ID_administrator" IS NOT NULL AND "ID_worker" IS NULL) OR '
            '("ID_employer" IS NULL AND "ID_administrator" IS NULL AND "ID_worker" IS NOT NULL)',
            name="chk_one_user"
        ),
    )