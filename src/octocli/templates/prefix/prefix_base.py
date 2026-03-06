from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from ..settings import SettingsPrefix


class PrefixDeclarativeBase(DeclarativeBase):
    pass


class PrefixBase(PrefixDeclarativeBase):
    __abstract__ = True
    _the_prefix = SettingsPrefix().table_prefix

    @declared_attr
    def __tablename__(cls):
        return cls._the_prefix + cls.__incomplete_tablename__  # pyright: ignore

    def asdict(self) -> dict:
        return {col.key: getattr(self, col.key) for col in self.__table__.columns}
