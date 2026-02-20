from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, TextClause
from sqlalchemy.orm import Mapped, mapped_column

from ..prefix import PrefixBase


class {{ classname }}(PrefixBase):
    __incomplete_tablename__ = "{{ tablename }}"

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
        server_default=TextClause("CURRENT_TIMESTAMP"),
    )
    deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=TextClause("FALSE"),
    )
