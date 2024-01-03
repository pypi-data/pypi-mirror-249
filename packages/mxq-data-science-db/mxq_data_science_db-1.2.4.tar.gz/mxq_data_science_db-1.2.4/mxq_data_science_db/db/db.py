"""Class to manage SQL connections to the DB
"""

from contextlib import contextmanager
import importlib
import logging
import sys
import time

import pymysql

pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import Session

from mxq_data_science_db.settings.settings import Settings


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
log = logging.getLogger(__name__)

settings = Settings()


class SQLConnection:
    """Open connections SQL database"""

    def __init__(self, database: str = settings.DATABASE):
        self.database = database
        self._build_url()
        self.engine = create_engine(self._url, echo=False)
        self.settings = settings

    def __enter__(self):
        """Open a transition connection with autocommit False
        Returns:
            connection
        """

        for i in range(100):
            try:
                self._conn = self.engine.connect()
            except:
                log.error(f"Try to connect")
                if i > 60:
                    raise
                time.sleep(1)
            else:
                break

        log.info(f"Connected: {self._url}")
        return self._conn

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """If no errors then commit and close the connection"""
        if exc_type is None:
            self._conn.commit()
        self._conn.close()

    @contextmanager
    def open_session(self):
        """Open the session

        Yields:
            session:
        """
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _build_url(self):
        """Build the url to connect to the db"""
        self._url = make_url(settings.build_db_url())

    def get_model_base(self):
        my_module = importlib.import_module(
            f"mxq_data_science_db.db.models.{self.database}"
        )
        Base = getattr(my_module, "Base")
        return Base
