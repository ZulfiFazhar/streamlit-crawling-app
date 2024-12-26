import streamlit as st
from datetime import datetime, timedelta
import subprocess

col1, col2 = st.columns([1, 8])
with col1:
    st.image("assets/Socialabs-Logo.svg", width=100)
with col2:
    st.title("Socialabs Data Crawling")
    st.write("")

with st.form(key='tweet_harvest'):
    token = st.text_input("Auth Token")
    keyword = st.text_input("Keyword")
    start_date = st.date_input("Tanggal Mulai", datetime.now() - timedelta(days=1))
    end_date = st.date_input("Tanggal Selesai", datetime.now())
    limit = st.number_input("Limit", 20)
    
    search_keyword = f'{keyword} until:{end_date} since:{start_date}'

    submit_button = st.form_submit_button(label='Start')

if submit_button:
    filename = f'crawling_{keyword}_{start_date}_{end_date}.csv'

    with st.spinner('Crawling..'):
        result = subprocess.check_call(f'npx --yes tweet-harvest@latest -o "{filename}" -s "{search_keyword}" -l {str(limit)} --token "{token}"', shell=True)

    st.success(f"Crawling berhasil!")
    st.success(f"Data berhasil disimpan di tweets-data/{filename}")

    # !npx --yes tweet-harvest@latest -o "{filename}" -s "{search_keyword}" -l {limit} --token "{token}"
