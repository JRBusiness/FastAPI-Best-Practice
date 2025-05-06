"""
The base_model module contains the ModelMixin class, which is used to provide generic helper functions
"""
import contextlib
from contextlib import contextmanager
from typing import List
from functools import wraps
from loguru import logger
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin
from config.settings import Settings
from typing import TypeVar
import functools
from app import db

settings = Settings()


Base = declarative_base()
DBType = TypeVar("DBType", bound=Base)


def handle_transaction(func):
    """
    The handle_transaction function is a decorator that wraps the decorated function in a try/except block.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        The wrapper function is a wrapper for the decorated function.
        """
        with db():
            # First try to get the session from the first arg (for class methods)
            with contextlib.suppress(IndexError):
                # First try to get the session from the first arg (for class methods)
                session = getattr(args[0], "session", None)
            if not session:
                # If the session was not found yet, try to get it from keyword args
                session = kwargs.get("session")

            if not session:
                raise ValueError("Database session not provided to decorated function.")

            try:
                result = func(*args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                logger.error(e)

    return wrapper


@contextmanager
def safe_session(session):
    """
    The safe_session function is a context manager that wraps the session object.
    It will commit any changes to the database and then close the session, unless an exception occurs.
    If an exception occurs, it will rollback any changes made to the database and raise a new error.

    Args:
        self: Refer to the current instance of a class

    Returns:
        A context manager

    """
    try:
        yield session
        session.commit()
        session.save()
    except Exception as e:
        logger.error(f"Exception occurred while committing to database: {str(e)}")
        session.rollback()
        raise e


def rollback_safe(func):
    """
    The rollback_safe function is a decorator that wraps the decorated function in a try/except block.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        The rollback_safe function is a decorator that wraps the decorated function in a try/except block.
        """
        with safe_session(args[0].session) as _db:
            try:
                func(*args, **kwargs, db=_db)
            except Exception as e:
                logger.error(f"Exception occurred while executing {func}: {str(e)}")
                _db.rollback()
                raise e

        return wrapper


class ModelMixin(AllFeaturesMixin):
    """
    The ModelMixin exists to provide us some generic helper functions that are
    useful across most database transactions.
    """

    __abstract__ = True

    @classmethod
    @handle_transaction
    def commit(cls):
        """
        Commits the current session
        """
        try:
            with db():
                cls.session.commit()
                return cls
        except Exception as e:
            logger.error(f"Exception occurred while stacking model: {str(e)}")
            cls.session.rollback()

    def load(self) -> dict:
        """
        Model to dictionary
        """
        with db():
            return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    @handle_transaction
    def load_all(iterable: list) -> List[dict]:
        """
        List of Models to dictionary
        """
        with db():
            return [item.load() for item in iterable]

    @staticmethod
    @handle_transaction
    def add_model(model: Base):
        """
        Inserts records to database with given model and given kwargs
        """
        with db():
            db.session.add(model)
            db.session.commit()
            return model()

    @staticmethod
    @handle_transaction
    def remove_model(models: Base, **kwargs):
        """
        Deletes record from database with given model and kwargs
        """
        with db():
            object_id = kwargs.get("id")
            models.session.Query(models).filter_by(id=object_id).delete()
            db.session.commit()
            return object_id

    @staticmethod
    @handle_transaction
    def update_model(model: Base, **kwargs):
        """
        Updates record in db with given kwargs
        """
        with db():
            object_id = kwargs.get("id") or kwargs.get("uuid")
            obj = model.session.Query(model).filter_by(id=object_id).first()
            if kwargs.get("uuid"):
                obj = model.session.Query(model).filter_by(uuid=object_id).first()
            for k, v in kwargs.items():
                if v == "":
                    v = None
                setattr(obj, k, v)
            db.session.commit()
        return object_id

    @staticmethod
    @handle_transaction
    def stack_model(model: Base, **kwargs):
        """
        Inserts records to database with given model and given kwargs

        """
        with db():
            return db.session.add(model(**kwargs))
