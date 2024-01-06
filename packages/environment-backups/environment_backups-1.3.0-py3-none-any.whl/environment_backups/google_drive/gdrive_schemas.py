from __future__ import annotations

import pickle
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from google.oauth2.credentials import Credentials
from pydantic import AnyHttpUrl, BaseModel, Field, HttpUrl, ValidationError
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated


def validate_client_id(v: str) -> str:
    regexp = re.compile(r"^\w+-\w+.apps.googleusercontent.com$")
    match = regexp.match(v)
    if match:
        return v
    else:
        raise ValidationError(f'The client id does not comply with the expected pattern')


ClientId = Annotated[str, AfterValidator(validate_client_id)]


class Installed(BaseModel):
    client_id: ClientId
    project_id: str
    auth_uri: HttpUrl = Field(default="https://accounts.google.com/o/oauth2/auth")
    token_uri: HttpUrl = Field(default="https://oauth2.googleapis.com/token")
    auth_provider_x509_cert_url: HttpUrl = Field(default="https://www.googleapis.com/oauth2/v1/certs")
    client_secret: str
    redirect_uris: List[AnyHttpUrl] = Field(default=['http://localhost'])


class GoogleConfiguration(BaseModel):
    installed: Installed


class GoogleCredentialsToken(BaseModel):
    token_file: Path
    max_age_days: Optional[int] = 15

    def get_token(self) -> Credentials | None:
        creds = None
        if self.token_file.exists():
            # TODO test for age of token. If token is older than 2 weeks?? don't load it.
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        return creds

    @property
    def created(self) -> datetime | None:
        if self.token_file.exists():
            dtc_timestamp = self.token_file.stat().st_ctime
            return datetime.fromtimestamp(dtc_timestamp)

    @property
    def age_days(self) -> int:
        if self.created:
            td = datetime.now() - self.created
            return td.days
        return -1

    @property
    def expired(self):
        return self.age_days > self.max_age_days

    def save(self, creds: Credentials):
        with open(self.token_file, 'wb') as token:
            pickle.dump(creds, token)
