import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleConnection:
    """
    The GoogleConnect Class is used to connect to the personal google account using google API credentials
    and retrieve and parse the data from the shared google sheet.
    """
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    def __init__(self, creds_file):
        self.client = None
        self.creds = None
        self.creds_file = creds_file

    def __enter__(self):
        try:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_file, GoogleConnection.scope)
            self.client = gspread.authorize(self.creds)
        except FileNotFoundError as e:
            pass

        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.session.close()
