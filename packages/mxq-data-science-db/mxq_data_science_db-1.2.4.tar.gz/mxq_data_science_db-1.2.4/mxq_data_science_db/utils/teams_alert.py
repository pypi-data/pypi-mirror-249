"""Utils to send alerts in Teams
"""
import logging
import os

import pymsteams

from mxq_data_science_db.settings.settings import Settings

settings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class teamsAlert:
    WEBHOOK_ULR = os.environ.get("TEAMS_WEBHOOK_ULR")

    def __init__(self):
        if teamsAlert.WEBHOOK_ULR is None:
            self.get_secret()
        self.teams_instance = pymsteams.connectorcard(teamsAlert.WEBHOOK_ULR)

    def get_secret(self):
        """Get webhook from secret manager"""
        teams_secrets = settings.get_aws_secrets("teams_secret")
        teamsAlert.WEBHOOK_ULR = teams_secrets.get("WEBHOOK_ULR")
        assert teamsAlert.WEBHOOK_ULR, "webhook not set"

    def send_message(self, message: str):
        """Send message to teams

        Args:
            message (str): message
        """
        self.teams_instance.text(message)
        self.teams_instance.send()

    def success_message(self, script_name: str):
        """Send default success message

        Args:
            script_name (str): script name
        """
        message = f"🟢 **{script_name}** ran successfully"
        self.send_message(message)

    def error_message(self, script_name: str):
        """Send default error message

        Args:
            script_name (str): script name
        """
        message = f"🔴 **{script_name}** got a error"
        self.send_message(message)
