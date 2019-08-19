def googlesheet_operations():

    from googleapiclient.discovery import build
    from oauth2client.service_account import ServiceAccountCredentials
    from googleapiclient.http import MediaFileUpload

##Authorize google drive api user and get credentials

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('Google-sheets-project-6ec13ae2ae0b.json', scope)


##Upload file to Google drive

    drive_service =  build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': 'finance_flagging',
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    media = MediaFileUpload('pandas_condition.xlsx',
                        resumable=True)


    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id').execute()


    file_id = file['id']

## Apply share to all permission to file uploaded
    batch = drive_service.new_batch_http_request()
    user_permission = {
        'type': 'anyone',
        'role': 'writer',
        'allowFileDiscovery' : True
    }
    batch.add(drive_service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
    ))
    batch.execute()

## Get the download link from Google
    data = drive_service.files().get(fileId=file_id,fields='exportLinks').execute()
    download_link = data['exportLinks'].get('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

## Delete the file from the drive
    drive_service.files().delete(fileId=file_id)

    return download_link