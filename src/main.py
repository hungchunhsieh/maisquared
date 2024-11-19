import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

# Replace 'your-service-account-key.json' with the path to your service account JSON key file
SERVICE_ACCOUNT_FILE = 'maisquared-d2412aaec7d7.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Authenticate using the service account
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

def list_parent_folders(parent_id):
    results = service.files().list(
        q=f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()
    folders = results.get('files', [])
    for folder in folders:
        createParentFolder(folder['name'])
        list_child_folders(folder['name'], folder['id'])

def list_child_folders(parent_name, child_id):
    results = service.files().list(
        q=f"'{child_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()
    folders = results.get('files', [])

    all_folders = []

    for folder in folders:
        all_folders.append(folder['name'])

    data = {
        "name": parent_name,
        "id": None,
        "serverUrl": None,
        "levelIds": all_folders,
    }
    path = 'output/{0}/manifest2.json'.format(parent_name,)
    createManifest(data, path)

def createManifest(data, path):
    with open(path, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def createParentFolder(folder_name):
    folder_path = 'output/{0}'.format(folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def createChildFolder(folder_name, parent_name):
    folder_path = 'output/{0}/{1}'.format(parent_name, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)



# Replace 'folder_id_here' with the actual folder ID from your link
folder_id = "1NiZ9rL19qKLqt0uNcP5tIqc0fUrksAPs"
list_parent_folders(folder_id)
