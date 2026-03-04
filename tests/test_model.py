from pathlib import Path

import pytest
from _typeshed import FileDescriptorOrPath

from octocli.model import Model

# ─────────────────────────── FIXTURES ────────────────────────────────────────

SOURCE = """\
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
"""

# ─────────────────────────── detect_style ────────────────────────────────────


class TestModelCreate:
    def test_create_path_not_provided(self):
        model = Model("user")
        model.create()

        filepath = Path.cwd() / "models" / "user.py"
        assert filepath.exists()

    def test_create_specific_path(self):
        model = Model("user", Path("~/cpid/courses/"))
        model.create()

        filepath = Path.home() / "cpid" / "courses" / "models" / "user.py"
        assert filepath.exists()
