"""Class to manage the settings, env variables and secrets.
.env file must be settings/secrets

ENV vars:
ENVIRONMENT:
    prod: run in production
    hmg: use homologa dbs
    dev: use local db
RUNNING_LOCAL: if True it will use DB_HOST = 127.0.0.1
DATABASE: database name

prod/hmg env vars:
DB_GCP_HOST
DB_GCP_PORT
"""
import json
import logging
import os
import sys

import boto3

from mxq_data_science_db.settings import logger

log = logging.getLogger(__name__)


class Settings:
    """Class to manage settings, secrets and env variables"""

    PROD = "prod"
    HMG = "hmg"
    DEV = "dev"
    ENVS = [
        DEV,
        HMG,
        PROD,
    ]

    AWS_PROFILE = os.environ.get("AWS_PROFILE")

    DB_ECONOMIA = "db_economia"
    DB_COMMODITY = "db_commodity"
    DB_COMEX = "db_comex"
    LIST_DATABASES = [DB_ECONOMIA, DB_COMMODITY, DB_COMEX]

    _instance = None
    _first = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            Settings._instance = super(Settings, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not Settings._first:
            log.debug("settings already instanced")
            return

        log.info("")
        log.info("-" * 30)
        log.info("Running Settings")
        log.info("-" * 30)
        self.BASE_DIR = os.getcwd()
        self.SECRETS_DIR = os.path.join(self.BASE_DIR, "settings", "secrets")
        self.FILES_DIR = os.path.join(self.BASE_DIR, "files")

        # ENV
        self.ENV = os.environ.get("ENV", "dev").lower()
        assert self.ENV in Settings.ENVS, f"{self.ENV} - invalid value. {Settings.ENVS}"
        log.info("Using environment: %s", self.ENV)

        # DATABASE
        self.DATABASE = os.environ.get("DATABASE", "").lower()
        assert (
            self.DATABASE in Settings.LIST_DATABASES
        ), f"Database invalid value: {self.DATABASE}\n{Settings.LIST_DATABASES}"
        log.info("Using database: %s", self.DATABASE)

        # SET Secrets
        self._get_secrets()

        Settings._first = False

    def _get_secrets(self):
        """Open the .env file"""
        if self.ENV in [Settings.PROD, Settings.HMG]:
            self._aws_secrets_db()
        else:
            log.info("Using dev local secrets")
            self._dev_secrets()

    def _aws_secrets_db(self):
        """Get secrets in AWS secret manager"""
        self.sql_secret_json = self.get_aws_secrets("report_secrets_sql")
        self._set_DB_from_secret()

    def get_aws_secrets(self, aws_secretmanager: str) -> dict:
        """Get Secrets from AWS secret manager

        Args:
            aws_secretmanager (str): secret manager name

        Returns:
            dict: json secret
        """
        session = boto3.Session(profile_name=Settings.AWS_PROFILE)
        client = session.client("secretsmanager")

        get_secret_value_response = client.get_secret_value(SecretId=aws_secretmanager)

        return json.loads(get_secret_value_response["SecretString"])

    def _set_DB_from_secret(self):
        """Set secrets for HMG e PROD"""
        self.DB_GCP_HOST = self.sql_secret_json["DB_GCP_HOST"]
        self.DB_GCP_PORT = self.sql_secret_json["DB_GCP_PORT"]
        self.db_secret = self.sql_secret_json.get(self.DATABASE.upper())
        assert self.db_secret, "Database secret not found in AWS secret"
        self.DB_GCP_USER = self.db_secret.get(self.ENV.upper()).get("USER")
        self.DB_GCP_PASSWORD = self.db_secret.get(self.ENV.upper()).get("PASSWORD")

    def _dev_secrets(self):
        """Set secrets for development"""
        self.DB_GCP_HOST = os.environ.get("DB_GCP_HOST", "127.0.01")  # "dev-mysql"
        self.DB_GCP_PORT = 3306
        self.DB_GCP_USER = os.environ.get("DB_GCP_USER", "development")
        self.DB_GCP_PASSWORD = os.environ.get("DB_GCP_PASSWORD", "development")

    def build_db_url(self):
        """Build MySQL url

        Returns:
            mysql url
        """
        if self.ENV == Settings.HMG:
            db = self.DATABASE + "_hmg"
        else:
            db = self.DATABASE

        return f"mysql://{self.DB_GCP_USER}:{self.DB_GCP_PASSWORD}@{self.DB_GCP_HOST}:{self.DB_GCP_PORT}/{db}"
