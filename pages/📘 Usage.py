import streamlit as st
session = st.session_state


################################## Creating UI

# -------------------------------- setting page configurations
st.set_page_config(page_title='Contact Patwari', page_icon=':telephone_receiver:', layout = 'centered')
with st.sidebar:
    st.header(':blue_book: Usage Guidelines')
    st.caption(":smile: Let's make it happen.")

# -------------------------------- UI
# title part
st.title(':blue_book: Usage Guidelines')
st.caption( "Following are two videos i.e. For desktop and For Mobile. Just watch the video you want and you will be ready to use the application. If you have any queries, contact the owner at: 0318-5842448")
st.divider()

# videos part
st.selectbox(label = 'Select your device.', options = ['Desktop', 'Mobile'], key = 'user_device')


#--------------------------------- Handling user selection
if session.user_device == 'Desktop':
    # st.subheader('This place is for desktop video')
    st.video('desktop-contact-patwari-intro.mp4')

# for any value (i.e. mobile) of user_device selectbox
else:
    st.video('mobile-contact-patwari-intro.mp4')