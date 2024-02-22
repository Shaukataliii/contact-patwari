# git add .
# git commit -m 'commit name'
# git push -u origin main
import pandas as pd
import streamlit as st
import time, os, csv
import dropbox

############################# Flow of the application
# Sets global variables and then goes inside the main() functions. There calls the required global variables. Loads the processed dataframe and creates UI components. On user click on the contact_btn button, calls the function to validate user input. If successful, then calls function to get patwari details. If successful, displays to the user. If validation fails, gives error to the user to fill the fields correctly. If details not found in df, tells the user that we don't have any match. All all the three cases i.e. successful displaying of details, validation error, records not found, records logs into the logs.csv file with timestamp and user details.

############################# Code Started

# Global Variables of df, and ready csv_data_filepath
session = st.session_state
csv_data_filepath = 'patwari-contacts-data.csv'
log_filename = 'contactpatwari-logs.csv'
df = None
# extracted from the df mouza column and hard coded. To avoid unnecessary computation. However, loaded processed data can be sent to the prepare_known_mouzas_list and uncommented the 3rd last line to get this list printed in the terminal.
data_mouzas = [
   'Barranga', 'Thati Kalra', ' Thati Chah', ' Dhok Dera', 'Moza Adleky', 'Sodyke', 'Chak Muhammad Pur', '205/9R', 'Kotli Kohala ', 'Melay Wali', 'Burj Jae', 'Ahmad Shah Wali', '213/9R', '214/9R', '215/9R', 'Garhi Ikhtiar Khan ', 'Leiti', 'Dora Sohu', 'Kot Raja', ' Chak 8 Sb', ' Uppi', 'Litri Janobi', 'Jandawala', ' 46/Db ', 'Chak No 219/9R. 296/Hr', 'Havli Coranga', ' Waliat Pur', 'Dhoray Wala', ' Thathi Sameja', 'Khalti', ' Chak No 162Np', ' Chak No 166Np', '4', '5', '114', '116 Dnb', 'Jhok Yar Shah', ' Chabri Bala Sharqi ', 'Ladan', ' Usman Dona', 'Patti Shohani', ' Patti Sultan Lashari', ' Patti Darwesh Lashari ', 'Kot Daud', ' Kehro Kaheri', 'Bahesti', 'Mad Koura', 'Raheem Yar Khan', ' Iman Garh', ' Koot Kandhara Singh', '237/9R', ' 238/9R', 'Kisran ', 'Bhonawali ', 'Dhullian', ' Ghreebwal ', 'Pirana', ' Rawal', ' Domiyal', ' Nathial', ' Dhoke Halim', 'Pirani ', 'Mikyal', ' Spyal', 'Dhok Gangawali ', 'Ghuman', 'Masu Sikhani', 'Ahmadani', 'Shadan', ' Lound', ' Chak Kandi Wala', 'Kofli', 'Gazi', 'Kala', 'Basti Ranjha', 'Ramin', 'Shero Dasti', 'Joni', 'Gajani', 'Pati Tali', 'Bait Sawai', 'Shah Sadar Din', 'Chak Bahadur Garh', 'Kot Mubarak Shumali', 'Kot Mubarak Janubi', 'Thaddi', 'Pati Sohani', 'Rakh Dhao Sheikhani', 'Qadra Jarwar', 'Chak Nao Abad', 'Peer Adil', 'Chak Jarwar', 'Kot Daud', 'Jarwar Khas', 'Ranwan', 'Paki', 'Chak Jhangail', 'Ghumrani', 'Umrani', 'Jiani', 'Yaroo', 'Khalool', 'Chabrai', ' Bala', ' Gharbi', 'Jhok Yar Shah', 'Chabri Zareen', 'Rakh Chabri Zareen', 'Ladan', 'Noria Koria Gharbi', 'Noria Koria Sharqi', 'Tibi Kharak', 'Bait Malana ', 'Dalana Pati Bhochri', 'Churhatta Sindh Shumali', 'Churhatta Pachad Shumali ', 'Noor Wah', 'Baila', 'Churhatta Kot Haibat', 'Dalana Pati Khas', 'Qasba Dera', 'Gadai Gharbi', 'Gadai Shumali', 'Gadai Sharqi', 'Dera Gharbi', 'Kotla Sikhani Gharbi', 'Darh Opla', 'Chak Dalail', 'Samina Gharbi', 'Haji Ghazi Ghari', 'Darahma', 'Bait Mohrai', 'Sobha Arain', 'Haji Ghazi Sharqi', 'Dera Purana', 'Chotala', 'Guja Bahar Sial', 'Mandoos Wala', 'Bhasti Bhai ', 'Chit Sarkani', 'Paigah Chak No. 1', 'Paigah Chak No. 2', 'Paigah Chak No. 3', 'Khakhi Gharbi', 'Gagoo', 'Basti Khosa', 'Mamoori', 'Dagar Chit', 'Pai Ramdani'
   ]

# Takes processed_df (with only patwari_name, contact_no, mouza) and prepares data_mouzas list with 1 mouza  on each index in title case and return it.
def prepare_known_mouzas_list(processed_df):
    '''Takes processed_df (with only patwari_name, contact_no, mouza) and prepares data_mouzas list with 1 mouza on each index in title case and return it.'''
    # preparing data_mouzas list
    print('Inside prepare_known_mouzas_list')
    print('-- Preparing data_mouzas list')
    data_mouzas = []

    for patwari_mouzas in processed_df['mouza']:
        # if there are comma-separated mouza names in any entry, then replacing (,) with (, ) and splitting the string and extending into data_mouuzas list after converting to title case.
        if patwari_mouzas.find(',') != -1:
            patwari_mouzas = patwari_mouzas.replace(',', ', ')
            mouzas = patwari_mouzas.split(', ')
            mouzas = [mouza.title() for mouza in mouzas]
            data_mouzas.extend(mouzas)
            print(f'-- {mouzas} extended.')

        else:
            # converting single patwari_mouzas to title and appending
            patwari_mouzas = patwari_mouzas.title()
            data_mouzas.append(patwari_mouzas)
            print(f'-- {patwari_mouzas} appended.')

    # uncomment to print the mouza as a list
    # print(data_mouzas)
    print(f'-- data_mouzas [] created. Length (known mouzas): {len(data_mouzas)}. Returning it.')
    return data_mouzas


# Takes csv data file path and dropped unused columns, prepares data_mouzas list, and returns [df, data_mouzas]
def prepare_data(csv_data_filepath: str):
    '''Prepares raw data. Takes csv data file path and dropped unused columns, prepares data_mouzas list, and returns [df, data_mouzas]'''

    ### Data preprocessing
    print('Inside prepare_data()')
    df = pd.read_csv(csv_data_filepath)
    print('-- Data loaded')

    # converting column names to lowercase and dropping unused features
    print('-- Converting column names to lowercase.')
    df.columns = df.columns.str.lower()
    print('-- Dropping unused features.')
    df.drop(['timestamp', 'tehsil', 'district', 'your e-mail'], axis=1, inplace=True)

    # preparing data_mouzas list
    data_mouzas = prepare_known_mouzas_list(df)

    # saving processed_dataframe
    print('-- Saving processed_dataframe')
    df.to_csv(csv_data_filepath, index=False)

    print('-- Returning data_mouzas')
    return data_mouzas


# Loads the dataframe
def load_df():
    '''Loads dataframe (using globally set filename) into the global var: df'''
    print('Inside load_df')
    # Indicating the use of the global var
    global df, csv_data_filepath
    df = pd.read_csv(csv_data_filepath)
    print('-- Data loaded globally.\n')
    return 0


###################################### Validates the user's input
def validate_contact(user_contact):

    print('\nInside validate_contact()')
    fake_contacts = [
        '00000000000', '11111111111', '22222222222', '33333333333', '44444444444', '55555555555', '66666666666', '77777777777', '88888888888', '99999999999', '03000000000', '03011111111', '03022222222', '03696969696', '03707070707',
        '03033333333', '03044444444', '03055555555', '03066666666', '03077777777', '03088888888', '03099999999', '03101010101', '03111111111', '03121212121', '03131313131', '03141414141', '03151515151', '03161616161', '03171717171', '03181818181', '03191919191', '03202020202', '03212121212', '03222222222', '03232323232', '03242424242', '03252525252', '03262626262', '03272727272', '03282828282', '03292929292', '03303030303', '03313131313', '03323232323', '03333333333', '03343434343', '03353535353', '03363636363', '03373737373', '03383838383', '03393939393', '03404040404', '03414141414', '03424242424', '03434343434', '03444444444', '03454545454', '03464646464', '03474747474', '03484848484', '03494949494', '03505050505', '03515151515', '03686868686',
        '03525252525', '03535353535', '03545454545', '03555555555', '03565656565', '03575757575', '03585858585', '03595959595', '03606060606', '03616161616', '03626262626', '03636363636', '03646464646', '03656565656', '03666666666', '03676767676'
    ]
    
    # if provided user contact no is not a digit or (it's length is something other than 11) then returning 1
    if not (user_contact.isdigit()) or not (len(user_contact) == 11):
        print(f'Length is not 11 or is not digit. Isdigit: {user_contact.isdigit()}. Length = {len(user_contact)}. Returning 1\n')
        return 1

    # if the provided user contact exists in fake_contacts[] returning 1 else 0
    elif user_contact in fake_contacts:
        print('-- Provided contact is fake. Returning 1\n')
        return 1
    
    else:
        print("-- User contact don't exist in fake_contacts[]. Returning 0\n")
        return 0


def validate_input():
    print('Inside validate_input()')
    global session

    # validating input_fields i.e. If they have data and the data is right
    input_fields = [session.user_name, session.user_profession, session.selected_mouza, session.user_contact]
    inputs_bools = list(map(lambda input: True in [input_char.isalpha() or input_char.isspace() for input_char in input], input_fields[0:3]))

    contact_validation_res = validate_contact(input_fields[3])

    if '' in input_fields:
        print('-- Null value found in user inputs. Returning 1\n')
        return 1

    # checking user inputs except contact, if they are not alpha (abc) then returning 1.

    if False in inputs_bools:
        print(f'-- Alpha inputs contain numerical data. The value is {input_fields[inputs_bools.index(False)]}. Returning 1\n')
        return 1

    # passing user contact no to validate_contact() and checking if the response is not 0 then returning 1
    elif contact_validation_res != 0:
        print(f'-- User contact is not numeric or its length is not 11 or it exists in the fake_contacts[]. Provided contact: { input_fields[3] }\n')
        return 1

    else:
        print('All user inputs are validated. Returning 0\n')
        return 0

# Takes mouza_name and checks if we have this mouza. If yes then returns [patwari_name, patwari_no] else returns 1
def handle_user_input(mouza_name):
    '''Takes mouza_name and checks if we have this mouza. If yes then returns [patwari_name, patwari_no] else returns 1'''
    print('Inside handle_user_input')
    # Looking for index
    print('-- Looking for index')
    # Accessing global var
    global df
    index = df[df['mouza'].str.contains(mouza_name, case=False)].index

    # checking if match found or not. If we have an index
    if len(index) != 0:
        index = index[0]
        print(f'-- Match found. Index: {index}. Extracting details')
        patwari_name = df['your name'][index]
        patwari_no = df['contact no.'][index]

        print('-- Returning details')
        return [patwari_name, patwari_no]

    else:
        print('-- Match not found. Returning 1')
        return 1


###################################### Updates dropbox logs file
def update_dropbox_logsfile(log_content):
    print('\n\nInside update_dropbox_logsfile()')
    # token = st.secrets['dropbox_token']
    token = 'sl.BwDHlIC9JmqEfYCd1vQwgn5hP5RTg7xBqr82jkuJmr3UsVi3Hap7aiq8bcqJnwJnbGPlteMJ3DV274I8D8pM4-5z_Fkuv0Njbz5KlNUblO6m1p6u10pAfxh76x2qttDYmQUaIXYBefu0'

    # Connecting to dropbox
    try:
        dbx = dropbox.Dropbox(token)
        dbx.users_get_current_account()
        print('-- Dropbox connection successful.')

    except:
        print('-- Error connecting to dropbox.')

    # Downloading server file contents and writting to local file
    print('-- Preserving existing data. Downloading server file contents and writting to local file')
    with open(log_filename, 'wb') as llf:
        _, response = dbx.files_download('/' + log_filename)
        llf.write(response.content)

    print('-- done')

    # Updating downloaded file
    print('-- Appending log details')
    with open(log_filename, 'a', newline = '') as lf:
        csv_writter = csv.writer(lf)
        csv_writter.writerow(log_content)

    # Uploading updated file to server
    print('-- Uploading updated file to server')
    try:
        with open(log_filename, 'rb') as lf:
            dbx.files_upload(lf.read(), '/' + log_filename, mode = dropbox.files.WriteMode('overwrite'))

        print('-- Server file uploaded (overwritten) successfully. Returning 0\n')
        return 0

    except:
        print('-- An error occured while uploading the updated file. Returning 1\n')
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

    # Handling log updation
    print('-- Handling log updation. Going inside update_dropbox_logsfile')
    update_dropbox_logsfile(log_content)

    print('-- Log saved. Returning 0\n')
    return 0


###################################### MAIN
def main():
    ################################## Configuring the app
    global df, data_mouzas
    # Loading data
    print('\n-------------------------------------------------------- \
          \n Loading df... \n')
    load_df()

    ################################## Creating UI

    # -------------------------------- setting page configurations
    st.set_page_config(page_title='Contact Patwari', page_icon=':telephone_receiver:', layout = 'centered')
    with st.sidebar:
        st.header(':telephone_receiver: Contact Patwari App.')
        st.caption(":smile: Let's solve it today.")

    # -------------------------------- UI
    # title part
    st.title(':telephone_receiver: Contact Patwari')
    st.caption( "We possess contact details for Punjab patwaris across more than 100 villages. If you are a patwari and don't find your details here, kindly reach out to the owner via WhatsApp at: 0318-5842448. If you want to know How to use the app. Just hit the sidebar icon > and click Usage.")
    st.video('desktop-contact-patwari-intro.mp4')
    st.divider()

    # user details part
    u_name, u_prof, u_contact = st.columns(3)
    # adding user name column
    with u_name:
        st.text_input(label='Your name:', placeholder = 'Shaukat Ali', key='user_name')
    # adding user profession column
    with u_prof:
        st.text_input(label='Your profession:', placeholder = 'Patwari', key='user_profession')
    # adding user contact no column
    with u_contact:
        st.text_input(label='Your contact', placeholder = '03185842448', key='user_contact')

    # Taking input part
    st.selectbox(label='Please select mouza', options=data_mouzas, key='selected_mouza')
    st.button(label='Get Contact', type = 'primary', key='contact_btn')


    ################################## Dealing with user input

    if session.contact_btn:
        with st.spinner('Please wait...'):
            print(print('\n-------------------------------------------------------- \
                         \n Button pressed. Validating inputs... \n'))
            validation_result = validate_input()

            # if all the required fields are filled.
            if validation_result != 1:
                print('\n-------------------------------------------------------- \
                        \n Getting patwari details... \n')

                # Getting patwari details
                patwari_details = handle_user_input(session.selected_mouza)

                if isinstance(patwari_details, list):

                    # Recording that the username with profession and contact_no successfully takesn the details of patwari of mouza: selected mouze. The file is a csv.
                    print('Recording log..')
                    record_log(session.user_name, session.user_profession, session.user_contact, session.selected_mouza, 'Successful')
                    print('Done \n\n')
                    
                    # Printing output
                    print('\n-------------------------------------------------------- \
                        \n Giving details to user... \n')

                    name, contact = patwari_details
                    st.write(f':blue[Patwari name:] {name}')
                    st.write(f':blue[Contact:] {contact}')


                # If result not found
                else:
                    # recording logs
                    print('Recording log..')
                    record_log(session.user_name, session.user_profession, session.user_contact, session.selected_mouza, 'No Details')
                    print('Done \n\n')

                    # printing output
                    st.error('Details not found.')


            # if inputs are not valid
            else:
                # recording logs
                print('Recording log..')
                record_log(session.user_name, session.user_profession, session.user_contact, session.selected_mouza, 'Validation Failed')
                print('Done \n\n')
                # Uncomment for debugging
                # st.write(session)

                # printing output (error)
                st.error('Please fill all the fields correctly.')

if __name__ == '__main__':
    main()