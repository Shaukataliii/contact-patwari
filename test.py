import dropbox, time, csv, os

log_filename = 'contactpatwari-logs.csv'

def update_dropbox_logsfile(log_content):
    print('\n\nInside update_dropbox_logsfile()')
    token = 'sl.BwDot-_TH3sdYE4NyS3AGvha5ZdrfsSSIuRP_l3jq54lrjEbu7p1sYIcS82sGyZBTinvd-_RVnKi-aCYxDHr-MLdAwPOAvaoLWcRk7nwyRqBGDKBGZqA6I2IYBPkoCQ0SVNd5rwvfB5F'

    # Connecting to dropbox
    try:
        dbx = dropbox.Dropbox(token)
        dbx.users_get_current_account()
        print('-- Dropbox connection successful.')

    except:
        print('-- Error connecting to dropbox.')

    # updating server file
    print('-- Uploading file to server')
    try:
        with open(log_filename, 'rb') as lf:
            dbx.files_upload(lf.read(), '/' + log_filename, mode = dropbox.files.WriteMode('overwrite'))

        print('-- Server file uploaded (overwritten) successfully. Returning 0')
        return 0

    except:
        print('-- An error occured while uploading the updated file. Returning 1')
        return 1

# Recording that the username with profession and contact_no successfully takesn the details of patwari of mouza: selected mouze. The file is a csv.
def record_log(name, profession, contact, mouza, status):
    '''Requires user_name, profession, contact, mouza, status and records log with timestamp. The file is a csv i.e. logs.csv'''
    global log_filename

    print('Inside record_log()')
    # creating timestamp
    print('-- Creating timestamp')
    timestamp = time.localtime()
    year = timestamp.tm_year
    month = timestamp.tm_mon
    day = timestamp.tm_mday
    hour = timestamp.tm_hour
    mint = timestamp.tm_min
    sec = timestamp.tm_sec
    timestamp = f'{year}-{month}-{day}-{hour}-{mint}-{sec}'

    # preparing log
    print('-- Preparing log')
    log_content = [timestamp, name, profession, contact, mouza, status]

    if not os.path.exists(log_filename):
        print('Writting log details (file was not present)')
        with open(log_filename, 'w', newline = '') as lf:
            csv_writter = csv.writer(lf)
            csv_writter.writerow(log_content)
    else:
        print('-- Appending log details')
        with open(log_filename, 'a', newline = '') as lf:
            csv_writter = csv.writer(lf)
            csv_writter.writerow(log_content)

    update_dropbox_logsfile(log_content)

    print('-- Log saved. Returning 0')
    return 0
    
    # Add timestamping feature here and then write timestamp and other infor in a csv file. (logs.txt)


record_log('shaukat', 'testing', 'fake', 'tahti kalra', 'success')