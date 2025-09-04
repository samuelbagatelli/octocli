from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, BigInteger, DateTime, TextClause
from sqlalchemy.orm import Mapped, mapped_column

from ..prefix import PrefixBase
from ..settings import SettingsEngine


class User(PrefixBase):
    __incomplete_tablename__ = "user"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=TextClause("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=TextClause(SettingsEngine().get_updated_at()),
    )
    deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=TextClause("FALSE"),
    )
    
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
      return f"<User(id={self.id})>"

    def keys(self) -> list[str]:
      return [column.key for column in self.__table__.columns]

    def __getitem__(self, key) -> Any:
      return getattr(self, key)
