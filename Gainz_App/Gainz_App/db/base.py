from sqlalchemy.orm import DeclarativeBase

from Gainz_App.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
