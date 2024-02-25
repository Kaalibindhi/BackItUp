This is a utility that built with Python and Tkinter that periodically backs up selected folders and files from your computer to cloud storage, safeguarding impotant data without manual intervention. It allows users to select a directory and set an interval for backups. The application uses the Google Drive API to store the backups.
1. **Google Drive Authentication**: The application authenticates with Google Drive using OAuth 2.0. It stores the access token in a local file (`token.json`) for future use.
2. **File Backup**: The application backs up all files in the selected directory to Google Drive. It checks the modification time of each file and only uploads files that have been modified since the last backup.
3. **Backup Interval**: Users can set the interval for backups. The application will automatically backup the selected directory to Google Drive at the specified interval.
4. **Tkinter GUI**: The application has a graphical user interface built with Tkinter. Users can select the directory to backup and set the backup interval through the GUI.
This was done by my team Radical Skadattle for the Tink Her Hack 2.0. which consists of Aditi Asok, Aimee Jobi, Amitha Thomas. 
