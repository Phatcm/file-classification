import streamlit as st
import requests
import json

def app():
    search_query = st.text_input("Search for files")
    if st.button("Search"):
        if search_query is not None:
            api_base_url = "https://o38ehtiqc5.execute-api.ap-northeast-1.amazonaws.com/prod/files"
            response = requests.post(api_base_url, params={'query': search_query})
            
            if response.status_code == 200:
                file_names = response.json()
                st.write("Similar files: ")
                for file_name in file_names:
                    st.write(file_name)
            else:
                st.write("Failed to retrive similar files")
    