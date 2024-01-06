from pathlib import Path
from typing import Optional

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from rich.pretty import pprint

from environment_backups.exceptions import UploadError
from environment_backups.google_drive.gdrive_schemas import GoogleCredentialsToken


class GDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, secrets_file: Path):
        # FIXME raise error if secrets_file does not exist
        self.secrets_file = secrets_file
        token_file = secrets_file.parent / 'token.pickle'
        creds = self.get_g_drive_credentials(token_file)
        self.service = build('drive', 'v3', credentials=creds)

    def get_g_drive_credentials(self, token_file: Path) -> Credentials:
        token = GoogleCredentialsToken(token_file=token_file)
        creds = token.get_token()

        if not creds or not creds.valid:
            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError:
                    flow = InstalledAppFlow.from_client_secrets_file(str(self.secrets_file), self.SCOPES)
                    creds = flow.run_local_server(port=0)
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(self.secrets_file), self.SCOPES)
                creds = flow.run_local_server(port=0)
            token.save(creds)
        return creds

    def upload(self, file_to_upload: Path, folder_id: str):
        filename = file_to_upload.name
        mime_type = 'application/octet-stream'
        body = {'name': filename, 'parents': [folder_id], 'mimeType': mime_type}
        try:
            media_body = MediaFileUpload(file_to_upload, mimetype=mime_type, chunksize=10485760, resumable=True)
            request = self.service.files().create(body=body, media_body=media_body)  # Modified
            result = request.execute()
            return result
        except Exception as e:
            error_message = f'Upload error. Type {e.__class__.__name__} error {e}'
            raise UploadError(error_message)

    def upload_folder(self, folder_to_upload: Path, parent_folder_id: str) -> None:
        """
        Uploads the content of a folder to Google Drive.

        :param folder_to_upload: Path of the folder to upload.
        :param parent_folder_id: ID of the Google Drive folder where the content should be uploaded.
        """
        # Traverse through the folder and its subfolders
        folder_id = self.create_folder(folder_name=folder_to_upload.name, parent_folder_id=parent_folder_id)
        for item in folder_to_upload.iterdir():
            if item.is_dir():
                # If the current item is a subfolder, create a folder in Google Drive and then upload its contents
                folder_id = self.create_folder(item.name, folder_id)
                self.upload_folder(item, folder_id)
            else:
                # If the current item is a file, upload it

                self.upload(item, folder_id)

    def create_folder(self, folder_name: str, parent_folder_id: Optional[str] = None) -> str:
        """
        Creates a folder in Google Drive.

        :param folder_name: Name of the folder to create.
        :param parent_folder_id: ID of the parent folder.
        :return: ID of the created folder.
        """
        body = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        if parent_folder_id:
            body['parents'] = [parent_folder_id]
        folder = self.service.files().create(body=body, fields='id').execute()
        return folder.get('id')

    def list_content(self, parent_folder_id: str):
        """
        Lists all the content (files and folders) in a Google Drive folder.

        :param parent_folder_id: ID of the Google Drive folder.
        :return: List of dictionaries containing 'name' and 'id' of each item.
        """
        results = []
        query = f"'{parent_folder_id}' in parents"

        # Fetch files and folders from the Google Drive API
        # Reference https://developers.google.com/drive/api/reference/rest/v3/files
        file_attributes = [
            'id',
            'name',
            'starred',
            'shared',
            'permissions(kind,type,role)',
            'mimeType',
            'fileExtension',
            'size',
        ]
        file_fields = ', '.join(file_attributes).strip()
        print(f'>>> {file_fields}')
        fields_definition = f"nextPageToken, files({file_fields})"
        # fields_definition = "nextPageToken, files(id, name)"
        response = self.service.files().list(q=query, fields=fields_definition).execute()

        # Extract the file names and IDs
        items = response.get('files', [])
        for item in items:
            results.append(item)

        # Handle pagination
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.files().list(q=query, fields=fields_definition, pageToken=page_token).execute()
            items = response.get('files', [])
            for item in items:
                results.append(item)

        return results


if __name__ == '__main__':
    root_folder = Path(__file__).parent.parent.parent
    sec_file = root_folder / '.envs' / 'luis.berrocal.1942-oauth.json'
    if not sec_file.exists():
        raise Exception(f'{sec_file} not found.')

    gdrive = GDrive(secrets_file=sec_file)
    fldr_id = '1nVh5_8SfU5a9wxGdgwyOkpNQC6tJ4qTF'
    file_to_upload = root_folder / 'README.md'

    gdrive.upload(file_to_upload, fldr_id)

    results = gdrive.list_content(fldr_id)
    for r in results:
        pprint(r)
        print('-' * 80)
