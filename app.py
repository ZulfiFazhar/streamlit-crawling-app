import streamlit as st
from datetime import datetime
import subprocess

st.title("Crawling anjay mabar")

with st.form(key='tweet_harvest'):
    token = st.text_input("Auth Token")
    keyword = st.text_input("Keyword")
    start_date = st.date_input("Tanggal Mulai", datetime.now())
    end_date = st.date_input("Tanggal Selesai", datetime.now())
    limit = st.number_input("Limit", 500)
    
    search_keyword = f'{keyword} until:{end_date} since:{start_date}'

    submit_button = st.form_submit_button(label='Start')

if submit_button:
    filename = f'crawling_{keyword}_{start_date}_{end_date}.csv'

    with st.spinner('Crawling..'):
        command = [
            'C:\\Program Files\\nodejs\\npx.cmd', '--yes', 'tweet-harvest@latest',
            '-o', filename,
            '-s', search_keyword,
            '-l', str(limit),
            '--token', token
            ]

        result = subprocess.run(command, capture_output=True, text=True)

    st.write(result.stdout)
    st.write(result.stderr)

    st.success(f"Crawling berhasil! Data berhasil disimpan dalam file {filename}")

    # !npx --yes tweet-harvest@latest -o "{filename}" -s "{search_keyword}" -l {limit} --token "{token}"
