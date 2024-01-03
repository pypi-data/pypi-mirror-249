"""Base model with general functions as upsert and bulk upsert
"""
import logging

import pandas as pd
from sqlalchemy import inspect
from sqlalchemy.dialects import mysql

from mxq_data_science_db.db.db import SQLConnection
from mxq_data_science_db.utils.utils import split_dataframe

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BaseModel:
    """Base class with general functions for the models."""

    __tablename__ = ""
    update_columns = []

    @classmethod
    def upsert(cls, *args, **kwargs):
        """Insert if duplicate key update"""
        obj = cls(*args, **kwargs)
        con = SQLConnection()
        logger.info(f"Update {obj.__tablename__} table on {con.database}")
        with con.open_session() as session:
            session.merge(obj)

    @classmethod
    def bulk_upsert(cls, df: pd.DataFrame, chuck_size: int = 10**4):
        """Insert/update a DataFrame

        Args:
            df (pd.DataFrame): dataframe to be inserted
        """
        table = cls().__table__
        logger.info(f"Bulk upsert in {table}, {len(df)} rows")
        if df.empty:
            logger.info("Nothing to insert/update")
            return

        # Update the non primary key columns
        inspector = inspect(cls)
        primary_keys = [column.name for column in inspector.primary_key]
        update_columns = [
            column.name
            for column in inspector.columns
            if column.name not in primary_keys
        ]

        # Run upinsert
        for chuck in split_dataframe(df, chuck_size=chuck_size):
            with SQLConnection() as con:
                insert_stmt = mysql.insert(table)
                upsert_stmt = insert_stmt.on_duplicate_key_update(
                    {col: getattr(insert_stmt.inserted, col) for col in update_columns}
                ).values(chuck.to_dict("records"))
                con.execute(upsert_stmt)
        logger.info(f"Bulk upsert done")
