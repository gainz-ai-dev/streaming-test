from sqlalchemy.orm import DeclarativeBase

from gainz.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
