# drive/upload.py
import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()        
drive = GoogleDrive(gauth)

def create_folder(folder_name, parent_folder_id=None):
    query = f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"
    else:
        query += " and 'root' in parents"

    file_list = drive.ListFile({'q': query}).GetList()
    if file_list:
        return file_list[0]['id']
    
    folder_metadata = {'title': folder_name,'mimeType': 'application/vnd.google-apps.folder'}
    if parent_folder_id:
        folder_metadata['parents'] = [{'id': parent_folder_id}]

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']

def upload_file(path, parent_folder_id):
    for x in os.listdir(path):
        if os.path.isfile(os.path.join(path, x)):  # Abaikan folder
            file = drive.CreateFile({'title': x, 'parents': [{'id': parent_folder_id}]})
            file.SetContentFile(os.path.join(path, x))
            file.Upload()
            print(f"File {x} berhasil diunggah ke folder ID: {parent_folder_id}")
            file = None