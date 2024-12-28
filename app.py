import os
import shutil
import subprocess
import streamlit as st
from datetime import datetime, timedelta
from drive.upload import upload_file, create_folder

col1, col2 = st.columns([1, 8])
with col1:
    st.image("assets/Socialabs-Logo.svg", width=100)
with col2:
    st.title("Socialabs Data Crawling")
    st.write("")

tab1, tab2 = st.tabs(["Crawling Data", "Upload to Google Drive"])

with tab1:
    language_option = {
        "Bahasa Indonesia": "id",
        "English": "en"}
    
    with st.form(key='tweet_harvest'):
        token = st.text_input("Auth Token")
        keyword = st.text_input("Keyword")
        language = st.selectbox("Language", list(language_option.keys()))
        start_date = st.date_input("Tanggal Mulai", datetime.now() - timedelta(days=1))
        end_date = st.date_input("Tanggal Selesai", datetime.now())
        limit = st.number_input("Limit", 20)
        
        language_id = language_option[language]

        search_keyword = f'{keyword} lang:{language_id} until:{end_date} since:{start_date}'

        submit_button = st.form_submit_button(label='Start')

    if submit_button:
        filename = f'crawling_{keyword}_{start_date}_{end_date}.csv'

        with st.spinner('Crawling..'):
            result = subprocess.check_call(f'npx --yes tweet-harvest@latest -o "{filename}" -s "{search_keyword}" -l {str(limit)} --token "{token}"', shell=True)

        st.success(f"Crawling berhasil!\nData berhasil disimpan di tweets-data/{filename}")

        # !npx --yes tweet-harvest@latest -o "{filename}" -s "{search_keyword}" -l {limit} --token "{token}"

with tab2:
    st.subheader("Upload File")
    uploaded_file = st.file_uploader("Select a file to upload")
    parent_folder_id = "1w3kBu8fvzHhLcXhecNwynaOTySF2lwA5"

    if uploaded_file:
        temp_dir = "temp_uploads/"
        os.makedirs(temp_dir, exist_ok=True)

        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File are successfully saved temporarily: {temp_file_path}")

        if st.button("Upload File"):
            today = datetime.now().strftime('%Y-%m-%d')
            try:
                with st.spinner('Uploading file...'):
                    date_folder_id = create_folder(today, parent_folder_id)
                    upload_file(temp_dir, date_folder_id)
                    st.success(f"File are successfully uploaded to Google Drive in the Socialabs/Crawling/{today}")
            except Exception as e:
                st.error(f"Error during upload: {e}")
            finally:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
    else:
        st.warning("Please select a file to upload.")

