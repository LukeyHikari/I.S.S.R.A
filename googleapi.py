from __future__ import print_function
from pprint import pprint
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
import google.auth
import io
import pandas as pd

class recording:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        self.creds = None
        self.service = None
        self.spreadsheetid = None
        self.ranges = None
        self.valrenopt = None
        self.valinpopt = None
        self.valranbody = None
        self.values = None
        self.maxgrade = None
        self.grade = None
        self.noofstudents = None
        self.actno = None
        self.acttype = None
        self.currstud = None
        self.grades = None
        self.wtindex = ['F','G','H','I','J','K','L','M','N','O']
        self.ptindex = ['S','T','U','V','W','X','Y','Z','AA','AB']

    def oauth(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('sheettoken.json'):
            self.creds = Credentials.from_authorized_user_file('sheettoken.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('sheettoken.json', 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('sheets', 'v4', credentials=self.creds)
            print("Authentication Completed")
        except HttpError as err:
            print(err)

    def checkgrade(self, _noofstudents, _actno, _acttype, _grade):
        try:
            self.oauth()
            self.spreadsheetid = '1e41321N9V0wQF7kifoDMpCfelVUhNkftdoVLsgfz38E'
            self.valrenopt = 'FORMATTED_VALUE'
            self.noofstudents = _noofstudents
            self.actno = _actno
            self.acttype = f'{_acttype}'
            self.grades = _grade

            for i in range(self.noofstudents): #Identifies cell to check and write to
                if self.acttype == 'Performance':
                    self.ranges = f'PR2_Q1!{self.ptindex[self.actno-1]}{12+i}'
                elif self.acttype == 'Written':
                    self.ranges = f'PR2_Q1!{self.wtindex[self.actno-1]}{12+i}'

                request = self.service.spreadsheets().values().get(
                    spreadsheetId=self.spreadsheetid, range=self.ranges,
                    valueRenderOption=self.valrenopt).execute()
                cellval = request.get('values', [])
                if len(cellval) > 0:
                    pprint(f'Student {i+1} has a Grade')
                else:
                    self.recordgrade(i, self.actno, _acttype, _grade[i])
        except HttpError as error:
            print(f"An Error Occured: {error}")
            return
        
    def recordgrade(self, _currstud, _actno, _acttype, _grade):
        try:
            self.spreadsheetid = '1e41321N9V0wQF7kifoDMpCfelVUhNkftdoVLsgfz38E'
            self.valinpopt = 'USER_ENTERED'
            self.grade = _grade
            self.values = [[self.grade]]
            self.valranbody ={'values': self.values}

            #Identifies cell to write to
            self.actno = _actno
            self.currstud = _currstud
            self.acttype = f'{_acttype}'
            if self.acttype == 'Performance':
                self.ranges = f'PR2_Q1!{self.ptindex[self.actno-1]}{12+self.currstud}'
            elif self.acttype == 'Written':
                self.ranges = f'PR2_Q1!{self.wtindex[self.actno-1]}{12+self.currstud}'                

            request = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheetid, range=self.ranges,
                valueInputOption=self.valinpopt, body=self.valranbody).execute()

        except HttpError as error:
            print(f"An Error Occured: {error}")
            return
    
    def highestgrade(self, _maxgrade, _actno, _acttype): #function to be run independently
        try:
            self.oauth()
            self.spreadsheetid = '1e41321N9V0wQF7kifoDMpCfelVUhNkftdoVLsgfz38E' 
            self.valinpopt = 'USER_ENTERED'
            self.maxgrade = _maxgrade
            self.values = [[self.maxgrade]]
            self.valranbody ={'values': self.values}

            #Identifies cell to write to
            self.actno = _actno
            self.acttype = f'{_acttype}'
            if self.acttype == 'Performance':
                self.ranges = f'PR2_Q1!{self.ptindex[self.actno-1]}10'
            elif self.acttype == 'Written':
                self.ranges = f'PR2_Q1!{self.wtindex[self.actno-1]}10'

            request = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheetid, range=self.ranges,
                valueInputOption=self.valinpopt, body=self.valranbody).execute()

        except HttpError as error:
            print(f"An Error Occured: {error}")
            return

class download:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        self.creds = None
        self.service = None

    def oauth(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('drivetoken.json'):
            self.creds = Credentials.from_authorized_user_file('drivetoken.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('drivetoken.json', 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('drive', 'v3', credentials=self.creds)
            print("Authentication Completed")
        except HttpError as err:
            print(err)

    def dlfile(self, real_file_id):
        self.oauth()
        try:
            file_id = real_file_id
            # pylint: disable=maybe-no-member
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        file.seek(0)

        with open(os.path.join(f'{os.getcwd()}/temp/1.png'), 'wb') as f:
            f.write(file.read())
            f.close()

        #return file.getvalue()
    
    def getFolderFiles(self, _folderid):
        self.oauth()
        folder = _folderid
        query = f"parents = '{folder}'"

        response = self.service.files().list(q=query).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = self.service.files().list(q=query, pageToken = nextPageToken).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')

        df = pd.DataFrame(files)
        id_dict = df["id"].to_dict()
        
        return id_dict


if __name__ == '__main__':
    run = recording()
    dl = download()
    #dl.dlfile('1o9Rg_sV-BUcuy5oBsJCgco6td_kKAGkP')
    #dl.getFolderFiles('1sfTXDhMzbx-UUKvvzqDScYWHf5VEJowd')
    run.oauth()
    # dl.dlfile('1sfTXDhMzbx-UUKvvzqDScYWHf5VEJowd')
    # run.highestgrade(10, 1, 'Performance')
    # run.checkgrade(5, 1, 'Performance', ['10','5','6','2','1'])