from datetime import datetime
from pathlib import Path

from pydantic import BaseModel

from environment_backups.google_drive.gdrive_schemas import GoogleCredentialsToken


class DummyTokenObject(BaseModel):
    name: str
    age: int


class TestGoogleCredentialsToken:
    def test_save(self, tmp_path):
        dummy_token = DummyTokenObject(name='My name', age=4)
        dummy_file = tmp_path / 'cred.token'
        gdrive_credential_token = GoogleCredentialsToken(token_file=dummy_file)
        assert not dummy_file.exists()
        gdrive_credential_token.save(dummy_token)
        assert dummy_file.exists()
        print(gdrive_credential_token.created)

    def test_age(self, fixtures_folder):
        dummy_file = fixtures_folder / 'dummy_token.token'
        gdrive_credential_token = GoogleCredentialsToken(token_file=dummy_file)
        # print(f'{gdrive_credential_token.age_days}')
        assert gdrive_credential_token.age_days != -1
