import os
import time
import json
import tkinter as tk
from tkinter import filedialog
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']

uploaded_files = {}

def authenticate_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\\adith\\OneDrive\\Desktop\\projects\\go\\helloworld\\BACKITUP\\beckip\\client_secret_783620241105-mrqrqk69ismq1h9d3udfns66d8mf9svb.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_to_google_drive(service, file_path):
    filename = os.path.basename(file_path)
    mod_time = os.path.getmtime(file_path)

    if filename in uploaded_files and uploaded_files[filename] >= mod_time:
        return

    file_metadata = {'name': filename}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print('File ID: %s' % file.get('id'))

    uploaded_files[filename] = mod_time

    with open('uploaded_files.json', 'w') as f:
        json.dump(uploaded_files, f)

def backup_files(interval, folder_path):
    global uploaded_files
    if os.path.exists('uploaded_files.json'):
        os.remove('uploaded_files.json')

    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            upload_to_google_drive(service, file_path)

    while True:
        time.sleep(interval)

def select_directory():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

root = tk.Tk()
root.title('Backup Application')
root.geometry('400x200')
root.configure(bg='lightblue')

tk.Label(root, text="Backup Interval (in seconds):", font=('Segoe UI',14), bg='lightblue', fg='black').grid(row=0, column=0, padx=10, pady=10)
interval_entry = tk.Entry(root, font=('Segoe UI', 14))
interval_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Folder Path:", font=('Segoe UI', 14), bg='lightblue', fg='black').grid(row=1, column=0, padx=10, pady=10)
folder_path_entry = tk.Entry(root, font=('Segoe UI', 14))
folder_path_entry.grid(row=1, column=1, padx=10, pady=10)

select_directory_button = tk.Button(root, text="Select Directory", command=select_directory, font=('Segoe UI', 14,'bold'), bg='darkblue', fg='white')
select_directory_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

start_backup_button = tk.Button(root, text="Start Backup", command=lambda: backup_files(int(interval_entry.get()), folder_path_entry.get()), font=('Segoe UI', 14,'bold'), bg='darkblue', fg='white')
start_backup_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()


