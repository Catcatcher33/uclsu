from __future__ import print_function

import os.path
import csv
import sys
import os
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE = os.getenv('RANGE')
SHEET_ID = os.getenv('SHEET_ID')


def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_members(file_name: str):
    members: list = []
    with open(file_name, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for line in csvreader:
            members.append([line[2]])  # Member emails column.
    return members


def get_last_index(spreadsheet):
    response = spreadsheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    return len(response.get('values'))


def add_members(file_name, sheet):
    index: int = get_last_index(sheet)
    members: list = get_members(file_name)
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, 
        range=f'Form Responses 1!B{index+1}:B', 
        valueInputOption='RAW', 
        body={'values':members}
        ).execute()


def remove_duplicates(spreadsheets):
    request_body: dict = {
        "requests" : [{
            "deleteDuplicates" : { 
                "range": {"sheetId": SHEET_ID},
                "comparisonColumns": {
                    "sheetId": SHEET_ID,
                    "dimension":"COLUMNS",
                    "startIndex":1,
                    "endIndex":2
                }
            }
        }]
    }
    spreadsheets.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=request_body).execute()


def edit(creds, file_name: str):
    spreadsheets = build('sheets', 'v4', credentials=creds).spreadsheets()
    add_members(file_name, spreadsheets)
    remove_duplicates(spreadsheets)


def main(file_name: str):
    creds = authenticate()
    try:
        edit(creds, file_name)
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main(sys.argv[1])