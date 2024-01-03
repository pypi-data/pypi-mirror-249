"""Utils to save files on dropbox
Salva os arquivos na pasta:
https://www.dropbox.com/home/MaxiQuim%20Ltda/Aplicativos/0000_Data%20Science/
"""
from io import BytesIO
import logging
import os

import dropbox
import requests
from tqdm import tqdm

from mxq_data_science_db.settings.settings import Settings

settings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Dropbox:
    MAX_SIZE = 4 * 1024 * 1024
    TIMEOUT = 900
    BASE_DIR = os.environ.get("DROPBOX_FOLDER","")

    ACCESS_TOKEN = ""
    SESSION = None

    @classmethod
    def get_secrets(cls):
        """Set dos secrets de variaveis de ambiente ou entao do aws secret"""
        refresh_token = os.environ.get("DROPOX_REFRESH_TOKEN")
        app_key = os.environ.get("DROPOX_REFRESH_TOKEN")
        app_secret = os.environ.get("DROPOX_REFRESH_TOKEN")
        if refresh_token is None or app_key is None or app_secret is None:
            dropbox_secrets = settings.get_aws_secrets("dropbox_secrets")
            refresh_token = dropbox_secrets.get("REFRESH_TOKEN")
            app_key = dropbox_secrets.get("APP_KEY")
            app_secret = dropbox_secrets.get("APP_SECRET")

        assert refresh_token, "refresh_token not set"
        assert app_key, "app_key not set"
        assert app_secret, "app_secret not set"
        return refresh_token, app_key, app_secret

    @classmethod
    def upload_per_session(cls, file: bytes, target_path: str):
        """Upload em batch de arquivos maior que o limiete do dropbox

        Args:
            file (bytes): arquivo
            target_path (str): target path no dropbox
        """
        dbx = Dropbox.get_session()
        file_size = len(file)
        with BytesIO(file) as f:
            with tqdm(total=file_size, desc="Uploaded") as pbar:
                upload_session_start_result = dbx.files_upload_session_start(
                    f.read(Dropbox.MAX_SIZE)
                )
                pbar.update(Dropbox.MAX_SIZE)
                cursor = dropbox.files.UploadSessionCursor(
                    session_id=upload_session_start_result.session_id,
                    offset=f.tell(),
                )
                commit = dropbox.files.CommitInfo(path=Dropbox.BASE_DIR + target_path)
                while f.tell() < file_size:
                    if (file_size - f.tell()) <= Dropbox.MAX_SIZE:
                        print(
                            dbx.files_upload_session_finish(
                                f.read(Dropbox.MAX_SIZE), cursor, commit
                            )
                        )
                    else:
                        dbx.files_upload_session_append(
                            f.read(Dropbox.MAX_SIZE),
                            cursor.session_id,
                            cursor.offset,
                        )
                        cursor.offset = f.tell()
                    pbar.update(Dropbox.MAX_SIZE)

    @classmethod
    def upload_direct(cls, file: bytes, target_path: str):
        """Upload de arquivos menores

        Args:
            file (bytes): arquivo
            target_path (str): target path no dropbox
        """
        dbx = Dropbox.get_session()
        with BytesIO(file) as f:
            r_drop = dbx.files_upload(
                f.read(),
                Dropbox.BASE_DIR + target_path,
                mode=dropbox.files.WriteMode.overwrite,
            )
        logger.info(r_drop)

    @classmethod
    def get_access_token(cls):
        """Pegar o access token para o dropbox
        Baseado em:
        https://www.dropboxforum.com/t5/Dropbox-API-Support-Feedback/Get-refresh-token-from-access-token/td-p/596739
        """
        url = "https://api.dropbox.com/oauth2/token"

        refresh_token, app_key, app_secret = Dropbox.get_secrets()
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": app_key,
            "client_secret": app_secret,
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            logger.exception(response.text)
            response.raise_for_status()

        Dropbox.ACCESS_TOKEN = response.json().get("access_token")
        assert Dropbox.ACCESS_TOKEN, "Error when trying to get dropbox access token"

    @classmethod
    def get_session(cls):
        """Cria a sessão do drop

        Returns:
            session: dropbox session
        """
        if Dropbox.SESSION:
            return Dropbox.SESSION

        if not Dropbox.ACCESS_TOKEN:
            Dropbox.get_access_token()

        dbx = dropbox.Dropbox(Dropbox.ACCESS_TOKEN, timeout=Dropbox.TIMEOUT)
        return dbx

    @classmethod
    def upload_file(cls, file: bytes, target_path: str):
        """Função para fazer o upload

        Args:
            file (bytes): arquivo
            target_path (str): target path no dropbox
        """
        logger.info(f"Upload file to Dropbox {Dropbox.BASE_DIR}")

        if len(file) > Dropbox.MAX_SIZE:
            Dropbox.upload_per_session(file, target_path)
        else:
            Dropbox.upload_direct(file, target_path)
        logger.info(f"Success: {target_path}")
