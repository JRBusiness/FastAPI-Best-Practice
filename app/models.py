import datetime
import secrets

import pytz
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID

from app.shared.bases.base_model import ModelMixin, handle_transaction




class User(ModelMixin):
    """
    User represents a users in the database.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    api_key = Column(String, default=secrets.token_urlsafe(36))

    created = Column(DateTime, nullable=False, default=datetime.datetime.now(pytz.utc))
    completed_search_requests = Column(Integer, nullable=False, default=0)
    completed_reveal_requests = Column(Integer, nullable=False, default=0)

    @classmethod
    @handle_transaction
    def get(cls, **kwargs):
        """
        This function provides the first users what matches the given kwargs
        """
        return cls.session.quey(cls).filter_by(**kwargs).first()

