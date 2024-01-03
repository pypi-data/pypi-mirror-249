"""Class to build the data lake saving .csvs locally or in the s3 bucket.
"""

from datetime import date
import io
import logging
import os
from typing import Tuple

import boto3
import pandas as pd

from mxq_data_science_db.settings.settings import Settings

settings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DataLake:
    
    AWS_PROFILE = os.environ.get("AWS_PROFILE")
    BUCKET: str = os.environ.get("BUCKET", "")
    BUCKET_FOLDER: str = os.environ.get("BUCKET_FOLDER", "")
    FILE_DIR = os.path.join(settings.BASE_DIR, "files")

    def __init__(self, report: str, save_cols: list, tuple_partition: Tuple):
        assert DataLake.BUCKET, "BUCKET was not set"
        assert report, "Report is blank"
        self.report = report
        assert save_cols, "save_cols is blank"
        self.save_cols = save_cols

        self.tuple_partition = tuple_partition

    def save_data_locally(self, df: pd.DataFrame, partion: list = []):
        """Save the report locally

        Args:
            df (pd.DataFrame): report
            partion (list, optional): partions. Defaults to [].
        """
        folder_path = os.path.join(DataLake.FILE_DIR, self.report, *partion)
        logger.info(f"Saving locally {folder_path}: {len(df)}")
        os.makedirs(folder_path, exist_ok=True)
        df.to_csv(os.path.join(folder_path, f"{self.report}.csv"), index=False)

    def save_data_bucket(self, df: pd.DataFrame, partion: list = []):
        """Send the files to s3 bucket

        Args:
            df (pd.DataFrame): report
            partion (list, optional): partions. Defaults to [].
        """
        self.session_aws = boto3.Session(profile_name=DataLake.AWS_PROFILE)
        self.client = self.session_aws.client("s3")
        folder_path = os.path.join(DataLake.BUCKET_FOLDER, self.report, *partion)

        logger.info(f"Save in S3 Bucket: {DataLake.BUCKET}/{folder_path}")
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        self.client.put_object(
            Body=csv_data,
            Bucket=DataLake.BUCKET,
            Key=f"{folder_path}/{self.report}.csv",
        )

    def save_data(self, df: pd.DataFrame):
        """Run the save data

        Args:
            df (pd.DataFrame): report
        """
        logger.info(f"Save report: {len(df)} rows")
        df = df[self.save_cols].copy() if self.save_cols else df.copy()
        self.partion_dataframe(df)
        logger.info("Saved succesfuly")

    def partion_dataframe(
        self, df: pd.DataFrame, current_loop: int = 0, loop_values: list = []
    ):
        """Partion the DataFrame and save it locally or to s3.

        For example:
            tuple_partition = (year, month)

        csv will be save in:
        report_name/
            year=2023/
                month=1/
                    report_name.csv
                month=2
                    report_name.csv
            year=2022/
                month=1
                    report_name.csv


        Args:
            df (pd.DataFrame): report
            current_loop (int, optional): count the number of loping to execute the save in the last. Defaults to 0.
            loop_values (list, optional): partions values. Defaults to [].
        """
        if current_loop == len(self.tuple_partition):
            if settings.ENV == settings.DEV:
                self.save_data_locally(df, loop_values)

            if settings.ENV == settings.PROD or settings.ENV == settings.HMG:
                self.save_data_bucket(df, loop_values)

            return

        # Get the current loop variable from the self.tuple_partition
        loop_variable = self.tuple_partition[current_loop]
        # Iterate over the unique values and perform recursive calls
        for value in set(df[loop_variable]):
            loop_values.append(
                f"{loop_variable}={value}"
            )  # Add the current value to the loop_values list
            df_copy = df[df[loop_variable] == value].drop(loop_variable, axis=1)

            self.partion_dataframe(df_copy, current_loop + 1, loop_values)
            loop_values.pop()  # Remove the current value from the loop_values list
