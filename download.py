import streamlit as st
import requests
import json
from streamlit_extras.stylable_container import stylable_container

def app():
    api_base_file = "https://i52vmx81j2.execute-api.ap-northeast-1.amazonaws.com/prod/files"
    response = requests.get(api_base_file)
    data = response.json()

    #list items
    items = data['Items']
    for item in items:
        file_name = item["FileType"]+"/"+item["FileName"]
        if st.button(f"Download {file_name}"):
            api_base_url = "https://i52vmx81j2.execute-api.ap-northeast-1.amazonaws.com/prod/url"
            api_url = "{}?download={}".format(api_base_url, file_name)
            response = requests.get(api_url)
            
            if response.status_code == 200:
                response_result = json.loads(response.text)
                presigned_url = response_result
                st.markdown(f'<a href="{presigned_url}">Click here to download</a>', unsafe_allow_html=True)
            else:
                st.write("Failed to retrieve presigned URL")