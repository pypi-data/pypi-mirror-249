"""Google Services Adapter module"""
from typing import List, Dict, Any
from os import environ, path as os_path
from io import BytesIO
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from googleapiclient.discovery import HttpRequest
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
ENV_VAR_NAMES = ["GOOGLE_TOKEN_PATH", "GOOGLE_CREDENTIALS_PATH"]

for env_var_name in ENV_VAR_NAMES:
    value = environ.get(env_var_name)
    if value is not None:
        globals()[env_var_name] = value
    else:
        raise EnvironmentError(
            f'Environment variable "{env_var_name}" is NOT set')


class GoogleServices():
    """Adapter for Google Services"""

    @classmethod
    def __get_google_credentials__(cls):
        creds = None
        try:
            if os_path.exists(GOOGLE_TOKEN_PATH):  # pylint:disable=undefined-variable
                creds = Credentials.from_authorized_user_file(
                    GOOGLE_TOKEN_PATH, SCOPES)  # pylint:disable=undefined-variable
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        GOOGLE_CREDENTIALS_PATH, SCOPES)  # pylint:disable=undefined-variable
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(GOOGLE_TOKEN_PATH, 'w', encoding="utf-8") as token:  # pylint:disable=undefined-variable
                    token.write(creds.to_json())
        except Exception as err:
            raise ValueError(
                f'Google Authentication Error {err}') from err
        return creds

    @classmethod
    def read_gsheet_data(cls, spreadsheet_id: str, range_name: str) -> List[Dict[str, Any]]:
        """Descarga desde GSheets a memoria y luego lo convierte a JSON"""
        data_as_json = []
        try:
            service = build(
                'sheets', 'v4', credentials=cls.__get_google_credentials__())
            if hasattr(service, 'spreadsheets'):
                sheet: Resource = service.spreadsheets()
                result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                            range=range_name).execute()
                values = result.get('values', [])
                if values:
                    headers = values[0]
                    data_as_json = [dict((header, value) for header, value in zip(
                        headers, row)) for row in values[1:]]
            return data_as_json
        except Exception as err:
            raise ConnectionError(
                'Error al leer datos de Google Sheets: ', err) from err

    @classmethod
    def read_excel_data_from_google_drive(cls, file_id: str, sheet_name: str) -> List[Dict[str, Any]]:
        """Descarga desde GDrive a memoria y luego lo convierte a JSON"""
        data_as_json = []
        try:
            service: Resource = build(
                'drive', 'v3', credentials=cls.__get_google_credentials__())
            if hasattr(service, 'files'):
                request: HttpRequest = service.files().get_media(fileId=file_id)
                downloader = request.execute()
                with BytesIO(downloader) as f:
                    xls = pd.ExcelFile(f)
                    for sheet in xls.sheet_names:
                        if sheet.strip() == sheet_name:
                            df = xls.parse(sheet)  # .fillna(0)
                            df.columns = df.columns.str.lower()
                            df.columns = df.columns.str.strip()
                            data_as_json = df.to_dict(orient='records')
            return data_as_json
        except Exception as err:
            raise ConnectionError(
                f'Error al leer datos en formato Excel desde Google Drive file id {file_id}') from err

    @classmethod
    def read_directory_content_from_google_drive(cls, dir_id: str, mime_type_filter: str) -> List[Dict[str, Any]]:
        """Lee el contenido de un directorio de Google drive y lo devuelve en JSON"""
        data_as_json: list = []
        try:
            service: Resource = build(
                'drive', 'v3', credentials=cls.__get_google_credentials__())
            if hasattr(service, 'files'):
                results = service.files().list(
                    q=f"'{dir_id}' in parents and trashed=false", fields="files(id, name, mimeType)").execute()
                items = results.get('files', [])
                if items:
                    for item in items:
                        if item.get('mimeType') == mime_type_filter:
                            data_as_json.append(item)
            return data_as_json
        except Exception as err:
            raise ConnectionError(
                f'Error al leer el directorio "{dir_id}" de Google Drive') from err
