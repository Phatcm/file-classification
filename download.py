import streamlit as st
import requests
import json
import time
import pandas as pd
import webbrowser 

def app():
    api_base_file = "https://i52vmx81j2.execute-api.ap-northeast-1.amazonaws.com/prod/files"
    response = requests.get(api_base_file)
    data = response.json()
    
    #search result
    items = data['Items']
    df = pd.DataFrame(items, columns=['FileName'])
    text_search = st.text_input("Search by name", value="")

    
    #define column name:
    colms = st.columns((1, 2, 2, 2, 2))
    fields = ["№", 'Name', 'Type', "Download", "Delete"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)
    
    #loop to show all files:
    for i, item in enumerate(items):
        item_name = item["FileName"]
        item_type = item["FileType"]
        file_name = item["FileType"]+"/"+item["FileName"]

        #condition to show only search result:
        if text_search:
            search_result = df["FileName"].str.contains(text_search)
            desired_content = df.loc[search_result]
            content_list = desired_content['FileName'].tolist()
            for name in content_list:
                if name == item_name:
                    list_item(api_base_file, i, item_name, item_type, file_name)
        else:
            list_item(api_base_file, i, item_name, item_type, file_name)
                    
def list_item(api_base_file, i, item_name, item_type, file_name):
            
    col1, col2, col3, col4, col5 = st.columns((1, 2, 2, 2, 2))
    col1.write(i) #index
    col2.write(item_name) #File name
    col3.write(item_type) #File type
    if col4.button("Download", item_name):
        api_base_url = "https://i52vmx81j2.execute-api.ap-northeast-1.amazonaws.com/prod/url"
        response = download_url(api_base_url, file_name)
        if response.status_code == 200:
            presigned_url = json.loads(response.text)
            webbrowser.open(presigned_url, new=0, autoraise=True)
        else:
            st.write("Failed to retrieve presigned URL")
    if col5.button("Delete", item_name+"1", type="primary"):
        response = delete_item(item_name, item_type, api_base_file)
        if response.status_code == 200:
            st.toast("You delete '"+item_name+"'")
            time.sleep(0.3)
            st.experimental_rerun()
        else:
            st.toast("Delete file failed")

def download_url(api_base_url, file_name):
    download_url = "{}?download={}".format(api_base_url, file_name)
    response = requests.get(download_url)
    
    return response

def delete_item(item_name, item_type, url):
    metadata = {
                    "name": item_name,
                    "type": item_type
                }
    delete_url = "{}?delete={}".format(url,json.dumps(metadata))
    response = requests.delete(delete_url)
    
    return response